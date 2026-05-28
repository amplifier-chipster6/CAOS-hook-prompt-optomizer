# Project Context

**Phase:** Reversibility / Rollback Planning
**Milestone:** v1.1.0 — Preserve local reference state, sync GitHub, then remove global hook/context-injection layers
**Active work:** Document reversibility, preserve failure history, and prepare a controlled rollback from global prompt/context influence to an explainable baseline

## Team
| Person | Role |
|--------|------|
| User | Product Owner / Requirements |
| Amplifier (Curator) | Memory specialist, coordination file maintainer |

## Recent Milestones
- 2026-05-23 — Initial project-local hook created per strict constraints (prompt_optimizer.py + hooks.json)
- 2026-05-23 — Pivot to global deployment via installer script after user requested universal availability
- 2026-05-23 — Memory curator session: 3 high-importance memories added (IDs f74a72a6..., e2407a9d..., f161cbe9...), PROVENANCE.md, updated HANDOFF.md, GLOSSARY.md, WAYSOFWORKING.md. All technical details, decisions, evolution, and lessons captured verbatim.

**Status:** Reversibility is now the main concern. The global hook worked technically, including direct `do not optimize` bypass testing, but the broader system created authority/source-attribution confusion around `contextInjection`, memory-aware guidance, project-context loading, and other global context layers. Current priority is to commit/push the repo as the durable learning artifact before changing live global files.

## Current rollback target

1. Preserve this repo and documentation in GitHub.
2. Back up global live files under `~/.amplifier/`.
3. Disable global shell-hook `contextInjection` from `~/.amplifier/hooks/`.
4. Optionally disable global memory/project-context hooks from `~/.amplifier/settings.yaml` if clean-room behavior is required.
5. Validate in a fresh session and document the resulting baseline.

This file is kept up-to-date per per-repo-conventions and AGENTS.md.