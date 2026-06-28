# Security and Ethics

This repository is designed for defensive cybersecurity education and authorized engineering work.

## Allowed Direction

- Detection engineering
- Threat hunting
- Incident response
- Security reporting
- Hardening and compliance
- Risk prioritization
- Authorized validation in controlled environments

## Disallowed Direction

- Malware generation
- Credential theft
- Exploit automation against real targets
- Unauthorized reconnaissance
- Instructions that enable harmful activity outside a defensive context
- Use of real private logs, credentials, or customer data in public commits

## Data Handling

Use synthetic or sanitized data by default. If a lab needs realistic logs, strip secrets, usernames, access tokens, IPs that identify a private environment, customer names, and any regulated personal data.

## Human Control

Any lab that suggests response actions such as account lockout, host isolation, firewall changes, or ticket escalation should keep humans in the approval loop.
