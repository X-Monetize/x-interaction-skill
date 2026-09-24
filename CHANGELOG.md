# Changelog

版本号遵循语义化版本（SemVer）：`major.minor.patch`。

- major：不兼容的大改动
- minor：新增平台或新能力
- patch：修复、规则微调

## v0.2.0 — 2026-09-24

- 移除内置的账号与语气设定（不再包含任何具体 X 账号或个人定位），面向所有使用者
- `references/voice.md` 改为通用语气模板：由使用者自行提供定位，或由 Agent 从上下文判断
- 输出头与规则中不再出现具体账号

## v0.1.1 — 2026-09-24

- 文档修正：调用示例和 default_prompt 的前缀由 `$` 改为 `/`（正确的唤起方式）

## v0.1.0 — 2026-09-24

首个版本。

- 支持平台：Tutti、灯塔（Lighthouse）
- 输出：回复、引用（可单要或都要）
- 读取：免登录免费接口（FxTwitter / VxTwitter / X 嵌入接口），附 `scripts/fetch_tweet.py`
