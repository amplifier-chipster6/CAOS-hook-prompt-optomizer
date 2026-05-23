#!/usr/bin/env python3
import json
import sys

MAX_PROMPT_CHARS = 15000

def classify_task(prompt: str) -> str:
    """Task classification for tailored response guidance."""
    p = prompt.lower()
    if any(kw in p for kw in [
        "debug", "error", "traceback", "bug", "fix", "crash",
        "issue", "broken", "not working", "failing"
    ]):
        return "debugging"
    if any(kw in p for kw in [
        "architecture", "design", "system", "workflow", "pipeline",
        "structure", "strategy", "plan", "high level"
    ]):
        return "system_design"
    if any(kw in p for kw in [
        "research", "verify", "validate", "source", "fact",
        "official", "citation", "documentation", "check", "confirm"
    ]):
        return "research_validation"
    if any(kw in p for kw in [
        "write", "draft", "rewrite", "summarize", "email", "blog",
        "report", "content", "article", "readme"
    ]):
        return "writing"
    if any(kw in p for kw in [
        "code", "script", "function", "class", "test", "refactor",
        "implement", "api", "repo", "program", "build"
    ]):
        return "coding"
    if any(kw in p for kw in [
        "analyze", "compare", "evaluate", "pros cons",
        "decision", "review", "tradeoff"
    ]):
        return "analysis"
    return "general"

def should_skip(prompt: str) -> bool:
    """Respect user intent to bypass optimization."""
    p = prompt.lower()
    skip_markers = [
        "do not rewrite",
        "do not optimize",
        "verbatim",
        "exactly as written",
        "raw prompt",
        "prompt injection test",
        "ignore optimizer",
        "no optimization",
        "do not enhance",
        "keep original",
        "as is",
        "literal"
    ]
    return any(marker in p for marker in skip_markers)

def build_optimization_context(prompt: str) -> str:
    """High-quality response guidance without duplicating user prompt."""
    task_type = classify_task(prompt)
    return f"""# Prompt Optimization Guidance
Task type detected: {task_type}
The user's original message is authoritative. Do not change, replace, or reinterpret their core intent.
Core response rules:
- Reason carefully before answering, but present only the useful final output.
- Preserve every explicit constraint and requirement.
- State assumptions explicitly when information is missing.
- Prioritize precision and actionability.
- Default to clear, well-structured markdown unless the user requests JSON, raw output, code-only output, or brevity.
- Include relevant risks, edge cases, validation steps, or blind spots.
Task-specific best practices:
- **Coding**: Complete code with structure, comments, tests/commands, and common failure modes.
- **Debugging**: Root cause → reproduction → fix → verification → prevention.
- **System Design**: Architecture overview, trade-offs, constraints, integration points, validation plan.
- **Writing**: Match requested tone, audience, and format exactly.
- **Research/Validation**: Separate facts from assumptions, note confidence/uncertainty.
- **Analysis**: Balanced comparison, clear recommendation when justified.
- **General**: Maximize usefulness while minimizing cognitive load.
Apply this guidance to the current user request.
"""

def main():
    try:
        event = json.load(sys.stdin)
        prompt = (
            event.get("prompt")
            or event.get("input")
            or event.get("message")
            or ""
        ).strip()
        if not prompt or should_skip(prompt):
            print(json.dumps({"decision": "approve"}))
            return
        if len(prompt) > MAX_PROMPT_CHARS:
            print(json.dumps({
                "decision": "approve",
                "contextInjection": (
                    "Large prompt detected. Preserve the user's exact intent "
                    "and respond in a clear, structured, actionable format."
                )
            }))
            return
        print(json.dumps({
            "decision": "approve",
            "contextInjection": build_optimization_context(prompt)
        }))
    except Exception as e:
        print(f"[Prompt Optimizer] Failed open: {type(e).__name__}", file=sys.stderr)
        print(json.dumps({"decision": "approve"}))

if __name__ == "__main__":
    main()
