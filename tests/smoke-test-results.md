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

## Live platform baseline — before atomic-question hardening

Date: 2026-11-19

The same no-case and user-correction prompts were run through the public web interfaces with Computer Use.

### 豆包

- **Load result:** ZIP rejected as an unsupported type; `PROMPT.md` and `SKILL.md` loaded successfully as separate Markdown files.
- **Behavior:** Diagnosed missing evidence, did not invent a case, and explicitly abandoned the rejected interpretation after correction.
- **Observed failure:** The final direction was singular, but diagnosis bullets and the closing prompt contained multiple interrogative clauses and answer slots.
- **Baseline result:** Partial pass.

### WorkBuddy

- **Load result:** Release ZIP accepted. WorkBuddy reported reading `PROMPT.md`, `SKILL.md`, and supporting reference files from the archive.
- **Behavior:** Diagnosed before rewriting, preserved the no-fabrication rule, and immediately discarded the rejected branch after correction.
- **Observed failure:** It bundled person, action, count, result, or several返工 alternatives into one turn.
- **Baseline result:** Partial pass.

The repository was then hardened so a guided reply must satisfy all three observable invariants: at most one question mark in the whole reply, only one interrogative sentence, and exactly one answerable information slot.

## Live platform regression — after atomic-question hardening

Date: 2026-11-19

The same no-case prompt and immediate user-correction prompt were repeated in fresh web conversations after the hardening changes.

### WorkBuddy

- **Load result:** Accepted `personal-ip-script-coach-v0.1.1.zip`, unpacked it, and reported reading `PROMPT.md`, `SKILL.md`, and the referenced rules.
- **Initial turn:** Passed. The reply contained one question mark and requested one fact only: the single audience identity the viewer should recognize as themselves.
- **Correction turn:** Passed. It explicitly discarded the previous audience branch and asked for one observable event only: the work stage in which the返工 occurred.
- **Regression result:** Pass.

### 豆包

- **Load result:** Continued to reject ZIP, but successfully parsed the separately uploaded `PROMPT.md`, `SKILL.md`, and `references/interview-playbook.md` files.
- **Initial turn:** Failed the strict mechanical invariant. Although the closing direction requested one result, a diagnosis bullet described two audience alternatives as rhetorical questions, producing two question marks and multiple answer slots in the full reply.
- **Correction turn:** Recovered the intended behavior. It explicitly discarded the content-goal and audience branches, reordered the diagnosis around workflow deliverables, and requested only one fact about the most common visible返工 behavior. It phrased the request as a declarative instruction and used no question mark.
- **Regression result:** Partial pass. Correction handling and single-slot semantics passed, but the initial full reply still failed the platform-neutral question-mark check.

### Regression summary

| Platform | Package load | Initial atomic turn | Correction branch reset | Correction atomic turn | Overall |
|---|---:|---:|---:|---:|---:|
| WorkBuddy | Pass | Pass | Pass | Pass | Pass |
| 豆包 | Files only | Fail | Pass | Pass | Partial pass |

The repository contract is now explicit and testable, while live compliance remains model-dependent. WorkBuddy follows the hardened contract from the ZIP. 豆包 follows it after correction but may still insert rhetorical questions inside diagnosis despite the uploaded rule, so its deployment instructions continue to require the three-file upload and the explicit one-question reminder.
