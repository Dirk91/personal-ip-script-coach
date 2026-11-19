from __future__ import annotations

import re
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def public_text_files() -> list[Path]:
    ignored = {".git", ".superpowers", "__pycache__"}
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and not ignored.intersection(path.relative_to(ROOT).parts)
        and path.suffix.lower() in {".md", ".yaml", ".yml", ".py", ".txt"}
    ]


def load_validator():
    script = ROOT / "scripts" / "validate_repo.py"
    if not script.is_file():
        raise AssertionError("scripts/validate_repo.py must exist")
    spec = importlib.util.spec_from_file_location("validate_repo", script)
    if spec is None or spec.loader is None:
        raise AssertionError("validator module must be loadable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RepositoryContractTests(unittest.TestCase):
    def test_skill_declares_canonical_name(self) -> None:
        """Catches a missing or wrongly named canonical Skill entrypoint."""
        skill = ROOT / "SKILL.md"
        self.assertTrue(skill.is_file(), "SKILL.md must exist")
        frontmatter = skill.read_text(encoding="utf-8").split("---", 2)[1]
        self.assertRegex(frontmatter, r"(?m)^name:\s*personal-ip-script-coach\s*$")

    def test_public_files_contain_no_private_absolute_paths(self) -> None:
        """Catches accidental publication of local absolute paths."""
        forbidden = ("/" + "Users" + "/", "/var/" + "folders" + "/")
        findings: list[str] = []
        for path in public_text_files():
            text = path.read_text(encoding="utf-8")
            for marker in forbidden:
                if marker in text:
                    findings.append(f"{path.relative_to(ROOT)}: {marker}")
        self.assertEqual([], findings)

    def test_public_files_contain_no_unfinished_scaffold_markers(self) -> None:
        """Catches a release that still contains unfinished placeholders."""
        markers = ("TO" + "DO", "TB" + "D")
        findings: list[str] = []
        for path in public_text_files():
            text = path.read_text(encoding="utf-8")
            for marker in markers:
                if re.search(rf"\b{re.escape(marker)}\b", text, flags=re.IGNORECASE):
                    findings.append(f"{path.relative_to(ROOT)}: {marker}")
        self.assertEqual([], findings)

    def test_relative_markdown_links_resolve(self) -> None:
        """Catches renamed or missing files referenced by public Markdown."""
        missing: list[str] = []
        for path in public_text_files():
            if path.suffix.lower() != ".md":
                continue
            for raw_target in MARKDOWN_LINK.findall(path.read_text(encoding="utf-8")):
                target = raw_target.strip().split("#", 1)[0].strip()
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                resolved = (path.parent / unquote(target)).resolve()
                if not resolved.exists():
                    missing.append(f"{path.relative_to(ROOT)} -> {target}")
        self.assertEqual([], missing)

    def test_validator_exposes_the_repository_contract(self) -> None:
        """Catches a validator that omits a required public check."""
        validator = load_validator()
        expected = {
            "repository_root",
            "find_markdown_links",
            "validate_required_files",
            "validate_relative_links",
            "validate_privacy",
            "validate_placeholders",
            "validate_project_map_coverage",
            "validate_empty_files",
            "main",
        }
        self.assertTrue(expected.issubset(set(dir(validator))))
        self.assertEqual(ROOT, validator.repository_root())

    def test_validator_finds_markdown_links_without_images(self) -> None:
        """Catches link parsing that mistakes embeds for navigational links."""
        validator = load_validator()
        text = "Read [guide](guide.md), not ![image](cover.png)."
        self.assertEqual(["guide.md"], validator.find_markdown_links(text))

    def test_validator_reports_missing_required_files(self) -> None:
        """Catches a validator that lets an incomplete repository pass."""
        validator = load_validator()
        with tempfile.TemporaryDirectory() as directory:
            errors = validator.validate_required_files(Path(directory))
        self.assertEqual(len(validator.REQUIRED_FILES), len(errors))

    def test_validator_cli_passes_the_repository(self) -> None:
        """Catches a CLI that disagrees with the reusable validation functions."""
        script = ROOT / "scripts" / "validate_repo.py"
        self.assertTrue(script.is_file(), "scripts/validate_repo.py must exist")
        completed = subprocess.run(
            ["python3", str(script)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertEqual("Repository validation passed.", completed.stdout.strip())

    def test_skill_routes_all_three_user_modes(self) -> None:
        """Catches an entrypoint that silently drops one supported mode."""
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for mode in ("只诊断", "逐步共创", "生成完整版"):
            self.assertIn(mode, text)
        self.assertIn("先诊断", text)

    def test_interview_contract_allows_only_one_question_per_turn(self) -> None:
        """Catches a playbook that degrades into a multi-question form."""
        path = ROOT / "references" / "interview-playbook.md"
        self.assertTrue(path.is_file(), "interview playbook must exist")
        text = path.read_text(encoding="utf-8")
        self.assertIn("每轮最多一个问题", text)
        self.assertIn("一到两句", text)

    def test_user_correction_reorders_the_interview(self) -> None:
        """Catches persistence with an interpretation the user has rejected."""
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("用户纠正", text)
        self.assertIn("立即废弃", text)
        self.assertIn("重新排序", text)

    def test_short_confirmation_advances_to_the_next_step(self) -> None:
        """Catches treating a short confirmation as missing information."""
        path = ROOT / "references" / "interview-playbook.md"
        self.assertTrue(path.is_file(), "interview playbook must exist")
        text = path.read_text(encoding="utf-8")
        for token in ("`1`", "`继续`", "`可以`"):
            self.assertIn(token, text)
        self.assertIn("进入下一步", text)

    def test_transcripts_and_fragments_enter_material_first_mode(self) -> None:
        """Catches rejection of useful input merely because no draft exists."""
        path = ROOT / "references" / "interview-playbook.md"
        self.assertTrue(path.is_file(), "interview playbook must exist")
        text = path.read_text(encoding="utf-8")
        self.assertIn("语音逐字稿", text)
        self.assertIn("零散素材", text)
        self.assertIn("从素材建立初稿", text)

    def test_default_standard_defers_to_user_supplied_rules(self) -> None:
        """Catches fallback guidance overriding the creator's own standard."""
        path = ROOT / "references" / "default-video-standard.md"
        self.assertTrue(path.is_file(), "default video standard must exist")
        text = path.read_text(encoding="utf-8")
        self.assertIn("用户当前指令 > 用户提供的标准 > 本默认标准", text)
        self.assertIn("只补充未覆盖部分", text)

    def test_default_standard_covers_audience_goal_and_visible_evidence(self) -> None:
        """Catches a standard that optimizes form without relevance or proof."""
        path = ROOT / "references" / "default-video-standard.md"
        self.assertTrue(path.is_file(), "default video standard must exist")
        text = path.read_text(encoding="utf-8")
        for question in ("这件事跟我有关吗？", "我能马上听懂吗？", "我看完能拿走什么？"):
            self.assertIn(question, text)
        self.assertIn("一个主要目标", text)
        self.assertIn("可见证据", text)

    def test_final_review_gates_truth_voice_privacy_and_call_to_action(self) -> None:
        """Catches synthesis that is publishable in form but unsafe or untrue."""
        path = ROOT / "references" / "final-review-checklist.md"
        self.assertTrue(path.is_file(), "final review checklist must exist")
        text = path.read_text(encoding="utf-8")
        for check in ("事实", "原话与语感", "隐私", "CTA"):
            self.assertIn(check, text)
        for status in ("`ready`", "`ready with noted gaps`", "`not ready—continue interview`"):
            self.assertIn(status, text)
        self.assertIn("只能返回一个", text)

    def test_every_adapter_routes_to_the_canonical_skill(self) -> None:
        """Catches an adapter that forks or bypasses the canonical workflow."""
        for filename in ("AGENTS.md", "CLAUDE.md", "PROMPT.md"):
            with self.subTest(adapter=filename):
                path = ROOT / filename
                self.assertTrue(path.is_file(), f"{filename} must exist")
                text = path.read_text(encoding="utf-8")
                self.assertIn("[SKILL.md](SKILL.md)", text)
                non_empty = [line for line in text.splitlines() if line.strip()]
                self.assertLessEqual(len(non_empty), 120, "adapter duplicates too much workflow")

    def test_adapter_markdown_references_exist(self) -> None:
        """Catches a platform entrypoint that sends an Agent to a missing file."""
        for filename in ("AGENTS.md", "CLAUDE.md", "PROMPT.md"):
            path = ROOT / filename
            self.assertTrue(path.is_file(), f"{filename} must exist")
            for target in MARKDOWN_LINK.findall(path.read_text(encoding="utf-8")):
                relative = target.split("#", 1)[0]
                self.assertTrue((ROOT / relative).is_file(), f"{filename} -> {relative}")

    def test_openai_metadata_is_quoted_and_invokes_the_skill(self) -> None:
        """Catches malformed UI metadata or a prompt that omits explicit invocation."""
        text = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertRegex(text, r'(?m)^\s*display_name:\s*"个人 IP 爆款脚本引导挖掘"\s*$')
        self.assertRegex(text, r'(?m)^\s*short_description:\s*"[^"]+"\s*$')
        self.assertRegex(text, r'(?m)^\s*default_prompt:\s*"[^\n]*\$personal-ip-script-coach[^\n]*"\s*$')
        self.assertRegex(text, r"(?m)^\s*allow_implicit_invocation:\s*true\s*$")

    def test_prompt_fallback_preserves_critical_rules_without_file_access(self) -> None:
        """Catches a pasted fallback that loses precedence, confirmations, or privacy."""
        text = (ROOT / "PROMPT.md").read_text(encoding="utf-8")
        fallback = text.split("## Concise fallback when file navigation is unavailable", 1)[1]
        for phrase in ("current instruction", "user-supplied standard", "`1`", "avatar", "display name"):
            self.assertIn(phrase, fallback)

    def test_readme_covers_supported_platforms_scope_and_privacy(self) -> None:
        """Catches a public guide that cannot be installed or overclaims results."""
        path = ROOT / "README.md"
        self.assertTrue(path.is_file(), "README.md must exist")
        text = path.read_text(encoding="utf-8")
        for platform in ("Codex", "Claude Code", "WorkBuddy", "豆包", "通用 Agent"):
            self.assertIn(platform, text)
        for section in ("三种模式", "快速开始", "隐私", "贡献"):
            self.assertIn(section, text)
        self.assertIn("不保证爆款", text)
        self.assertIn("personal-ip-script-coach", text)
        self.assertIn("tests/behavioral-scenarios.md", text)
        self.assertIn("tests/smoke-test-results.md", text)

    def test_license_is_standard_mit_for_pl(self) -> None:
        """Catches a release without the approved redistribution terms."""
        path = ROOT / "LICENSE"
        self.assertTrue(path.is_file(), "LICENSE must exist")
        text = path.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("MIT License\n"))
        self.assertIn("Copyright (c) 2026 PL", text)
        self.assertIn("THE SOFTWARE IS PROVIDED \"AS IS\"", text)

    def test_demo_shows_the_complete_coaching_arc(self) -> None:
        """Catches a demo that skips the adaptive behavior users need to assess."""
        path = ROOT / "examples" / "complete-demo.md"
        self.assertTrue(path.is_file(), "complete demo must exist")
        text = path.read_text(encoding="utf-8")
        for stage in ("弱稿", "诊断", "用户纠正", "临时版", "就绪检查", "最终口播稿"):
            self.assertIn(stage, text)
        self.assertGreaterEqual(len(re.findall(r"(?m)^### 第[一二三四五六七八九十]+轮", text)), 5)
        self.assertIn("本示例完全虚构", text)
        self.assertIn("每轮一个问题", text)

    def test_behavior_pack_covers_all_seven_risk_scenarios(self) -> None:
        """Catches a release that omits one of the approved behavior risks."""
        path = ROOT / "tests" / "behavioral-scenarios.md"
        self.assertTrue(path.is_file(), "behavioral scenarios must exist")
        text = path.read_text(encoding="utf-8")
        self.assertEqual(7, len(re.findall(r"(?m)^## Scenario [1-7]:", text)))
        for case in (
            "No case",
            "User correction",
            "Oral story",
            "Transcript only",
            "Conflicting standard",
            "Reply `1`",
            "Private screenshot",
        ):
            self.assertIn(case, text)
        for rule in ("one question maximum", "no fabricated fact", "standard precedence", "no premature completion"):
            self.assertIn(rule, text)

    def test_release_validator_rejects_empty_markdown(self) -> None:
        """Catches a structurally present but unusable documentation file."""
        validator = load_validator()
        self.assertTrue(hasattr(validator, "validate_empty_files"))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "empty.md").write_text("  \n", encoding="utf-8")
            errors = validator.validate_empty_files(root)
        self.assertEqual(["Empty Markdown file: empty.md"], errors)

    def test_project_map_covers_every_release_file(self) -> None:
        """Catches new public files that become invisible to Vault navigation."""
        validator = load_validator()
        self.assertTrue(hasattr(validator, "validate_project_map_coverage"))
        self.assertEqual([], validator.validate_project_map_coverage(ROOT))

    def test_final_required_file_set_is_complete(self) -> None:
        """Catches a partial release that passes with a missing adapter or evidence file."""
        validator = load_validator()
        expected = {
            "README.md",
            "LICENSE",
            "ProjectMap.md",
            "SKILL.md",
            "AGENTS.md",
            "CLAUDE.md",
            "PROMPT.md",
            "agents/openai.yaml",
            "references/default-video-standard.md",
            "references/interview-playbook.md",
            "references/final-review-checklist.md",
            "examples/complete-demo.md",
            "scripts/validate_repo.py",
            "tests/__init__.py",
            "tests/test_repository_contract.py",
            "tests/behavioral-scenarios.md",
            "tests/smoke-test-results.md",
        }
        self.assertEqual(expected, set(validator.REQUIRED_FILES))
        self.assertEqual([], validator.validate_required_files(ROOT))


if __name__ == "__main__":
    unittest.main()
