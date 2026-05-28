# Reversibility Plan: Global Hooks and Context Injection

## Purpose

This plan preserves the prompt optimizer experiment as a reference artifact, then returns the live Amplifier environment toward its original pre-experiment state by removing or disabling global hook and context-injection layers in controlled steps.

The goal is not to erase the learning. The goal is to make the system reversible while keeping the repository, provenance notes, and failure history available for recursive meta-cognitive amplification.

## Scope

This plan covers live global state outside this repository:

- `~/.amplifier/hooks/hooks.json`
- `~/.amplifier/hooks/prompt_optimizer.py`
- `~/.amplifier/settings.yaml` entries that activate global memory/context hooks

It also covers repository documentation updates needed before syncing to GitHub.

This plan does not remove normal Amplifier system/developer instructions, bundle context loaded by the active bundle, or conversation history already present in an existing session.

## Current live global influence layers

### 1. Global shell hook

File:

```text
~/.amplifier/hooks/hooks.json
```

Current behavior:

- Registers a `UserPromptSubmit` hook with `matcher: "*"`.
- Runs `python3 ${AMPLIFIER_HOOKS_DIR}/prompt_optimizer.py`.
- Applies in every project/directory where global hooks are loaded.

### 2. Global prompt optimizer script

File:

```text
~/.amplifier/hooks/prompt_optimizer.py
```

Current behavior:

- Classifies prompts using keyword matching.
- Uses `should_skip()` for bypass phrases such as `do not optimize`.
- Emits `contextInjection` for normal prompts.
- Emits reduced `contextInjection` for large prompts.
- Fails open with `{"decision": "approve"}` on errors.

Known direct bypass test:

```bash
echo '{"prompt":"do not optimize, explain X"}' | python3 ~/.amplifier/hooks/prompt_optimizer.py
```

Expected output:

```json
{"decision": "approve"}
```

### 3. Global native memory/context hooks

File:

```text
~/.amplifier/settings.yaml
```

Relevant entries currently observed:

```yaml
modules:
  contexts:
  - module: context-amplifier-module-context-memory
  - module: context-memory
  - module: context-managed
  - context-mempalace
  hooks:
  - hooks-project-context
  - hooks-mempalace-capture
  - hooks-mempalace-briefing
  - module: hooks-memory-capture
  - module: hooks-memory
```

These are separate from the shell `contextInjection` hook. Removing `prompt_optimizer.py` injection does not automatically disable these memory/project-context layers.

## Definition of original state

Because the exact pre-experiment global config may not be fully known, define two restoration levels.

### Level 1: No global prompt optimizer injection

- `~/.amplifier/hooks/hooks.json` no longer registers the prompt optimizer, or
- `~/.amplifier/hooks/prompt_optimizer.py` always returns `{"decision": "approve"}` without `contextInjection`.

This removes the global `UserPromptSubmit` prompt optimization layer.

### Level 2: No global memory/project-context hook influence

In addition to Level 1:

- Remove globally added memory/context hooks from `~/.amplifier/settings.yaml`.
- Remove globally added memory/context modules if they were introduced only for this experiment.

This reduces automatic session-start/session-end memory/project-context influence.

### Level 3: Clean-room live environment

In addition to Level 2:

- Start a fresh session after config changes.
- Confirm no prompt optimizer guidance appears.
- Confirm no memory/project-context hook reminders appear unless loaded by the active bundle itself.
- Use a minimal bundle/profile if needed for true baseline comparison.

## Reversal principles

1. Preserve first, remove second.
2. Back up every global file before editing it.
3. Prefer disabling over deleting until validation passes.
4. Validate each layer independently.
5. Record failures and rollback points in this repository.
6. Do not confuse shell `contextInjection` with native context, system messages, mode reminders, or already-injected conversation history.

## Phase 1: Preserve repository state

Before changing global config, ensure the repository contains:

- README summary of the experiment and reversibility goal.
- `project-context/PROVENANCE.md` ADRs.
- `project-context/WAYSOFWORKING.md` failure patterns and verification commands.
- `project-context/HANDOFF.md` current next steps.
- This reversibility plan.

Then commit and push the repository using the normal git workflow.

Git operations should be handled by the git operations specialist or normal repository process, not mixed with global config edits.

## Phase 2: Back up global state

Create a timestamped backup directory:

```bash
BACKUP_DIR="$HOME/.amplifier/backups/reversibility-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

cp ~/.amplifier/hooks/hooks.json "$BACKUP_DIR/hooks.json.bak" 2>/dev/null || true
cp ~/.amplifier/hooks/prompt_optimizer.py "$BACKUP_DIR/prompt_optimizer.py.bak" 2>/dev/null || true
cp ~/.amplifier/settings.yaml "$BACKUP_DIR/settings.yaml.bak" 2>/dev/null || true

printf 'Backup written to %s\n' "$BACKUP_DIR"
```

Record the backup path in `project-context/HANDOFF.md` or an experiment note before proceeding.

## Phase 3: Disable global prompt optimizer shell hook

Recommended first action: disable registration, do not delete files yet.

### Option A: Remove `UserPromptSubmit` registration

Edit:

```text
~/.amplifier/hooks/hooks.json
```

Change it to an empty hook set if the prompt optimizer is the only hook:

```json
{
  "description": "Global hooks disabled during reversibility rollback",
  "hooks": {}
}
```

Validate JSON:

