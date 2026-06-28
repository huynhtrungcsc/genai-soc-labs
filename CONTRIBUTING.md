# Contributing

Thank you for improving `genai-soc-labs`. This repository is maintained as a professional AI cybersecurity engineering portfolio, so contributions should keep the structure clean, defensive, and reproducible.

## Development Principles

- Keep every lab focused on a realistic SOC or blue-team workflow.
- Prefer synthetic or sanitized datasets that can be safely published.
- Document assumptions, limitations, and security boundaries.
- Avoid code, prompts, or instructions that enable unauthorized access, malware creation, credential theft, or real-world exploitation.
- Favor clear architecture and evaluation over flashy demos.

## Lab Structure

A mature lab should eventually use this layout:

```text
labs/XX-lab-slug/
  README.md
  backend/
  frontend/
  sample-data/
  evals/
  docs/
  docker-compose.yml
```

The current repository starts with README scaffolds for all 29 labs. Implementation will be added incrementally.

## Pull Request Checklist

Before opening a pull request, make sure the change:

- Fits the lab scope and naming convention
- Updates the relevant README or documentation
- Uses defensive security framing
- Does not include secrets, tokens, real credentials, or sensitive customer data
- Adds evaluation notes when changing model behavior
- Keeps generated files and temporary artifacts out of Git

## Commit Style

Use concise, descriptive commits:

```text
docs: add lab 01 architecture notes
feat: scaffold incident report backend
chore: add shared RAG utilities
```
