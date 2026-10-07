---
name: Skill request
about: Suggest a new skill, or ask whether your case fits an existing one
title: "[skill] <one-line scenario>"
labels: enhancement
body:
  - type: textarea
    id: scenario
    attributes:
      label: The situation, in one sentence
      description: Write it the way you would say it to the assistant, for example "I have two internship offers and keep going back and forth"
    validations:
      required: true
  - type: textarea
    id: trigger
    attributes:
      label: When should it trigger, and when should it stay out of the way
    validations:
      required: true
  - type: textarea
    id: evidence
    attributes:
      label: Has this happened more than once
      description: A skill is worth writing when the same process has been validated at least twice. One-off tasks are not skills.
    validations:
      required: true
  - type: textarea
    id: existing
    attributes:
      label: Checked the existing 13 skills
      description: Read README.md first. If one of them is close, say which and why it does not fit.
    validations:
      required: true
  - type: checkboxes
    id: privacy
    attributes:
      label: Privacy check
      options:
        - label: This request contains no personal names, employers, salaries, or contact details
          required: true
