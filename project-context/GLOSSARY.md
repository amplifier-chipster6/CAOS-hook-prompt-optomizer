# Glossary

## Core Terms (use exactly)

- **UserPromptSubmit**: The Amplifier hook event that fires on every user prompt submission. Registered in hooks.json under the "hooks" key. Our global hook matches with "matcher": "*".

- **contextInjection** (or contextInjection): The JSON field returned by shell-hooks to inject structured guidance into the agent context without modifying the user's original prompt. Must be used instead of native Core fields unless verified otherwise. Our optimizer always pairs it with "decision": "approve".

- **shell-hook**: Project-local or global mechanism using .amplifier/hooks/hooks.json + executable commands (Python in our case). Supports ${AMPLIFIER_HOOKS_DIR} variable. Global version lives in ~/.amplifier/hooks/ and applies everywhere.

- **fail-open**: Critical safety property of the prompt optimizer. On any error, large prompt, should_skip match, or exception, the hook returns {"decision": "approve"} with minimal or no contextInjection so prompt submission is never blocked.

- **prompt optimizer** / **global prompt optimizer hook**: The artifact built in this project. Consists of prompt_optimizer.py (classification + guidance builder) and hooks.json. Provides task-specific response guidance (debugging flow, coding completeness, etc.) while preserving user intent.

- **should_skip()**: Function in prompt_optimizer.py that detects phrases like "do not optimize", "as is", "verbatim" to bypass injection and respect explicit user intent.

- **classify_task()**: Keyword-based deterministic classifier returning one of: debugging, system_design, research_validation, writing, coding, analysis, general. Used to tailor the injected guidance.

- **build_optimization_context()**: Core function that assembles the markdown guidance (core rules + task-specific best practices) without ever duplicating or referencing the specific user prompt content.

- **one-line-installer-patterns**: Skill used implicitly for the global deployment installer script (/tmp/global-prompt-optimizer.sh) to handle write restrictions on ~/.amplifier/.

- **per-repo-conventions**: Skill/pattern for discovering AGENTS.md, project-context/* before making changes. This repo follows it by maintaining coordination files.

## Terms from Parent Prompt
- Project-local hook, global hook, amplifier-module-hook-shell, decision/contextInjection JSON shape, verbatim drawers (in curator context).

See PROVENANCE.md for decision rationale and memories for full implementation details. All terms preserved exactly as used in the conversation and code.