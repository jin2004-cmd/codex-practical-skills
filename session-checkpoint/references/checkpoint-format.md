# Checkpoint format

The project AGENTS.md defines the canonical memory area and checkpoint path. Keep one current checkpoint; put older events in the event log instead of creating competing "latest" files.

Include:

- the date, current goal, and a one-line project role;
- user-confirmed facts and preferences, separated from tool checks, suggestions, and unverified claims;
- actual artifacts, locations, and validation scope;
- authorization and privacy boundaries;
- unresolved blockers and the minimum information needed to resolve them;
- one to three next actions with their relevant entry points.

Read the current checkpoint first when resuming. Read the current-state file only when the task needs live status, and search historical logs only for a dated dispute. Do not save hidden chain-of-thought.
