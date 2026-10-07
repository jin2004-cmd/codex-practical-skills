---
name: Bug report
about: A skill did not trigger, ran wrongly, or its description does not match its behaviour
title: "[bug] <skill name>: <one line>"
labels: bug
body:
  - type: input
    id: skill
    attributes:
      label: Which skill
      description: Folder name, for example llm-output-eval-gate
    validations:
      required: true
  - type: textarea
    id: input
    attributes:
      label: What you gave it
      description: Paste the actual request or input. No personal names, companies, or contact details please.
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: What you expected
    validations:
      required: true
  - type: textarea
    id: actual
    attributes:
      label: What actually happened
    validations:
      required: true
  - type: textarea
    id: env
    attributes:
      label: Environment
      description: Agent (Codex / Claude / other), OS, and any runtime dependency installed
  - type: checkboxes
    id: privacy
    attributes:
      label: Privacy check
      options:
        - label: I removed names, employers, salaries, contact details, and private links from everything above
          required: true
