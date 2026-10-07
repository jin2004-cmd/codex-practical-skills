"""Read-only checks for one Obsidian memory area; no note contents in output."""
import argparse
import json
import re
import sys
from pathlib import Path

# Prefer an optional packaged dependency when present; public installs may use
# their own PyYAML instead of carrying a platform-specific binary.
sys.path.insert(0, str(Path(__file__).resolve().parent / "_deps"))
try:
    import yaml
except ModuleNotFoundError as exc:
    raise SystemExit("validate_memory.py requires PyYAML; install it in the active environment") from exc

WIKI = re.compile(r"!?\[\[([^\]\n]+)\]\]")
SENSITIVE = [
    re.compile(r"https://open\.feishu\.cn/open-apis/bot/v2/hook/[a-f0-9-]{20,}", re.I),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"(?:app_secret|api_key|access_token|refresh_token)\s*[:=]\s*[\"']?[A-Za-z0-9_-]{16,}", re.I),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", required=True)
    parser.add_argument("--area", required=True)
    args = parser.parse_args()
    vault = Path(args.vault).resolve()
    area = (vault / args.area).resolve()
    if not area.is_relative_to(vault) or not area.is_dir():
        raise SystemExit("Area must be an existing directory within the vault.")
    errors = []
    notes = sorted(area.rglob("*.md"))
    canvases = sorted(area.rglob("*.canvas"))

    if not notes:
        errors.append({"file": area.relative_to(vault).as_posix(), "reason": "Memory area contains no notes"})

    def fail(path, reason):
        errors.append({"file": path.relative_to(vault).as_posix(), "reason": reason})

    def resolve_link(target):
        target = target.split("|", 1)[0].split("#", 1)[0].strip()
        if not target:
            return True
        # Explicit vault-relative links avoid resolving ambiguous duplicate names.
        if "/" not in target and "\\" not in target:
            return False
        path = (vault / target).resolve()
        if not path.is_relative_to(vault):
            return False
        return path.is_file() or (path.suffix == "" and path.with_suffix(".md").is_file())

    for path in notes:
        body = path.read_text(encoding="utf-8-sig")
        match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", body, re.S)
        if not match:
            fail(path, "Missing YAML properties")
        else:
            try:
                props = yaml.safe_load(match.group(1))
                if not isinstance(props, dict):
                    raise ValueError("Properties must be a mapping")
                if not props.get("title") or not props.get("created"):
                    fail(path, "Missing title or created")
                tags = props.get("tags")
                if not isinstance(tags, list) or not 3 <= len(tags) <= 5:
                    fail(path, "Expected 3 to 5 tags")
                elif len(set(tags)) != len(tags) or any("/" in str(tag) for tag in tags):
                    fail(path, "Duplicate or hierarchical tags")
            except (yaml.YAMLError, ValueError, TypeError) as exc:
                fail(path, "Invalid properties: " + type(exc).__name__)
        for target in WIKI.findall(body):
            if not resolve_link(target):
                fail(path, "Unresolved or ambiguous internal link: " + target)
        if any(pattern.search(body) for pattern in SENSITIVE):
            fail(path, "Possible credential pattern; inspect locally")

    for path in canvases:
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
            nodes, edges = data.get("nodes", []), data.get("edges", [])
            all_ids = [item["id"] for item in nodes + edges]
            if len(set(all_ids)) != len(all_ids):
                fail(path, "Duplicate node or edge ID")
            node_ids = {node["id"] for node in nodes}
            for node in nodes:
                kind = node.get("type")
                if kind not in {"text", "file", "link", "group"}:
                    fail(path, "Unknown node type")
                if not all(key in node for key in ("x", "y", "width", "height")):
                    fail(path, "Missing node geometry")
                elif any(not isinstance(node[key], (int, float)) for key in ("x", "y", "width", "height")) or node["width"] <= 0 or node["height"] <= 0:
                    fail(path, "Invalid node geometry")
                required = {"text": "text", "file": "file", "link": "url"}.get(kind)
                if required and required not in node:
                    fail(path, "Missing type-specific node field")
                if kind == "file" and not resolve_link(node.get("file", "")):
                    fail(path, "Unresolved Canvas file")
            for edge in edges:
                if edge.get("fromNode") not in node_ids or edge.get("toNode") not in node_ids:
                    fail(path, "Dangling edge")
                for key in ("fromSide", "toSide"):
                    if key in edge and edge[key] not in {"top", "right", "bottom", "left"}:
                        fail(path, "Invalid edge side")
        except (ValueError, KeyError, TypeError, AttributeError):
            fail(path, "Invalid Canvas structure")
    print(json.dumps({"notes": len(notes), "canvases": len(canvases), "errors": errors}, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
