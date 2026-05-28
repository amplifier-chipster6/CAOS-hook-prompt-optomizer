# Architecture Decision Records & Provenance

## Decision: Implement as Amplifier Shell-Hook (not full bundle or module)
**Date:** 2026-05-23
**Context:** Original user prompt required strict adherence to project-local .amplifier/hooks/ implementation using existing shell-hook mechanism. No new bundles, no fat bundles, no new repos, preserve current structure.
**Alternatives Considered:**
- Full Amplifier module (violates "no bundle" constraint)
- Behavior or context provider (more native but would require config changes)
- Pure project-local only (rejected by user after initial implementation)
**Decision:** Used .amplifier/hooks/hooks.json with command hook + global ~/.amplifier/hooks/ fallback via installer script. This respects all constraints while achieving desired global behavior.
**Rationale:** Shell-hook system (amplifier-module-hook-shell) supports JSON decision+contextInjection response exactly as specified. Global install via ~/.amplifier/hooks/ is the documented way to achieve cross-project availability without bundles.
**Status:** Implemented and verified globally active.

## Decision: Keyword-based classification + fail-open design
**Date:** 2026-05-23
**Context:** Hook must be deterministic, lightweight (<5s timeout), never block prompt submission.
**Rationale:** Keyword lists in classify_task() ensure O(1) performance, no LLM dependency. should_skip() respects explicit user bypass requests. All paths return {"decision": "approve"}. Large prompt fallback and full exception handling ensure robustness.
**Consequences:** Fast and reliable. Future enhancement path exists via skills system for smarter classification without breaking determinism.

## Decision: Context injection only, no prompt rewriting
**Date:** 2026-05-23
**Context:** User prompt must remain authoritative.
**Rationale:** build_optimization_context() generates guidance metadata only, explicitly stating "The user's original message is authoritative. Do not change, replace, or reinterpret their core intent." No duplication of user content in injection.
**Status:** Fully compliant.

## Evolution to Global Deployment
Initial local implementation in repo's .amplifier/hooks/ was expanded to global ~/.amplifier/hooks/ after user stated "i dont want project specific i want global". Installer script pattern used to handle write restrictions (see one-line-installer-patterns skill). Fixed heredoc/quoting bug in JSON.

**Related memories:** See memories with IDs f74a72a6-6955-4794-a09c-b6884aa5c3c0, e2407a9d-3eab-4482-b3c1-6ad438c456f7, f161cbe9-7532-4a95-9267-19c9dc27e5b1 (high importance foundational workflow improvement).

**Next:** Consider skillifying the hook creation process itself.

## Decision: Evolve Prompt Optimizer to be Memory-System Aware
**Date:** 2026-05-23
**Context:** After enabling global memory hooks (context-managed, hooks-mempalace-*, hooks-project-context) in ~/.amplifier/settings.yaml, the prompt_optimizer.py guidance needed updating to leverage them for better outputs.
**Alternatives Considered:**
- Leave guidance generic (missed opportunity for coherence).
- Use LLM for classification in hook (violates lightweight/deterministic requirement).
- Move logic into native context provider (would require bundle changes, violating original constraints).
**Decision:** Updated only the `build_optimization_context()` function with verbatim references to active hooks, explicit instructions to read coordination files, use palace tools, cite memories, and produce curator-friendly structured output. Classification, should_skip, fail-open JSON shape, and all safety properties left unchanged.
**Rationale:** Creates virtuous cycle: memory-aware guidance → better structured agent responses → richer verbatim captures for curator Phase 1 (categorization into decision/architecture/pattern/lesson_learned + importance scoring) → higher quality drawers/KG facts → better future briefings via hooks-mempalace-briefing. Fully preserves original critical constraints (no bundles, contextInjection only, user prompt authoritative, deterministic <5s Python).
**Status:** Complete. Now part of the definitive global system. Cross-referenced in memories dae720b1-95e7-4274-ba0f-00652cdc9d01, dbd5e8d2-0b54-4615-a615-1bf8637648ea, f78d067c-14ce-422a-824f-1eef86a0c8de and this HANDOFF.md update.
**Consequences:** Every future prompt submission benefits from memory coherence and curator optimization. This repo's project-context/ now contains the complete provenance.

## Decision: Prioritize Reversibility and Source Attribution
**Date:** 2026-05-25
**Context:** Follow-up sessions showed that the global prompt optimizer and memory-aware guidance worked technically, but created confusion about which layer influenced responses. Direct testing confirmed `do not optimize` bypasses `~/.amplifier/hooks/prompt_optimizer.py` for exact matches, but that only bypasses the shell hook. It does not remove other global memory hooks, project-context hooks, active bundle context, prior transcript context, or runtime developer/system messages.
**Alternatives Considered:**
- Keep global hooks as permanent default (rejected because the user needs reversible cognitive infrastructure, not hidden steering).
- Delete global files immediately (rejected because it risks losing reproducibility and failure history before syncing to GitHub).
- Preserve repo first, then remove global influence layers in phases (selected).
**Decision:** Treat reversibility as the next milestone. Preserve the repository, update documentation, sync GitHub, then remove or disable global `contextInjection` and optional memory/project-context hooks using a backed-up, validated rollback plan.
**Rationale:** Recursive meta-cognitive amplification requires remembering both successes and failures. The system must preserve the experiment as a learning artifact while allowing the live environment to return to an explainable baseline.
**Status:** Plan documented in `docs/REVERSIBILITY_PLAN.md`. Repository documentation updated. Live global files have not yet been changed by this decision.
**Consequences:** Future hook/context systems should include source attribution, explicit kill switches, bypass levels, and rollback commands from the beginning.