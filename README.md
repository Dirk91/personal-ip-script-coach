# personal-ip-script-coach

**中文名称：个人 IP 爆款脚本引导挖掘 Skill**

> **版本：** [v0.1.2](CHANGELOG.md)<br>
> **最近提交：** `ebeb2a1`<br>
> **自动校验：** 28 项测试通过 · 仓库结构校验通过<br>
> **开源协议：** [MIT License](LICENSE)

把个人经历变成好内容，真正难的通常不是“把话写漂亮”，而是把关键的真实素材挖出来。本 Skill 让 Agent 先判断稿子缺什么，再按一次一个问题的节奏追问，最后才整理为可口播的完整脚本。

## 你可以用它做什么

| 你手上有什么 | 它会怎么帮你 |
| --- | --- |
| 一篇写不顺的口播稿 | 先指出亮点、缺口和应优先补的素材，不直接替你乱改。 |
| 一个选题和零散想法 | 用访谈把经历、案例、判断和原话逐步挖出来。 |
| 一份语音逐字稿 | 提取可用的个人表达，补齐观众、证据、机制和行动路径。 |
| 已经准备好的素材 | 生成完整脚本，并检查事实、隐私、口语感和 CTA。 |

## 三步开始

1. **下载或克隆**本仓库；
2. **选择平台入口**：Codex、Claude Code、WorkBuddy、豆包或其他可读文件的 Agent；
3. **先给素材，再选模式**：只诊断、逐步共创或生成完整版。

最简单的第一句话：

```text
使用 $personal-ip-script-coach。先只诊断这篇口播稿缺什么，不要直接改写。
```

一个面向个人 IP 口播稿的开源 Agent 工作流：先诊断稿子缺什么，再用“一次只问一个问题”的访谈，把创作者脑中的真实经历、案例、判断和原话挖出来，最后整理成仍然像本人说话的完整脚本。

它不是固定文案模板，也不保证爆款。它解决的是更基础的问题：让不同 Agent 都能用同一套方法，少编、少美化，多追问真实素材。

## 开始前必读

- [重要说明](NOTICE.md)：开源层、用户素材和非公开商业材料的授权边界；
- [完整使用说明](docs/USER_GUIDE.zh-CN.md)：安装、模式、提示词、故障处理和发布前检查；
- [用户须知与免责声明](docs/DISCLAIMER.zh-CN.md)：AI、平台、隐私、版权和结果风险；
- [版权、转载与传播规则](docs/CONTENT_POLICY.zh-CN.md)：MIT 仓库允许什么，用户私密材料保护什么；
- [非公开材料保密与禁止转录约定模板](docs/CONFIDENTIALITY_TEMPLATE.zh-CN.md)：用于课程、社群、咨询或企业内部交付，不限制已公开的 MIT 仓库。

> **授权边界：** 本仓库是 MIT 开源项目，因此不能禁止他人依法转发或修改公开文件。禁止转发、录屏、转录和导入知识库的要求，只能针对另行交付的非公开材料，通过单独、明确的约定建立。

## 能做什么

- 诊断已有口播稿的优势、缺口和补充顺序；
- 从选题、语音逐字稿或零散素材建立初稿；
- 通过逐轮访谈补案例、个人证据、机制和行动路径；
- 保留创作者的高辨识度原话与口语节奏；
- 在素材足够时生成完整稿，并检查事实、隐私和 CTA。

## 能力边界

首版不负责自动发布、平台抓取、视频剪辑或账号数据复盘；不虚构经历、结果、数字和对话；不替任何内容作传播效果保证。**不保证爆款**，只提高脚本的相关性、证据密度、个人表达和可执行性。

## 三种模式

1. **只诊断**：告诉你已经有什么、还缺什么、先补哪一项。
2. **逐步共创**：先诊断，再每轮只问一个问题，让你自己说出素材。
3. **生成完整版**：素材齐备后成稿；若你要求提前出稿，会明确标成临时版并列出缺口。

## 仓库结构

```text
personal-ip-script-coach/
├── SKILL.md
├── AGENTS.md
├── CLAUDE.md
├── PROMPT.md
├── NOTICE.md
├── VERSION
├── CHANGELOG.md
├── CONTRIBUTING.md
├── agents/openai.yaml
├── docs/
│   ├── USER_GUIDE.zh-CN.md
│   ├── DISCLAIMER.zh-CN.md
│   ├── CONTENT_POLICY.zh-CN.md
│   └── CONFIDENTIALITY_TEMPLATE.zh-CN.md
├── references/
│   ├── default-video-standard.md
│   ├── interview-playbook.md
│   └── final-review-checklist.md
├── examples/complete-demo.md
├── scripts/validate_repo.py
└── tests/
    ├── test_repository_contract.py
    ├── behavioral-scenarios.md
    └── smoke-test-results.md
```

`SKILL.md` 是唯一核心规则源。其他平台入口只负责把 Agent 引回核心文件，避免不同平台各自演化出一套流程。

## 快速开始

把仓库克隆或下载到本地：

