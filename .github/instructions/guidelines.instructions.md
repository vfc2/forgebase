---
applyTo: "**"
---
# Project Overview

This project is an ultra-minimal, async, transport-agnostic chat boundary that streams LLM replies using **Semantic Kernel**’s `ChatCompletionAgent.invoke_stream(...)`. It ships with a CLI for development/testing and a clean seam for a future web app. Built with **Python 3.12** and **no business logic**.

## Folder Structure

* `/src/forgebase`: Contains the source code (core, infrastructure, interfaces, prompts).
* `/tests`: Contains unit tests (pytest) covering streaming, CLI behavior, and service orchestration.
* `/.github/instructions`: Contains project instructions and maintenance guidelines.

## Libraries and Frameworks

* `semantic-kernel` for LLM chat via `ChatCompletionAgent` (streaming).
* Python stdlib `asyncio` and `logging` for streaming and diagnostics.
* Tooling: `pytest` for tests, `black` for formatting, `pylint` for linting, `mypy` for type checking.

## Coding Standards

* Google-style docstrings for every module, class, and function.
* Full type hints; async-first design (`AsyncIterator[str]` for streaming).
* Format with **Black**; **Pylint** and **mypy** must be clean (0 warnings).
* No dynamic imports; no I/O in `core/`; never log secrets.

The following must run without any error before any change can be Committed:

```bash
python -m black src tests && python -m pylint src && python -m mypy src && python -m pytest tests
```

## UI guidelines

* CLI must print streamed chunks immediately and add a final newline when the stream completes.
* Future web clients should stream via SSE or WebSocket and maintain a simple, clean UX.