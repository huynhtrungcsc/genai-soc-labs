# Evaluation

The first implementation is deterministic so the lab can be tested without external model access.

## Current Checks

- Vietnamese and English questions map to expected hunt intents.
- SPL, Sentinel KQL, and Elastic KQL render valid draft syntax.
- Validation warnings are emitted for analyst review.
- Execution returns matching rows from the synthetic event dataset.
- API endpoints require authentication for query data.

## Future LLM Evaluation

When an LLM provider is added, evaluate:

- Query syntax validity for each SIEM dialect
- Field grounding against known schema
- No invented indexes, tables, or unsupported fields
- Correct handling of time ranges and boolean logic
- Analyst-rated usefulness of explanations and follow-up hunts
- Cost and safety warnings for broad production searches