```bash
python3 -m json.tool ~/.amplifier/hooks/hooks.json >/dev/null
```

### Option B: Keep registration but force approve-only

If you need the command hook to remain present, edit `~/.amplifier/hooks/prompt_optimizer.py` so `main()` consumes stdin and always returns:

```json
{"decision": "approve"}
```

This keeps the protocol valid while removing all `contextInjection` behavior.

Validation command:

```bash
echo '{"prompt":"explain X"}' | python3 ~/.amplifier/hooks/prompt_optimizer.py
```

Expected output:

```json
{"decision": "approve"}
```

## Phase 4: Verify shell `contextInjection` is gone

Search global hooks:

```bash
grep -RIn "contextInjection\|Prompt Optimization Guidance\|Enhanced Response Guidance" ~/.amplifier/hooks/ || true
```

If Option A was used, direct script output may still inject when called manually, but the global hook should no longer call it. If Option B was used, the script itself should no longer emit injection.

Start a fresh Amplifier session and ask a normal prompt:

```text
explain X
```

Expected absence:

- no `# Prompt Optimization Guidance`
- no `# Enhanced Response Guidance`
- no `Task type detected:`
- no `Apply this guidance to the current user request`
- no `Make your response easy for the curator...` from the prompt optimizer

## Phase 5: Disable global native memory/context hooks if desired

Only do this after Level 1 is validated.

Edit:

```text
~/.amplifier/settings.yaml
```

Remove or comment through a controlled YAML edit the entries that were globally added for the memory hook experiment.

Observed candidates:

```yaml
modules:
  contexts:
  - module: context-amplifier-module-context-memory
  - module: context-memory
  - module: context-managed
  - context-mempalace
  hooks:
  - hooks-project-context
  - hooks-mempalace-capture
  - hooks-mempalace-briefing
  - module: hooks-memory-capture
  - module: hooks-memory
```

Do not remove providers, routing, tools, or bundle registrations unless separately confirmed to be part of the rollback.

Validation:

```bash
python3 - <<'PY'
import yaml
from pathlib import Path
path = Path.home() / '.amplifier' / 'settings.yaml'
with path.open() as f:
    data = yaml.safe_load(f)
print('YAML OK')
print(data.get('modules', {}).get('hooks', []))
print(data.get('modules', {}).get('contexts', []))
PY
```

Then start a fresh session and confirm memory/project-context hook reminders are absent unless supplied by the active bundle itself.

## Phase 6: Separate unavoidable context from reversible context

Even after global hooks are removed, some guidance may remain because it is not from the prompt optimizer:

| Source | Removed by disabling prompt optimizer? |
|---|---:|
| Global `prompt_optimizer.py` `contextInjection` | Yes |
| Global memory hooks in `settings.yaml` | No, separate step |
| Active bundle context files | No |
| System/developer messages from runtime | No |
| Skills visibility | No |
| Mode reminders | No |
| Existing conversation history | No |

Use fresh sessions for validation. Existing sessions may contain prior injected guidance in their transcript history.

## Phase 7: Rollback procedure

If disabling breaks desired behavior, restore from the backup directory:

```bash
cp "$BACKUP_DIR/hooks.json.bak" ~/.amplifier/hooks/hooks.json
cp "$BACKUP_DIR/prompt_optimizer.py.bak" ~/.amplifier/hooks/prompt_optimizer.py
cp "$BACKUP_DIR/settings.yaml.bak" ~/.amplifier/settings.yaml
```

Validate:

```bash
python3 -m json.tool ~/.amplifier/hooks/hooks.json >/dev/null
python3 -m py_compile ~/.amplifier/hooks/prompt_optimizer.py
python3 - <<'PY'
import yaml
from pathlib import Path
yaml.safe_load((Path.home() / '.amplifier' / 'settings.yaml').read_text())
print('settings YAML OK')
PY
```

## Phase 8: Document the reversal outcome

After each phase, update:

- `project-context/HANDOFF.md` with what changed and what remains.
- `project-context/PROVENANCE.md` if a durable architecture decision was made.
- `project-context/WAYSOFWORKING.md` with any failure pattern or command that worked.

If an attempted reversal fails, record:

- exact command,
- observed output,
- expected output,
- suspected source of remaining guidance,
- final resolution.

## Success criteria

Level 1 success:

- Fresh session does not receive prompt optimizer guidance for ordinary prompts.
- Global shell hook either has no `UserPromptSubmit` registration or emits no `contextInjection`.
- Repository records the rollback plan and backup path.

Level 2 success:

- Fresh session does not receive memory/project-context hook reminders from global settings.
- `~/.amplifier/settings.yaml` no longer globally loads the rollback-targeted memory hooks/contexts.

Level 3 success:

- Clean-room session behavior is explainable only by active bundle/system context and user messages.
- There is a documented command path to re-enable the removed hooks if desired.

## Known risks

- Disabling memory hooks may reduce continuity and curator capture.
- Removing settings entries manually can break YAML or remove unrelated functionality.
- Existing sessions can preserve old injected context even after live hooks are disabled.
- Project-local hooks may still run inside this repository if local hook loading takes precedence.
- The exact original global state may be unknown unless a pre-experiment backup exists.

## Recommended order

1. Commit and push repository documentation first.
2. Back up global files.
3. Disable global shell prompt optimizer registration.
4. Validate fresh session behavior.
5. Only then remove global memory/context hooks if clean-room behavior is required.
6. Document final state and rollback instructions.
