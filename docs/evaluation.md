# Evaluation

GenAI security tools need evaluation beyond whether the answer sounds fluent. Each lab should define task-specific measurements before it is considered complete.

## Baseline Evaluation Areas

- Factuality: Does the output stay grounded in provided evidence?
- Coverage: Does the model capture the important security events or findings?
- Precision: Does it avoid inventing indicators, hosts, users, or root causes?
- Usefulness: Would an analyst know the next step after reading the output?
- Safety: Does it avoid unsafe offensive instructions or sensitive data disclosure?
- Latency: Is the workflow usable during an investigation?

## Suggested Artifacts

Each mature lab should include:

```text
evals/
  cases.yaml
  expected/
  reports/
  README.md
```

Evaluation notes should explain both success cases and known failure modes.
