---
name: workflow-distiller
description: Distil a repeated, validated process into a narrow reusable Skill - check the existing index first for an updatable neighbour, strip every real name before the Skill goes public, and sync README plus CHANGELOG in the same commit. Also use when asked to "沉淀 skill" or "沉淀一下今天的". Not for one-off answers, unverified fixes, or turning private facts into memory (that belongs in dated memory logs).
version: 2.0.0
---

# Workflow Distiller

Turn a repeated, verified process into a narrow reusable Skill.
Ordinary facts belong in memory; a one-off task belongs in a task record.

**Evidence bar**: repeated at least twice, or done once with a failure you had to fix by hand.
A workflow you only *plan* to repeat is a candidate, not a Skill.

## Step 1: Check the index before you create anything

🔴 **The dominant failure is creating a duplicate.** A Skill set that grows organically accumulates
near-twins that then fire on each other's triggers and drift apart.

1. **List what already exists — on the remote, not from memory.** Skill counts quoted in old notes
   are stale within a day. Two sessions in one day reported the same repo as "9", "21" and "24";
   the API said 24.
2. If a neighbour already covers 80% of the process → **upgrade it, do not fork it.**
   Adding a mode to an existing Skill beats a second overlapping folder.
3. If you do create one, write the boundary explicitly: what it does **not** handle, and which
   neighbour owns that. Descriptions without a negative boundary get triggered by unrelated work.

Real case: a request to distil "面试复盘" looked like a new Skill, but `interview-debrief` already
existed. The right move was a v2.0.0 that adds a second mode, not a second folder.
The same pass found that Skill was **missing from the README index entirely** — a Skill that exists
but is not listed is invisible, so "check the index" means check both directions.

## Step 2: Distil the failure modes, not the happy path

The happy path is what any competent assistant already does. **The Skill earns its keep by encoding
what actually went wrong.** For each step ask: what did I get wrong, and what would have prevented it?

Write down:

- The wrong command / wrong tool name you tried first (`lark-cli meeting` does not exist; it is `note`)
- The tool that silently truncates (`WebFetch` stops at the first large table)
- The success signal that lies (a script returning `success: true` while the content is wrong)
- The thing that is broken on this machine and should be routed around, not fixed

## Step 3: Mark what is verified

Every non-obvious claim carries one tag:

- `【事实】` + where you saw it
- `【推断】` + what it rests on
- `【待确认】` + what blocks confirmation

Two rules that follow:

- 🔴 **"I never verified it" ≠ "it is wrong."** A number in an existing artifact was judged fabricated
  because the same number appeared elsewhere with a different meaning. Re-counting the source showed
  both were real and meant different things. **Open the source and count before you "correct" a number.**
- 🔴 **Numbers are re-counted, never recalled.** Different sessions carry different counts. Quote them
  side by side with their source, then give the freshly verified value. Do not merge them, do not guess
  which is right.

## Step 4: Desensitise before anything goes public

Deleting file paths and referral codes is **not** desensitisation. The leaks that actually happen:

| 漏的是什么 | 例子 |
|---|---|
| 人名 | 候选人姓名、同事、内推人 |
| 雇主名 / 学校名 | 写在 Example 里最难发现 |
| 录用进度、薪资 | "已 offer 待签" 比公司名更暴露 |
| **示例里的真实事件** | 用真实客户案例当 Example，等于把客户公开 |
| 情绪措辞 | 教训里的批评原话不要照抄进公开产物；留内核，去掉原话 |

**Check the Example block specifically.** It is where real names survive every other pass, because
it is the part that looks harmless.

Rule of thumb: a paid job for a client never turns into a public example with the client's details in it.
Generalise — "某高校计算机专业", "一家情感社交产品" — or use a synthetic case.

## Step 5: Version, index, changelog — in one commit

Semantics: **new** Skill `v1.0.0`; **new mode or new gate** → minor bump; **correction or wording** → patch.

🔴 **A Skill that is not in the index does not exist.** Every push that adds or bumps a Skill must, in
the same commit:

1. Add or update its entry in `README.md` — one English line of scope + one Chinese parenthetical
2. Update the count wherever it is stated (headline, `Contents`, badge, category roll-ups)
3. Add a `CHANGELOG.md` entry under a new version heading: Added / Changed / Fixed, each naming the
   Skill and its from → to version

**Derive those counts from the remote listing, not from the previous changelog entry.** The count in
the last changelog line is the count before your change.

## Step 6: Push without clobbering

🔴 **Concurrent sessions overwrite each other silently.** A push at 17:45 from one session replaced a
17:05 push from another, and the later one did not know the earlier one existed. Before pushing:

1. **Fetch the current remote HEAD and the sha of every file you are about to touch.**
2. Build the new tree with that sha as `base_tree` — never a locally cached tree.
3. Only include files you actually changed. A staging directory that still holds last week's copy of
   `README.md` will silently revert it.
4. After the push, **fetch the file back and confirm the content** — do not trust the commit sha.

Also note: `git push` may be blocked by the network while the Git Data API works. When transport fails,
build the commit through the API (blob → tree → commit → update ref) rather than retrying the push.

## Step 7: Run any shipped script once

A script in `scripts/` that has never executed is a liability: it will be cited as working. Run it
against an isolated case and keep the result in the Skill as evidence.

> 🔴 Referencing a script that does not exist is the same bug. One release of this Skill told readers
> to run `quick_validate.py`, a file the repository never had.

## Keep SKILL.md short

Purpose, trigger boundary, essential constraints, routing. Mode-specific detail goes to `references/`,
deterministic repeated work goes to `scripts/`. A Skill nobody reads start to finish does not fire.

## Red lines

- 🔴 **A Skill never expands authorization.** No publish, send, install, or modify of unrelated systems
  just because a workflow mentioned them.
- 🔴 **No secrets, no private chats, no company material, no hidden reasoning.** Desensitise at Step 4,
  not after the push.
- 🔴 **Do not distil a process you have not actually run.** A plausible-looking workflow that fails the
  first time it is used is worse than no Skill.

## Example

Repeated and validated → candidate:

> 每次发作品集都要：列改动文件、确认 URL、dry-run、再发布，而且每次都怕覆盖线上。

One-off with no evidence → not a Skill, leave it as a task record:

> 这次把首页标题改大一点。

Distilled once but with a real failure fixed by hand → still worth it:

> 今天第一次给客户做面试诊断，踩了「WebFetch 截断逐字稿」「Word COM 坏了导不出 PDF」
> 「远程已有 interview-debrief 却不在索引里」三个坑 → 全部写进 v2.0.0，下次直接复用。
