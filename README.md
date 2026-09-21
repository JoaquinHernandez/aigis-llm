# aigis-llm
# Aegis LLM 🛡️

A defensive, enterprise-grade Cybersecurity LLM platform. AegisLLM acts as a high-speed orchestrator for SOC triage, vulnerability management, and incident response runbooks, utilizing local RAG and multi-agent tool execution.

## 🚀 Features
*   **Automated Alert Triage:** Ingests alerts from Splunk, Elastic, and Sentinel, mapping behaviors directly to MITRE ATT&CK.
*   **Decoupled Tooling:** Uses FastMCP to orchestrate integrations with ServiceNow, VirusTotal, and internal ticketing systems safely.
*   **Local, Private AI:** Configured to run entirely air-gapped. Tuned for vLLM inference on local high-performance GPUs (optimized for RTX 5090 environments).
*   **Secure by Design:** Built-in prompt injection defenses, PII redaction, and strict RBAC via Keycloak.

## 🛠️ Tech Stack
*   **Backend:** Python, FastAPI, LangGraph, pgvector, SQLAlchemy.
*   **Frontend:** React, Vite, Tailwind CSS, shadcn/ui.
*   **Integrations:** FastMCP (Model Context Protocol).
*   **Deployment:** Docker, Kubernetes (Helm).

## 🏁 Quickstart

1. **Clone & Configure:**
   ```bash
   git clone [https://github.com/yourusername/aegis-llm.git](https://github.com/yourusername/aegis-llm.git)
   cd aegis-llm
   cp .env.example .env # Configure your API keys and Keycloak credentials
