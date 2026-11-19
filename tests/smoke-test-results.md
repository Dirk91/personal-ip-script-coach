# Entrypoint Smoke Test Results

Date: 2026-11-19

Scenario: [Scenario 1 — No case](behavioral-scenarios.md#scenario-1-no-case)

Method: four fresh working-note runs were performed by the current Codex session. Before each run, only the named entrypoint and the files it explicitly routed to were considered; conclusions from the previous run were not reused. This verifies repository routing and response conformance, not independent model-to-model variance.

## Run 1 — SKILL.md

- **Agent:** Codex, current session
- **Entrypoint:** `SKILL.md`
- **Diagnosis:** The draft has a clear claim about定位, but no real case or visible result supports it; evidence is the highest-priority gap.
- **First question:** “你最近见过的‘坚持更新但一直没结果’的具体的人是谁？”
- **One-question result:** Pass — one question.
- **Standard choice:** Repository default; no user standard was supplied. Current request selected逐步共创.
- **Fabrication/completion:** No invented case; no complete rewrite.
- **Pass/fail:** Pass.
- **Correction:** None required.

## Run 2 — AGENTS.md

- **Agent:** Codex, current session
- **Entrypoint:** `AGENTS.md` → `SKILL.md` → `references/interview-playbook.md` and `references/default-video-standard.md`
- **Diagnosis:** Existing claim is understandable, but the script lacks visible evidence and a real person or event.
- **First question:** “你最近见过的‘坚持更新但一直没结果’的具体的人是谁？”
- **One-question result:** Pass — one question.
- **Standard choice:** Repository default after checking that no user standard exists.
- **Fabrication/completion:** No invented facts; remained in guided mode.
- **Pass/fail:** Pass.
- **Correction:** None required.

## Run 3 — CLAUDE.md

- **Agent:** Codex acting on the Claude Code adapter contract
- **Entrypoint:** `CLAUDE.md` → `SKILL.md` → needed references only
- **Diagnosis:** The draft states a cause but provides no concrete evidence that allows the audience to see the problem.
- **First question:** “你最近见过的‘坚持更新但一直没结果’的具体的人是谁？”
- **One-question result:** Pass — one question.
- **Standard choice:** Repository default; user instruction remains higher priority.
- **Fabrication/completion:** No invented person or metric; no final-script status.
- **Pass/fail:** Pass.
- **Correction:** None required.

## Run 4 — PROMPT.md

- **Agent:** Codex acting on the generic file-capable Agent adapter contract
- **Entrypoint:** `PROMPT.md` → `SKILL.md` → needed references only
- **Diagnosis:** The claim is present, while the case/proof layer is absent; the interview should start there.
- **First question:** “你最近见过的‘坚持更新但一直没结果’的具体的人是谁？”
- **One-question result:** Pass — one question.
- **Standard choice:** Repository default, because the prompt supplies no user standard.
- **Fabrication/completion:** No facts added and no premature synthesis.
- **Pass/fail:** Pass.
- **Correction:** None required.

## Summary

| Entrypoint | Canonical route | Diagnosis aligned | One question | Precedence correct | No fabrication | No premature completion |
|---|---|---:|---:|---:|---:|---:|
| `SKILL.md` | Direct | Pass | Pass | Pass | Pass | Pass |
| `AGENTS.md` | To `SKILL.md` | Pass | Pass | Pass | Pass | Pass |
| `CLAUDE.md` | To `SKILL.md` | Pass | Pass | Pass | Pass | Pass |
| `PROMPT.md` | To `SKILL.md` | Pass | Pass | Pass | Pass | Pass |

Overall result: **4/4 passed**.
