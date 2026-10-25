---
name: personal-tone-writing
description: Write in a specific person's own voice - the punctuation bans, the anti-pivot sentence ban, plain-language over jargon, identity-first openings, and the boundary rule that decides when the voice library must NOT be applied. Covers three delivery shapes with different rules: written test answers (typos are required), spoken scripts (typos are forbidden), and internal work docs (typos are forbidden). Triggers on "用我的语气写", "过一遍语气库", "这版像不像我写的", "帮我写口播稿", "写个工作流程规范". Not for fact-checking and not for editing someone else's original text.
version: 1.0.0
---

# Personal Tone Writing

Writing that reads like one specific human. The shape is **a spoken shell around a professional
core**: the tone can be loose, the logic cannot.

## Step 0 — The boundary rule (read this first)

The voice library is a **ghostwriting** tool. It is not a filter to run over his own drafts.

| Situation | Apply the voice library? |
|---|---|
| Application open questions, written-test answers, interview scripts — **newly written** | ✅ yes |
| Spoken scripts / short-video scripts — **newly written** | ✅ yes, but see the spoken block below |
| Internal workflow docs / specs — **newly written** | ✅ yes, but see the docs block below |
| His own existing drafts, **or an old draft you were asked to dig up** | 🚫 never |
| Someone else's original text, a brand brief, a data table | 🚫 never — touching it is falsification |

> Real case: asked to dig up an old script from the memory base, I could not find it and quietly
> wrote a fresh one in his voice instead. His reply was "I didn't ask you to run my script through
> my voice library." Running an original through the library **is** rewriting it, which makes the
> retrieval pointless — he wanted the artifact, not a version of it.

🔴 **If you cannot find it, say you cannot find it.** He would rather hear "it was never saved"
than receive a draft he cannot tell apart from the original.

## Step 1 — Punctuation bans (hard)

| Mark | Rule |
|---|---|
| Dash `——` | forbidden entirely |
| Colon `：` | forbidden — start a new sentence or use a comma |
| Semicolon `；` | basically never — split into two sentences or use a comma |
| Quotation marks | forbidden entirely. Quote by breaking with a comma: 大意是骂你是因为喜欢这款游戏 |
| Comma | the workhorse. One comma after another is the actual style |
| Exclamation `！` | only on genuine emotion, 3-5 sentences apart, never doubled |
| Ellipsis | rare. To drag emotion use **three Chinese full stops** `。。。` |

Quotation marks in particular: the fix is not deletion, it is four moves —
comma-parenthesise it into the sentence, introduce it with a comma, write it bare, or expand the
quoted words into plainer speech.

## Step 2 — Ban the pivot sentence

`不是 A，而是 B` is the single most reliable AI tell. **More than one occurrence in a piece reads
as machine-written.** Allow at most one, and prefer rewriting to a direct positive statement.

- ❌ 它考的不是操作，而是记忆 → ✅ 它考的全是记忆
- ❌ 我不是因为数值留下来的，而是因为人 → ✅ 我是因为人才留下来的，跟数值没啥关系

Same family, same ban: `与其说…不如说…`.

## Step 3 — Plain language, and never exhaustive

Jargon in an operations answer is a failure, not a flex.

| Written | Should be |
|---|---|
| 配置源 | 同一个东西在两个地方各写了一遍 |
| 一致性校验 | 文字跟实际对不上 |
| 灰度 / 回滚预案 | (do not write it, he does not need it) |
| 置信度 | 自己没把握的地方 |

And **不面面俱到才是真人的思考模式** — a real person holds four or five points, not eight.
Keep every list to **3-5 items**; cut the rest rather than round them out.

## Step 4 — Identity first, then method

If the question covers work he has actually done, the first sentence must say so. A generic
methodology answer throws away his strongest card.

- Open with 这个我干过，去年做 X 的时候就是从零起的内容板块
- Then, mid-answer, 我在那边就是这么干的

Subjective markers — 我个人觉得 / 我的想法是 / 我看下来 — at least **3 per piece**.

## Step 5 — Shape-specific rules

The three delivery shapes disagree with each other. This is where most mistakes happen.

| | Written test / open question | Spoken script | Internal work doc |
|---|---|---|---|
| Typos | **required, 2-4** (的/得/地, 在/再) | **forbidden** | **forbidden** |
| Why | the strongest "a human typed this" signal | you cannot hear a typo when it is spoken | a colleague follows it; a typo is rework |
| Length | 400-430 chars when capped | 4.5-5 chars per second — fix duration first | one page |
| List items | 3-5 | five blocks | 3-5 steps |

**Spoken script specifics**

1. Fix duration first, then word count: **4.5-5 chars/second**, so 70 seconds ≈ 335 characters.
2. Five blocks: hook (0-5s) → turn / identity (5-12s) → mechanism (12-30s) → what to do (30-45s)
   → close + sign-off.
3. **Reverse-play hook**: spend the first three seconds performing the other side's pitch, then
   flip at second five. That gap is what holds the viewer. 🔴 The flip must land inside 5 seconds
   or the video genuinely becomes the thing it is mocking.
4. Deliver **pure dialogue only** — no timecodes, no action notes, no subtitle markup.
5. Cover: yellow headline 2 lines + white subline 1 line, few words. Real numbers; absurdity is
   enough without exaggeration.
6. Do not name real institutions, do not quote a specific price, do not say 骗 or 诈骗 — lay out
   the fact chain and let the viewer conclude.

**Internal work doc specifics**

- One page. Every step is 2-3 sentences and states **an action, not a principle**
  (写 前贴丢给百炼反推, not 通过视觉理解模型实现提示词逆向工程).
- The step he called out as most important gets marked in its heading.

## Step 6 — Official external voice (a different register entirely)

Addressing users publicly is not a tone-concentration question, it is a different register.
Order: **敬语（您 / 大家）→ 共情 → 感谢对方的贡献 → 正式道歉（自报昵称）→ 具体动作（到人、到时间）
→ 官方感言 → 祝福收尾**.

- Never 称兄道弟, never join the users in trash-talking your own product.
- Apologise by owning the fault — no external excuses.
- Actions must be concrete. If you have no authority, say it will be escalated.

## Self-check before sending

1. Does this read like him talking to a classmate, then analysing properly?
2. Strip the filler — is the skeleton still a complete professional argument? (It must be.)
3. Any sentence an AI would write but he would not say? Rewrite it.
4. Any dash, colon, semicolon, or quote? Delete all of them.
5. How many pivot sentences? More than one → fix.
6. **Is this a newly written piece?** If it is his original, you should not have touched it.

## Red lines

- 🔴 **Never invent a number to make the voice land.** Tone is worthless if the figure pops under
  one question.
- 🔴 **Never leave an unfinished item in the self-check** ("typos not added yet"). Ship complete or
  do not ship.
- 🔴 **Never run the voice library over a draft you were asked to retrieve.**
