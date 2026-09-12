param(
    [Parameter(Mandatory = $true)]
    [string]$RepoPath,
    [string]$Remote = "origin",
    [string]$Branch = "main",
    [string]$Proxy,
    [int]$WarnFileSizeMB = 20,
    [int]$MaxFileSizeMB = 95,
    [switch]$Push
)

$ErrorActionPreference = "Stop"
$previousPromptSetting = $env:GIT_TERMINAL_PROMPT
$env:GIT_TERMINAL_PROMPT = "0"

function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Arguments)

    $gitArgs = @()
    if ($Proxy) {
        $gitArgs += @("-c", "http.proxy=$Proxy")
    }
    $gitArgs += $Arguments
    & git @gitArgs
    if ($LASTEXITCODE -ne 0) {
        throw "git command failed: git $($Arguments -join ' ')"
    }
}

try {
    $resolvedRepo = (Resolve-Path -LiteralPath $RepoPath).Path
    $root = (& git -C $resolvedRepo rev-parse --show-toplevel 2>$null).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $root) {
        throw "RepoPath is not a Git worktree: $resolvedRepo"
    }
    $root = (Resolve-Path -LiteralPath $root).Path

    $status = @(& git -C $root status --porcelain)
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to read Git status."
    }
    if ($status.Count -gt 0) {
        throw "Worktree is not clean. Commit or intentionally remove pending changes before publishing."
    }

    $currentBranch = (& git -C $root branch --show-current).Trim()
    if ($currentBranch -ne $Branch) {
        throw "Expected branch '$Branch' but current branch is '$currentBranch'."
    }

    $remoteUrl = (& git -C $root remote get-url $Remote).Trim()
    if ($LASTEXITCODE -ne 0 -or $remoteUrl -notmatch "github\.com[:/]") {
        throw "Remote '$Remote' is missing or is not a GitHub remote: $remoteUrl"
    }

    $oversized = @()
    $warnings = @()
    $treeLines = @(& git -C $root ls-tree -r -l HEAD)
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to inspect committed files."
    }
    foreach ($line in $treeLines) {
        if ($line -match "^\d+\s+\w+\s+\w+\s+(\d+)\t(.+)$") {
            $bytes = [int64]$Matches[1]
            $path = $Matches[2]
            $sizeMB = [math]::Round($bytes / 1MB, 2)
            if ($sizeMB -ge $MaxFileSizeMB) {
                $oversized += "$path ($sizeMB MB)"
            } elseif ($sizeMB -ge $WarnFileSizeMB) {
                $warnings += "$path ($sizeMB MB)"
            }
        }
    }
    if ($oversized.Count -gt 0) {
        throw "Files exceed the safe size limit: $($oversized -join ', ')"
    }

    Push-Location $root
    try {
        Invoke-Git fetch $Remote $Branch
        $localCommit = (& git rev-parse HEAD).Trim()
        $remoteRef = "refs/remotes/$Remote/$Branch"
        & git show-ref --verify --quiet $remoteRef
        if ($LASTEXITCODE -eq 0) {
            $remoteCommit = (& git rev-parse $remoteRef).Trim()
            & git merge-base --is-ancestor $remoteRef HEAD
            if ($LASTEXITCODE -ne 0) {
                throw "Remote branch is ahead or diverged. Stop and review before publishing."
            }
        } else {
            $remoteCommit = $null
        }

        Invoke-Git show --check --format= HEAD
        if ($Push) {
            Invoke-Git push $Remote "HEAD:$Branch"
            $mode = "pushed"
        } else {
            Invoke-Git push --dry-run $Remote "HEAD:$Branch"
            $mode = "dry-run"
        }

        [PSCustomObject]@{
            status = "ok"
            mode = $mode
            repository = $root
            remote = $remoteUrl
            branch = $Branch
            localCommit = $localCommit
            remoteCommitBefore = $remoteCommit
            warnings = $warnings
        } | ConvertTo-Json -Depth 3
    } finally {
        Pop-Location
    }
} finally {
    $env:GIT_TERMINAL_PROMPT = $previousPromptSetting
}
