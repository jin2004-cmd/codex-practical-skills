---
name: workflow-distiller
description: Extract a reusable assistant workflow from a completed task when the user requests skill distillation or a repeated process has been validated. Not for one-off answers or unverified fixes.
---

# Workflow Distiller

Turn a repeated, verified process into a narrow reusable Skill. Ordinary facts belong in memory; a one-off task belongs in a task record.

1. Inspect the existing Skill index first. Prefer a focused update to an existing capability over a duplicate.
2. Record the real trigger, inputs, outputs, failure modes, and validation evidence. Mark an idea as a candidate when evidence is incomplete.
3. Keep SKILL.md short: purpose, trigger boundary, essential constraints, and routing. Put mode-specific guidance in references and deterministic repeated work in scripts.
4. Define both positive and negative examples so unrelated work does not trigger the Skill.
5. Use the available skill-creator when creating or changing a Skill. Run quick_validate.py, and run new scripts in an isolated test case.
6. Do not copy secrets, private conversations, company material, or hidden reasoning. A Skill never expands authorization to publish, send, install, or modify unrelated systems.
