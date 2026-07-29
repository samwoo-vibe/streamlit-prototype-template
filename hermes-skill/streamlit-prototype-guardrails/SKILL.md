---
name: streamlit-prototype-guardrails
description: "Use when creating, changing, reviewing, or debugging a Samwoo employee Streamlit prototype. Enforce framework isolation, portable SQLAlchemy persistence, Pydantic boundaries, secret handling, and tests so approved prototypes can be migrated to FastAPI and PostgreSQL."
license: Proprietary
metadata:
  hermes:
    tags: [streamlit, prototype, citizen-development, python, migration]
    related_skills: [test-driven-development]
---

# Samwoo Streamlit Prototype Guardrails

## Overview

Keep employee prototypes simple to run with uv while preserving code that can later move to
FastAPI and PostgreSQL. Treat Streamlit as a replaceable presentation layer, not the application.

## Required First Step

Read the repository-root `AGENTS.md` completely before inspecting or changing code. If it is
missing, stop and ask for the current Samwoo template rules. Repository rules are the source of
truth when they are stricter than this skill.

Completion criterion: summarize the active rules and requested behavior before editing.

## Architecture Boundary

Use these ownership rules:

| Location | Owns | Must not own |
|---|---|---|
| `app.py`, `pages/` | Streamlit widgets, layout, user messages | SQL, business rules |
| `schemas/` | Pydantic input/output contracts | UI or persistence |
| `services/` | Validation and business rules | Streamlit or SQLAlchemy sessions |
| `repositories/` | Query and persistence operations | UI decisions |
| `models.py` | SQLAlchemy portable table mappings | SQLite-only behavior |

Never import `streamlit` under `src/`. Never open a SQLAlchemy session from `app.py` or `pages/`.
Pass repository objects to service functions. Keep important state in the database rather than
only in `st.session_state`.

Completion criterion: each changed behavior has one clear owner and the source scan finds no
Streamlit imports under `src/`.

## Implementation Workflow

1. Restate the requested workflow, users, inputs, outputs, and failure cases. Ask about missing
   business decisions instead of inventing them.
2. Define or update Pydantic schemas.
3. Add a failing pytest test for the business behavior.
4. Implement the smallest framework-independent service change.
5. Add or update SQLAlchemy models and repository methods only when persistence is required.
6. Connect the service to the Streamlit page last.
7. Run all verification commands.

Completion criterion: the behavior works through the page, while its core result is testable
without starting Streamlit or a real database server.

## Data Portability

- Use `DATABASE_URL`; default only to `sqlite:///./data/prototype.db`.
- Use SQLAlchemy ORM and portable column types.
- Do not use SQLite `PRAGMA`, SQLite-specific functions, or raw SQL without explicit approval.
- Do not treat a local DB file as source code.
- Use fake/in-memory repositories for service unit tests when practical.
- Do not connect prototypes to Coolify, Hermes production services, or company production DBs.

Completion criterion: deleting the local DB creates a clean prototype DB on next start, and no DB
file is tracked by Git.

## Security Boundary

- Never place passwords, tokens, keys, connection secrets, personal data, or actual company data
  in source, examples, logs, screenshots, or tests.
- Commit `.env.example`, never `.env`.
- Do not implement public deployment from this prototype template.
- Warn the user before adding collection of personal or sensitive information.

Completion criterion: inspect the changed diff and confirm it contains no secret or real data.

## Verification

Run from the repository root:

```bash
uv sync
uv run ruff check .
uv run pytest
```

Also verify:

```bash
rg -n "import streamlit|from streamlit" src
git status --short
```

Start the app when the change affects the UI:

```bash
uv run streamlit run app.py
```

Do not claim completion if a required check was skipped or failed. Report the exact skipped check
and reason.

## Common Pitfalls

1. **Putting everything below a button.** Move validation and processing into a service.
2. **Using DataFrames as implicit contracts.** Define Pydantic records at module boundaries.
3. **Hiding workflow state in `session_state`.** Persist durable state through a repository.
4. **Optimizing for SQLite.** Use portable SQLAlchemy constructs that PostgreSQL can support.
5. **Adding FastAPI or Node.js.** Keep the employee prototype uv-only; migration is a later,
   separately approved project.
6. **Calling a prototype production-ready.** Record unresolved authentication, authorization,
   concurrency, audit, migration, and operational requirements.

## Final Checklist

- [ ] Root `AGENTS.md` was read and followed
- [ ] Streamlit exists only in presentation files
- [ ] Business logic is covered by tests
- [ ] DB access is behind repositories
- [ ] Pydantic models define relevant boundaries
- [ ] No SQLite-specific behavior was introduced
- [ ] No secrets or real company data are tracked
- [ ] `uv sync`, Ruff, and pytest pass
- [ ] UI-affecting changes were smoke-tested
