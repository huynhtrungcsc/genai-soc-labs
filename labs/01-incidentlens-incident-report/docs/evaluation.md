# Evaluation

The first implementation is deterministic so it can be tested without external model access.

## Current Checks

- Parser extracts normalized events from JSONL and text logs.
- Timeline identifies common SOC investigation phases.
- MITRE mapping returns known ATT&CK techniques for sample evidence.
- Report generator separates analyst detail from executive summary.
- API requires authentication for incident data.

## Future LLM Evaluation

When an LLM provider is added, evaluate:

- Factual grounding against event evidence
- No invented hosts, users, IPs, or timestamps
- Clear separation of observation and inference
- Useful remediation recommendations
- Refusal of unsafe offensive instructions