```bash
git clone <repository-url> personal-ip-script-coach
cd personal-ip-script-coach
```

然后按平台选择入口。

### Codex

把整个 `personal-ip-script-coach` 目录复制或链接到 Codex 可读取的 Skills 目录，或直接在仓库中工作。调用示例：

```text
使用 $personal-ip-script-coach。先只诊断这篇口播稿缺什么，不要直接改写。
```

Codex 会从 [SKILL.md](SKILL.md) 和 [OpenAI 元数据](agents/openai.yaml) 进入核心流程。

### Claude Code

用 Claude Code 打开仓库。根目录的 [CLAUDE.md](CLAUDE.md) 会引导它读取 [SKILL.md](SKILL.md) 和当前阶段需要的 reference。

```text
请按仓库里的 personal-ip-script-coach 工作流，一次问我一个问题，把这组零散素材补成口播稿。
```

### WorkBuddy

实测可把整个仓库压缩包上传到 WorkBuddy。上传后要求它先解压并读取 [PROMPT.md](PROMPT.md)，再进入 [SKILL.md](SKILL.md)。如果当前版本不能跟随文件链接，复制 `PROMPT.md` 的“Concise fallback”段落到对话中，再粘贴你的稿件或素材。

### 豆包

豆包网页对话实测不接收 ZIP。分别上传 [PROMPT.md](PROMPT.md) 和 [SKILL.md](SKILL.md)；需要严格访谈时，再上传 [references/interview-playbook.md](references/interview-playbook.md)。第一条指令写：

```text
先读取 PROMPT.md，再读取 SKILL.md。现在进入逐步共创模式。整条回复最多出现一个问号，最后只索取一个信息点。
```

如果豆包当前会话不能读取文件，复制 `PROMPT.md` 的 fallback 内容使用；不要要求它假装读取了仓库。

网页端实测中，豆包即使加载了三份文件，首轮诊断仍可能把受众备选项写成多个反问句。遇到这种情况，直接指出“废弃上一轮多问题输出，只保留一个信息点”，再继续访谈；不要一次回答它列出的全部问题。跨平台行为记录见 [tests/smoke-test-results.md](tests/smoke-test-results.md)。

### 通用 Agent

任何能读取本地文件、项目仓库或上传附件的通用 Agent，都可以先读 [PROMPT.md](PROMPT.md)，再转入 [SKILL.md](SKILL.md)。完全不支持文件读取的平台，只能复制 `PROMPT.md` 的简版规则和待处理素材。

## 推荐输入

最少提供以下任意一种：

- 一篇已有口播稿；
- 一个选题和若干零散素材；
- 一份语音逐字稿。

还可以提供自己的视频标准、历史脚本、匿名后的评论/私信、真实案例、目标平台、时长和内容目标。当前任务指令和用户标准永远高于仓库默认标准。

## 使用示例

```text
这是我的稿子和视频标准。先只诊断，不要重写；然后我说“继续”时，进入逐步共创，一次只问我一个问题。
```

完整的虚构演示见 [examples/complete-demo.md](examples/complete-demo.md)。

## 验证

仓库核心校验只依赖 Python 3 标准库：

```bash
python3 -m unittest tests.test_repository_contract -v
python3 scripts/validate_repo.py
```

第二条命令通过时会输出 `Repository validation passed.`。

人工行为验收见 [tests/behavioral-scenarios.md](tests/behavioral-scenarios.md)，四入口烟测记录见 [tests/smoke-test-results.md](tests/smoke-test-results.md)。

## 隐私

- 公开前隐藏截图中的头像、昵称、账号、联系方式和无关元数据；
- 不把私人会话、真实粉丝身份、会话 ID、本地绝对路径或临时附件路径提交到仓库；
- 不确定的事实应标为待核实；
- 示例和测试使用虚构或匿名材料；
- 没有文件能力的平台不应声称已经保存内容。

## 贡献

欢迎提交 issue 或 pull request，尤其是：

- 不同 Agent 平台的实际加载结果；
- 能暴露“一次一问”失效、标准优先级错误或虚构事实的行为场景；
- 更清晰但不复制核心流程的平台入口；
- 隐私与安全输出方面的改进。

修改核心行为时，请同步更新测试和相关 reference，并确保平台入口仍然回到 `SKILL.md`。

提交前请阅读 [贡献指南](CONTRIBUTING.md)。

## 版本与发布

当前版本为 **v0.1.2**。每次对外发布都会更新 [VERSION](VERSION) 与 [更新记录](CHANGELOG.md)，并执行两条本地校验命令。详细改动见 [CHANGELOG.md](CHANGELOG.md)。

## License

公开仓库文件适用 [MIT License](LICENSE)，可以在保留版权和许可声明的前提下使用、复制、修改与分发。用户输入、第三方材料和另行交付的非公开内容不因使用本项目而自动获得 MIT 授权。详细边界见 [NOTICE.md](NOTICE.md) 与 [版权、转载与传播规则](docs/CONTENT_POLICY.zh-CN.md)。
