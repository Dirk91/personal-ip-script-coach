# 贡献指南

感谢你愿意改进 personal-ip-script-coach。

## 适合提交的改进

- 不同 Agent 平台的真实安装与加载结果；
- 能复现“一次只问一个问题”失效、事实被虚构或隐私边界被忽略的场景；
- 更清晰的平台入口或使用说明；
- 匿名、虚构的示例与测试材料；
- 文档、链接、测试与兼容性修复。

## 提交前请确认

1. 不提交真实用户稿件、录音、聊天记录、截图、联系方式、账号 ID、API Key 或本机绝对路径；
2. 核心行为变更必须同步更新相关 reference、行为场景或测试；
3. 所有平台入口仍应指向 [SKILL.md](SKILL.md)，不要维护彼此矛盾的独立流程；
4. 运行并通过：

```bash
python3 -m unittest tests.test_repository_contract -v
python3 scripts/validate_repo.py
```

## Pull Request 说明建议

请在描述中写清：

- 你观察到的实际问题；
- 修改了哪些文件；
- 如何验证；
- 是否改变了核心工作流或兼容性。

提交即表示你确认拥有所提交内容的必要权利，并同意其按本仓库的 [MIT License](LICENSE) 发布。
