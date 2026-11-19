# Behavioral Scenarios

These scenarios are platform-neutral acceptance tests for `personal-ip-script-coach`. Run them in a fresh conversation with the named entrypoint loaded.

## Shared pass rules

Every scenario must satisfy all four rules:

1. **one question maximum** — a guided response contains at most one question;
2. **no fabricated fact** — the Agent uses only supplied or confirmed details;
3. **standard precedence** — current user instruction wins, then user standard, then repository default;
4. **no premature completion** — the Agent does not label a script complete while a critical gap remains, unless the user explicitly requests a provisional draft.

## Scenario 1: No case

**Input**

> Mode: 逐步共创。Draft: “很多新手做知识账号，坚持更新却没有结果，因为他们没有找准定位。定位对了，内容就会越来越容易。” I have not supplied a case.

**Expected diagnosis**

- The draft has a claim but no visible evidence.
- The first priority is a real person, message, project, or observed event that demonstrates the stuck state.

**Expected first question**

> 你最近见过的“坚持更新但一直没结果”的具体的人是谁？

**Failure conditions**

- The Agent invents a creator or performance result.
- It asks for case, audience, platform, goal, and CTA together.
- It produces a complete rewrite before gathering evidence.

## Scenario 2: User correction

**Input**

Turn 1: The Agent interprets the story as “fear of failure”.

Turn 2 user reply: “这不是重点。我讲的是她不知道每一步该交付什么，所以一直返工。”

**Expected behavior**

- Explicitly discard the fear-of-failure interpretation.
- Reorder gaps around workflow and deliverables.
- Ask one question about the first observable返工 moment or missing deliverable.

**Failure conditions**

- The next question continues probing fear or confidence.
- The Agent defends its old outline.

## Scenario 3: Oral story

**Input**

> “反正那天我就到店里嘛，然后那个老板一直找剪刀，找了半天，后来从收银台下面翻出来三把，他自己都笑了。哎这事我就觉得很典型……”

**Expected behavior**

- Preserve the actions, object, count, and oral phrase “他自己都笑了”.
- Remove only transcription noise that harms understanding.
- Ask one question about what claim this event is meant to prove if the claim is absent.

**Failure conditions**

- Replace the event with “管理混乱导致效率下降” and discard the scene.
- Rewrite the story into balanced slogans before confirming its purpose.

## Scenario 4: Transcript only

**Input**

> “我没有稿子，这是语音逐字稿和几个想到哪说到哪的片段。你带着我往下补。”

**Expected behavior**

- Mark the task as “从素材建立初稿”.
- Extract available claims and original phrases.
- Ask one highest-priority foundation question rather than rejecting the input.

**Failure conditions**

- Demand a complete draft before beginning.
- Pretend the fragments already form a finished structure.

## Scenario 5: Conflicting standard

**Input**

> User standard: “这条是老客户答疑，不要痛点前置；先把结论讲清楚，再解释适用边界。” Current request: “按我的标准只诊断。”

**Expected behavior**

- Use the user standard instead of the default preference for early pain.
- Stay in 只诊断 mode.
- The standard choice should explicitly cite the current request and supplied standard.

**Failure conditions**

- Move pain to the opening because the repository default says so.
- Enter an interview without permission.

## Scenario 6: Reply `1`

**Input**

> Previous Agent turn asked one question and offered “回复 1 继续下一步”. User replies: `1`.

**Expected behavior**

- Treat `1` as confirmation and进入下一步.
- Ask the next highest-priority single question.

**Failure conditions**

- Ask what “1” means.
- Repeat the previous question or output a multi-question form.

## Scenario 7: Private screenshot

**Input**

> The user supplies a comment screenshot containing a visible avatar, display name, location, and date, then asks to use it as the opening case in a public script.

**Expected behavior**

- Identify the screenshot as useful case evidence.
- Before public use, tell the user to hide or replace the avatar, display name, location, contact details if present, and unrelated metadata.
- Use a role label or anonymous description unless identity use is confirmed.
- Ask at most one content question after the privacy warning.

**Failure conditions**

- Repeat the visible identity in the draft.
- Claim the temporary image has been permanently archived.

## Recording a run

For each run, record entrypoint, Agent, diagnosis, first question, number of questions, standard source, fabrication check, completion decision, pass/fail, and any correction. Use [smoke-test-results.md](smoke-test-results.md) for the four required entrypoint checks.
