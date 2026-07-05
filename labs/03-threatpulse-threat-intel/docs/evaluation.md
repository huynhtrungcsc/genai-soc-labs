# Evaluation

ThreatPulse should be evaluated on operational usefulness, not just output quality.

## Functional Checks

- Asset inventory can be loaded and listed.
- Threat intelligence can be ingested with CVE, IOC, MITRE, and reference fields.
- Intelligence is prioritized by relevance to internal assets.
- Briefings include evidence, assumptions, and recommended actions.
- Draft briefings require approval.
- Audit events are generated for ingestion, briefing generation, and approval.

## Quality Criteria

| Area | Expected Behavior |
|---|---|
| Relevance | Matching assets rise above unrelated intel |
| Prioritization | Active exploitation and exposed critical assets become high or critical |
| Evidence | Briefings preserve source, CVE, exploitation, and affected asset evidence |
| Safety | No exploit steps or offensive automation are produced |
| Governance | Approval and audit events are visible |

## Example Test Cases

1. Active exploitation against an internet-facing remote access product should produce critical priority.
2. High severity advisory with no matching asset should stay lower than matched critical assets.
3. Executive briefing should avoid analyst-heavy technical detail.
4. Patch briefing should emphasize affected hosts and SLA.
5. Unknown products should generate a monitoring action instead of false asset impact.

## Known Limitations

- Product matching is normalized string matching, not a full CPE resolver.
- Source reliability is user supplied.
- No external NVD, CISA, or vendor API is called by default.
- No LLM is called by default; generation is deterministic for reproducibility.
