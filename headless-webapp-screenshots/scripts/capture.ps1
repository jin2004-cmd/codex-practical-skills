param(
  [Parameter(Mandatory=$true)][string]$Url,
  [Parameter(Mandatory=$true)][string]$Out,
  [int]$Width = 1440,
  [int]$Height = 900,
  [double]$Scale = 1,
  [int]$Budget = 8000,
  [string]$Chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
)
# Capture a deterministic screenshot of a web page with headless Chrome.
# Examples:
#   .\capture.ps1 -Url "file:///C:/proj/harness.html?shot=1&view=today" -Out ".\shot-desktop.png"
#   .\capture.ps1 -Url "...?shot=1&view=stats&theme=dark" -Out ".\shot-mobile.png" -Width 390 -Height 844 -Scale 2
if (-not (Test-Path $Chrome)) {
  $edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
  if (Test-Path $edge) { $Chrome = $edge } else { throw "No Chrome/Edge found. Pass -Chrome <path>." }
}
$profileDir = Join-Path $env:TEMP ("shot-profile-" + [guid]::NewGuid().ToString("N").Substring(0,8))
& $Chrome --headless=new --disable-gpu --hide-scrollbars `
  "--user-data-dir=$profileDir" `
  "--virtual-time-budget=$Budget" `
  "--window-size=$Width,$Height" `
  "--force-device-scale-factor=$Scale" `
  "--screenshot=$Out" $Url 2>&1 | Out-Null
Remove-Item -Recurse -Force $profileDir -ErrorAction SilentlyContinue
if (Test-Path $Out) { Write-Output "saved: $Out" } else { throw "capture failed: $Out not created" }
