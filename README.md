<div align="center">

# GenAI SOC Labs

Applied Generative AI systems for Security Operations Center workflows and AI cybersecurity engineering.

[![License: MIT](https://img.shields.io/badge/License-MIT-0f766e.svg)](LICENSE)
[![Labs](https://img.shields.io/badge/Labs-29-111827.svg)](#lab-catalog)
[![Focus](https://img.shields.io/badge/Focus-SOC%20%7C%20Blue%20Team-1d4ed8.svg)](#scope)
[![Status](https://img.shields.io/badge/Status-Active%20Build-374151.svg)](#roadmap)

[Overview](#overview) · [Lab Catalog](#lab-catalog) · [Architecture](docs/architecture.md) · [Evaluation](docs/evaluation.md) · [Security](SECURITY.md) · [Contributing](CONTRIBUTING.md)

</div>

---

## Overview

`genai-soc-labs` is a portfolio monorepo for 29 hands-on labs at the intersection of Generative AI and cybersecurity. The main focus is SOC engineering: incident response, threat hunting, SIEM workflows, threat intelligence, SOAR assistance, forensic timelines, and analyst enablement.

The goal is to demonstrate practical AI cybersecurity engineering, not only prompt usage. Each lab is designed to grow into a production-style web application with authentication, role-based access control, clean user experience, deployment, evaluation, and responsible security boundaries.

## Scope

This repository is organized for an AI Cybersecurity Engineer portfolio with a SOC specialization.

Core engineering themes:

- LLM-assisted investigation workflows
- Retrieval-augmented generation for security knowledge
- Log parsing, normalization, and correlation
- Analyst-facing explanations with citations and evidence
- Human approval for sensitive response actions
- Secure-by-design application scaffolding
- Evaluation for hallucination, precision, recall, and operational usefulness

## Lab Catalog

| # | Lab | Domain | Method | Track |
|---|---|---|---|---|
| 01 | [IncidentLens: AI Incident Report Assistant](labs/01-incidentlens-incident-report/) | Incident Response | FastAPI + deterministic AI-ready analysis | Implemented |
| 02 | [QueryForge: Natural Language SIEM Assistant](labs/02-queryforge-siem-assistant/) | Threat Hunting | FastAPI + text-to-query engine | Implemented |
| 03 | [ThreatPulse: AI Threat Intelligence Briefing](labs/03-threatpulse-threat-intel/) | Threat Intelligence | FastAPI + asset-aware intelligence scoring | Implemented |
| 04 | [PhishGuard: Context-Aware Phishing Detection](labs/04-phishguard-phishing-detection/) | Email Security | LLM + Classification | Backlog |
| 05 | [HardeningPilot: CIS/ISO Security Advisor](labs/05-hardeningpilot-compliance-advisor/) | Compliance & Hardening | RAG + LLM | Backlog |
| 06 | [BehaviorSentinel: UEBA Risk Detection](labs/06-behaviorsentinel-ueba/) | Insider Threat | Anomaly Detection + LLM | Backlog |
| 07 | [PlaybookOps: SOAR Response Assistant](labs/07-playbookops-soar-assistant/) | SOAR | LLM + Workflow | Flagship |
| 08 | [RiskRanker: Vulnerability Prioritization Engine](labs/08-riskranker-vulnerability-risk/) | Vulnerability Management | LLM + Analytics | Backlog |
| 09 | [MalwareLens: Static Malware Analysis Assistant](labs/09-malwarelens-static-analysis/) | Malware Analysis | LLM + Static Analysis | Backlog |
| 10 | [VendorShield: Third-Party Risk Assessor](labs/10-vendorshield-third-party-risk/) | Third-Party Risk | RAG + LLM | Backlog |
| 11 | [AwareOps: Security Awareness & Phishing Simulation](labs/11-awareops-security-awareness/) | Security Awareness | LLM + Personalization | Backlog |
| 12 | [LeakWatch: Data Leak Monitoring Assistant](labs/12-leakwatch-data-leak-monitoring/) | Data Leak Monitoring | LLM + Monitoring | Backlog |
| 13 | [NetBeacon: C2 & Exfiltration Detection](labs/13-netbeacon-c2-exfil-detection/) | Network Detection | ML + LLM | Flagship |
| 14 | [PolicyRAG: Security Policy Assistant](labs/14-policyrag-security-policy/) | Policy Management | RAG + LLM | Backlog |
| 15 | [CodeTriage: SAST Finding Assistant](labs/15-codetriage-sast-assistant/) | Application Security | LLM + Code Analysis | Backlog |
| 16 | [AuditFlow: Compliance Evidence Generator](labs/16-auditflow-evidence-reporting/) | Compliance Reporting | RAG + LLM | Backlog |
| 17 | [SurfaceMap: Attack Surface Management AI](labs/17-surfacemap-attack-surface/) | ASM | LLM + Recon | Backlog |
| 18 | [ForensicTrace: Investigation Timeline Builder](labs/18-forensictrace-timeline-builder/) | Digital Forensics | LLM + Correlation | Flagship |
| 19 | [SOCMentor: Tier-1 Analyst Assistant](labs/19-socmentor-tier1-assistant/) | SOC Assistant | RAG + LLM | Flagship |
| 20 | [CloudGuardAI: CSPM Risk Advisor](labs/20-cloudguardai-cspm/) | Cloud Security | LLM + Analytics | Backlog |
| 21 | [FraudSignal: Transaction Fraud Detection](labs/21-fraudsignal-fraud-detection/) | Fraud Detection | ML + LLM | Backlog |
| 22 | [RedReport: Defensive Red Team Reporting Assistant](labs/22-redreport-redteam-reporting/) | Offensive Security (Defensive Use) | LLM + RAG | Backlog |
| 23 | [PrivacyPilot: Vietnam PDPD Compliance Assistant](labs/23-privacypilot-pdpd-compliance/) | Data Privacy Compliance | RAG + LLM | Backlog |
| 24 | [DeepfakeShield: Synthetic Media Detection](labs/24-deepfakeshield-detection/) | Deepfake Detection | Vision/Audio + LLM | Backlog |
| 25 | [ExecBrief: Executive Security Reporting AI](labs/25-execbrief-security-brief/) | Executive Reporting | LLM + Analytics | Backlog |
| 26 | [DataSentinel: Data Classification & DLP Assistant](labs/26-datasentinel-dlp-classification/) | Data Protection | LLM + Classification | Backlog |
| 27 | [BreachSim: Defensive Attack Simulation Planner](labs/27-breachsim-defense-validation/) | Breach Simulation | LLM + RAG | Backlog |
| 28 | [AccessMind: IAM Governance Reviewer](labs/28-accessmind-iam-governance/) | Identity Governance | LLM + Analytics | Backlog |
| 29 | [IoTWatch: IoT/OT Security Monitoring AI](labs/29-iotwatch-iot-ot-security/) | IoT/OT Security | ML + LLM | Backlog |

## Repository Structure

```text
genai-soc-labs/
  README.md
  CONTRIBUTING.md
  LICENSE
  SECURITY.md
  CODE_OF_CONDUCT.md
  docs/
    architecture.md
    evaluation.md
    roadmap.md
    security-and-ethics.md
    source-briefs.tsv
  labs/
    01-incidentlens-incident-report/
      README.md
    02-queryforge-siem-assistant/
      README.md
    ...
    29-iotwatch-iot-ot-security/
      README.md
  shared/
    README.md
  .github/
    ISSUE_TEMPLATE/
    PULL_REQUEST_TEMPLATE.md
```

## Implementation Standard

Every completed lab should meet the same minimum bar:

- Full web application, not a notebook-only or CLI-only prototype
- Deployed online with a public demo URL when safe to expose
- Authentication and basic role-based access control
- Clear UI/UX for analyst workflows
- Sample data or synthetic datasets suitable for public release
- Documented architecture and security assumptions
- Evaluation notes for model quality and operational risk
- Responsible-use boundaries for defensive security only

## Roadmap

The flagship SOC labs are prioritized first:

1. IncidentLens: AI Incident Report Assistant
2. QueryForge: Natural Language SIEM Assistant
3. ThreatPulse: AI Threat Intelligence Briefing
4. PlaybookOps: SOAR Response Assistant
5. NetBeacon: C2 & Exfiltration Detection
6. ForensicTrace: Investigation Timeline Builder
7. SOCMentor: Tier-1 Analyst Assistant

See [docs/roadmap.md](docs/roadmap.md) for the full plan.

## Responsible Use

These labs are intended for defensive security, education, and authorized enterprise security workflows. They avoid exploit generation, malware creation, credential abuse, or unauthorized reconnaissance. See [docs/security-and-ethics.md](docs/security-and-ethics.md) and [SECURITY.md](SECURITY.md).

## License

Released under the [MIT License](LICENSE).
