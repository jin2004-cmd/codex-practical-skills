"""Advisory, single-writer turn counter. No chat access, network, or compaction API."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from datetime import datetime, timezone


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def initial(interval: int) -> dict:
    return {"schema_version": 1, "interval": interval, "count": 0,
            "recent_key_hashes": [], "last_checkpoint": None}


def read_state(path: Path, requested_interval: int | None) -> dict:
    if not path.exists():
        return initial(requested_interval or 5)
    state = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(state, dict) or state.get("schema_version") != 1:
        raise ValueError("unsupported state schema; preserved without changes")
    if type(state.get("interval")) is not int or not 1 <= state["interval"] <= 100:
        raise ValueError("invalid interval in state; preserved without changes")
    if type(state.get("count")) is not int or state["count"] < 0:
        raise ValueError("invalid count in state; preserved without changes")
    keys = state.get("recent_key_hashes")
    if not isinstance(keys, list) or len(keys) > 128 or any(
        not isinstance(k, str) or len(k) != 64 or any(c not in "0123456789abcdef" for c in k)
        for k in keys
    ):
        raise ValueError("invalid key history; preserved without changes")
    if state.get("last_checkpoint") is not None and not isinstance(state["last_checkpoint"], dict):
        raise ValueError("invalid checkpoint metadata; preserved without changes")
    if requested_interval is not None and requested_interval != state["interval"]:
        raise ValueError("interval differs from existing state; not silently changed")
    return state


def write_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
                                         prefix=".checkpoint-", suffix=".tmp", delete=False) as file:
            temporary = file.name
            json.dump(state, file, ensure_ascii=False, indent=2)
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--interval", type=int)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    tick = sub.add_parser("tick")
    tick.add_argument("--turn-key", required=True)
    complete = sub.add_parser("complete")
    complete.add_argument("--checkpoint", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.interval is not None and not 1 <= args.interval <= 100:
            raise ValueError("interval must be between 1 and 100")
        state = read_state(args.state, args.interval)
        counted = False
        if args.command == "tick":
            if not args.turn_key.strip():
                raise ValueError("turn-key cannot be empty")
            key_hash = hashlib.sha256(args.turn_key.encode("utf-8")).hexdigest()
            if key_hash not in state["recent_key_hashes"]:
                state["recent_key_hashes"] = (state["recent_key_hashes"] + [key_hash])[-128:]
                state["count"] += 1
                state["updated_at"] = now()
                write_state(args.state, state)
                counted = True
        elif args.command == "complete":
            if not args.checkpoint.is_file():
                raise ValueError("checkpoint must be an existing UTF-8 file")
            raw = args.checkpoint.read_bytes()
            if not raw.decode("utf-8-sig").strip():
                raise ValueError("checkpoint cannot be empty")
            fingerprint = hashlib.sha256(raw).hexdigest()
            previous = state["last_checkpoint"]
            if previous and previous.get("sha256") == fingerprint:
                if state["count"]:
                    raise ValueError("checkpoint unchanged since new turns; state preserved")
                # A retried completion must not erase the original covered_turns.
            else:
                state["last_checkpoint"] = {
                    "path": str(args.checkpoint.resolve()), "sha256": fingerprint,
                    "bytes": len(raw), "completed_at": now(), "covered_turns": state["count"]}
                state["count"] = 0
                state["updated_at"] = now()
                write_state(args.state, state)
        print(json.dumps({"count": state["count"], "interval": state["interval"],
                          "due": state["count"] >= state["interval"], "counted": counted,
                          "last_checkpoint": state["last_checkpoint"]}, ensure_ascii=False))
        return 0
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        # Do not print malformed state or user-provided text.
        print(json.dumps({"error": type(error).__name__, "state_preserved": True}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
