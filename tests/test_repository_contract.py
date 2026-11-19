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
        self.assertEqual(3, len(errors))

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


if __name__ == "__main__":
    unittest.main()
