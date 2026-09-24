---
name: x-interaction-skill
version: 0.1.1
description: Draft ready-to-post reply and/or quote copy for an X/Twitter status link, following the rules of a task platform (Tutti or 灯塔/Lighthouse). Use when the user gives an x.com or twitter.com link and asks for 回复, 引用, 评论, or both, or mentions a Tutti or 灯塔 task. Reads the tweet through free no-login endpoints only. Output copy for the user to paste and publish manually; never post, schedule, or save files.
---

# X Interaction

Turn one tweet link into copy the user can paste straight into X. The user publishes by hand, so reading must stay free and nothing here touches an X account.

## Resolve the Request

Before fetching, settle three things from the user's message. Ask only if something is genuinely missing and cannot be defaulted.

| Item | Values | Default |
|---|---|---|
| Output | 回复 / 引用 / 两者 | Both, if the user does not say |
| Platform | Tutti / 灯塔 | Ask if unclear; the rules differ |
| Account | @AlexUseAI / @alexgiantwhale | @AlexUseAI |

Words like "评论" mean 回复. "转评" or "带评转发" mean 引用.

## Workflow

1. Read the platform file for the chosen platform:
   - Tutti: [platforms/tutti.md](platforms/tutti.md)
   - 灯塔: [platforms/lighthouse.md](platforms/lighthouse.md)

   Platform rules override the general rules below when they conflict.
2. Fetch the tweet:

   ```bash
   python3 scripts/fetch_tweet.py "<tweet link>" --replies 15
   ```

   The path is relative to this skill's directory. It needs only Python 3 standard library.

   The script tries FxTwitter, then VxTwitter, then X's embed endpoint. All are free, keyless, and never log in. Only FxTwitter returns existing replies.
3. If every source fails, ask the user to paste the tweet text. Never switch to paid APIs, cookie-based scrapers, or the user's logged-in browser.
4. Understand the tweet before writing:
   - The author's actual point and the specific details (numbers, features, steps).
   - If `quoted` is present, read both layers. If `thread` is present, read the whole thread.
   - Skim `replies` for angles already taken, and avoid them.
5. Read [references/voice.md](references/voice.md) for the account voice.
6. Write only the requested output types, following the rules below and the platform file.
7. Stop after returning the copy. Do not create files, update tracking docs, call publishing tools, or post.

## General Rules

These apply to every platform.

- Add something of the owner's own: a question, a judgment, a use case, or a caveat. Never a bare "说得好", an emoji-only reply, or a paraphrase.
- Never copy the original's sentences or structure, and never reuse a fixed template across tasks.
- Never claim to have used, tested, or bought something unless the user says so. Write "想试试""看起来""准备拿XX试一下", not "实测""用了一周".
- No false or exaggerated claims about the product. Stick to what the original says.
- Do not repeat promo codes, invite links, or referral codes from the original. Point readers to the original post.
- Plain text and emoji only. No Markdown: no `**bold**`, backticks, `-` lists, or tables. X does not render them.
- Colloquial Chinese. If the original is in English, still write in Chinese and add the context a Chinese reader needs.

Output-type rules (platform files may tighten them):

- 回复: written to the author, specific to their post. 1-3 short sentences, at most 140 Chinese characters. No hashtags.
- 引用: written to the owner's own followers, so it must make sense without the original. Hook first, then the one or two points worth knowing, then the owner's angle. Aim for 140 Chinese characters; never exceed 280. At most one or two hashtags.

## Output

Start with one line:

`原推：@作者（N 粉）｜一句话概括｜平台：Tutti｜账号：@AlexUseAI`

Then, for each requested type, give two versions, each in its own `text` code block so the user can copy it in one click. Label each block with a few words on its angle, for example `回复 A（提问）`. Make the two versions genuinely different, such as one concrete question and one judgment. For replies, include at least one version with a specific question, because it invites the author to respond.

End with at most three short notes, only when useful: a claim to verify, a line to delete if the user will not follow through, or a platform rule that shaped the copy.

## 版本与升级

本 Skill 的版本以 `SKILL.md` 开头 frontmatter 里的 `version` 字段为准（语义化版本 `major.minor.patch`）。升级说明见 `CHANGELOG.md`。

Agent 在运行时：

- 回答"当前什么版本"：读本文件 frontmatter 的 `version`，例如 `v0.1.1`。
- 判断"该不该升级"：在 skill 目录下执行 `git ls-remote --tags origin`，取最新的 `v*` tag 与本地 `version` 对比；远端更高就提示有新版本。命令失败（无网络、仓库私有、无 git）时不臆测，改为提示用户自行到仓库查看最新 tag。
- 不要自动 `git pull` 或改动文件。升级由用户决定。

## 发布流程（固化）

每次发版严格按这四步，顺序不能乱：

1. 改 `SKILL.md` frontmatter 的 `version` 为新的版本号。
2. 在 `CHANGELOG.md` 顶部加一条对应版本的记录。
3. `git add -A && git commit -m "chore: bump version to X.Y.Z"`（如改动本身尚未提交，先单独提交改动，再提交版本号）。
4. `git tag vX.Y.Z && git push origin main vX.Y.Z`。

版本号规则（SemVer）：

- **patch（z+1）**：修复、文档修正、平台规则微调、小幅改进。任何已发布内容的修正一律走 patch，不回头改旧版本。
- **minor（y+1，z 归零）**：新增平台、新增能力。
- **major（x+1）**：不兼容的大改动。

**铁律：已经推送出去的 tag 绝不覆盖、不 `--force`、不删除重打。** 发现已发布版本有问题，就发下一个 patch 版本修掉，而不是改写历史。所以 `git tag -f` 和 `git push --force` 在任何情况下都不用。


## Maintaining This Skill

When a platform changes its rules, edit only that platform's file and bump its `更新日期`. To add a platform, copy an existing platform file, fill in the same sections, and add it to the Workflow list and the Resolve table above.
