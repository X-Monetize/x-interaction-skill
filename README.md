# x-interaction-skill

给一个推文链接，按任务平台（Tutti、灯塔）的规则草拟回复和/或引用文案，复制后手动发布。

- 读取推文完全免费：依次尝试 FxTwitter、VxTwitter、X 官方嵌入接口，不需要 API Key，也不登录 X 账号
- 只起草文案，不自动发布（两个平台都禁止自动化互动）
- 适用于 Codex、Claude Code 等支持 Agent Skills 的工具

## 目录

```
x-interaction-skill/
├── SKILL.md              # 入口：流程、通用规则、输出格式
├── platforms/
│   ├── tutti.md          # Tutti 规则
│   └── lighthouse.md     # 灯塔规则
├── references/voice.md   # 语气模板（通用，可自行覆盖）
├── scripts/fetch_tweet.py
└── agents/openai.yaml    # Codex 显示信息
```

## 安装

把本目录软链接到 Agent 读取 Skill 的位置：

```bash
# Codex（项目级）
ln -s /path/to/x-interaction-skill /path/to/project/.agents/skills/x-interaction-skill

# Claude Code（项目级）
ln -s /path/to/x-interaction-skill /path/to/project/.claude/skills/x-interaction-skill
```

## 使用

两个客户端的唤起前缀不同：

```bash
# Codex —— $ 前缀
$x-interaction-skill 灯塔任务，只要回复：https://x.com/xxx/status/123

# Claude Code —— / 前缀
/x-interaction-skill 灯塔任务，只要回复：https://x.com/xxx/status/123
```

不写"回复"或"引用"时默认两种都给；不写平台时会先问。

## 平台规则更新

规则变了只改对应的 `platforms/*.md`，并更新文件顶部的更新日期。新增平台：复制一份现有平台文件，填好同样的几个小节，再在 `SKILL.md` 的 Workflow 和 Resolve 表里加上。

## 单独使用读取脚本

```bash
python3 scripts/fetch_tweet.py "https://x.com/xxx/status/123" --replies 15
```

输出精简 JSON：原推正文、作者粉丝数、互动数据、被引用推文、Thread 前后文、已有回复（仅 FxTwitter 源）。

## 作者

由 [@alexgiantwhale](https://x.com/alexgiantwhale) 维护 —— Go 后端工程师，在 X 上分享 AI 工具和工程向内容。欢迎关注。

