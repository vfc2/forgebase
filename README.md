<p align="center">
	<img src="https://upload.wikimedia.org/wikipedia/commons/9/96/Microsoft_logo_%282012%29.svg" alt="Microsoft Logo" width="160" />
</p>

<h1 align="center">Forgebase</h1>
<p align="center"><strong>Global Hackathon 2025 – Microsoft ISD</strong></p>
<p align="center">Accelerating the path from idea to execution with AI‑guided, structured requirements generation.</p>

---

> [!IMPORTANT]  
> Forgebase is an independent initiative and is not an official Microsoft product or offering. Forgebase is not affiliated with or endorsed by Microsoft.

## Problem & Opportunity
### The challenge
Gathering project requirements is one of the most fragmented, delay‑prone stages of delivery. Inputs arrive through emails, decks, meetings and ad‑hoc chats; critical questions are missed, assumptions go unvalidated, and gaps only surface downstream as risk, rework, or stalled delivery.

### The opportunity
Microsoft ISD needs a faster, safer way to turn early project discussions into requirements that are structured, complete, and ready for execution.

## Solution Summary
Forgebase automates requirements capture through a guided, conversational AI experience. It leverages institutional knowledge and proven delivery patterns to surface missing context, reduce ambiguity, and transform dialogue into an execution‑ready backlog (Epics, Features, User Stories). Instead of static documents, it produces living, structured artifacts designed to flow directly into Azure DevOps (export pipeline in progress).

### Business Impact
* Cut requirements definition from weeks to hours.
* Improve quality & completeness by embedding return‑of‑experience.
* Accelerate kick‑off with Agile‑ready backlogs.
* Reduce delivery risk via standardized capture and translation.

### Target Users
Program managers, delivery leads, product owners, and cross‑functional teams seeking consistent, high‑velocity project initiation.

## Key Capabilities (Current)
| Category | Capability |
|----------|------------|
| Conversation | Streaming AI chat with context persistence |
| Requirements | AI‑assisted PRD generation & iterative refinement |
| PRD View | Live Markdown rendering & version updates |
| Project Mgmt | Create / update lightweight project records with PRD field |
| Tooling | Agent tool to persist PRD updates during conversation |
| Quality | 90+ automated backend tests; typed services & domain isolation |

### In Progress / Planned
* Structured backlog synthesis (Epics ➜ Features ➜ User Stories)
* Azure DevOps export (work item creation pipeline)
* Requirements completeness scoring & gap prompts
* Reuse of pattern library / delivery accelerators
* Multi‑user identity & secure tenancy

## How It Works (Architecture Overview)
Forgebase uses a clean, service‑oriented, port & adapter architecture:
1. Frontend (React + Vite) provides chat + PRD views.
2. Backend (FastAPI) exposes project & chat endpoints with streaming responses.
3. ChatService orchestrates AI interactions and delegates structured updates to tools.
4. An agent tool (`update_prd`) persists evolving PRD content to the project store.
5. Domain entities enforce invariants; repository layer abstracts persistence (currently in‑memory / simple store, pluggable later).
6. Output is rendered as live Markdown; future pipeline will map structured artifacts to Azure DevOps work items.

## Technology Stack
| Layer | Technologies |
|-------|--------------|
| Frontend | React, TypeScript, Mantine UI, Vite, Vitest |
| Backend | FastAPI, Python 3.12, Semantic Kernel (agent orchestration) |
| Streaming | Server-Sent Events (SSE) |
| Quality | pytest, mypy, pylint, black |
| Tooling | Agent tool pattern via ports & adapters |

## Quick Start
```bash
# Clone & enter repo (assumes Python 3.12 & Node 18+ available)

# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.sample .env  # fill in Azure OpenAI values if needed
PYTHONPATH=src python src/forgebase/interfaces/web.py  # http://localhost:8000

# Frontend (new terminal)
cd ../frontend
npm install
npm run dev  # http://localhost:5173

# (Optional) run both from repo root
./start_dev.sh
```

## Project Structure (High-Level)
```
backend/
	src/forgebase/
		core/         # Domain services & entities
		infrastructure/ # Agent + config implementations
		interfaces/   # API & CLI adapters
		tools/        # AI tool implementations
frontend/
	src/
		components/   # UI + chat + PRD views
		hooks/        # Domain-aware React hooks
		services/     # API client
		types/        # Shared typings
```

## Development & Quality Gates
```bash
# Backend
cd backend && source .venv/bin/activate
python -m black src tests && python -m pylint src tests && python -m mypy src && pytest -q

# Frontend
cd frontend
npm run test -- --run && npm run build
```

## Roadmap Snapshot
| Phase | Focus |
|-------|-------|
| Now | PRD generation + refinement loop |
| Next | Backlog structuring & export mapping |
| Then | Pattern library integration & risk scoring |

## Status & Disclaimer
This is a Global Hackathon 2025 prototype. Some described features (e.g., Azure DevOps export, full backlog synthesis) are under active development. Not for production use without security, identity, and persistence hardening.

## License
BSD 3-Clause License (see `LICENSE`).

---
Questions or ideas? Open an issue or drop a suggestion in the Hackathon channel.
