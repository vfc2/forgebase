---
applyTo: "**"
---
# Project Overview

Forgebase is a simple MVP that lets a user chat with an agent to produce a Product Requirements Document (PRD) and scope the required work. It’s designed to be interface agnostic and can be used from a GUI, a web-app or any frontend.

**Goal:** Guide a conversational workflow that turns raw dialogue into a structured PRD and a scoped plan of work (e.g., sections, assumptions, constraints, and—later—high-level epics/stories).

## Folder Structure

* `/src/forgebase`: Contains the source code (core, infrastructure, interfaces, prompts).
* `/src/forgebase/web`: The web app front-end. 
* `/tests`: Contains unit tests (pytest) covering streaming, CLI behavior, and service orchestration.
* `/.github/instructions`: Contains project instructions and maintenance guidelines.

## Libraries and Frameworks

* `semantic-kernel` for LLM chat via `ChatCompletionAgent` (streaming).
* Python stdlib `asyncio` and `logging` for streaming and diagnostics.
* Tooling: `pytest` for tests, `black` for formatting, `pylint` for linting, `mypy` for type checking.
* You must ask before adding any external libraries or dependencies.

## Coding Standards

* Always favour simplicity and minimise side-effects at all cost.
* Google-style docstrings for every module, class, and function.
* Full type hints; async-first design (`AsyncIterator[str]` for streaming).
* Format with **Black**; **Pylint** and **mypy** must be clean (0 warnings).
* No dynamic imports; no I/O in `core/`; never log secrets.

**The following must run without any error after any change:**

```bash
python -m black src tests && python -m pylint src tests && python -m mypy src && python -m pytest tests
```

## UI guidelines

* CLI must print streamed chunks immediately and add a final newline when the stream completes.
* Future web clients should stream via SSE or WebSocket and maintain a simple, clean UX.