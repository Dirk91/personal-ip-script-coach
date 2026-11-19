#!/usr/bin/env python3
"""Validate the public repository without third-party dependencies."""

from __future__ import annotations

import pathlib
import re
from urllib.parse import unquote


IGNORED_DIRECTORIES = {".git", ".superpowers", "__pycache__"}
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".py", ".txt"}
REQUIRED_FILES = ("SKILL.md", "agents/openai.yaml", "ProjectMap.md")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def repository_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def find_markdown_links(text: str) -> list[str]:
    return MARKDOWN_LINK.findall(text)


def iter_public_text_files(root: pathlib.Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if IGNORED_DIRECTORIES.intersection(path.relative_to(root).parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def validate_required_files(root: pathlib.Path) -> list[str]:
    return [f"Missing required file: {relative}" for relative in REQUIRED_FILES if not (root / relative).is_file()]


def validate_relative_links(root: pathlib.Path) -> list[str]:
    errors: list[str] = []
    for path in iter_public_text_files(root):
        if path.suffix.lower() != ".md":
            continue
        for raw_target in find_markdown_links(path.read_text(encoding="utf-8")):
            target = raw_target.strip().split("#", 1)[0].strip()
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            if not (path.parent / unquote(target)).resolve().exists():
                errors.append(f"Broken relative link: {path.relative_to(root)} -> {target}")
    return errors


def validate_privacy(root: pathlib.Path) -> list[str]:
    markers = ("/" + "Users" + "/", "/var/" + "folders" + "/")
    errors: list[str] = []
    for path in iter_public_text_files(root):
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker in text:
                errors.append(f"Private path in {path.relative_to(root)}: {marker}")
    return errors


def validate_placeholders(root: pathlib.Path) -> list[str]:
    markers = ("TO" + "DO", "TB" + "D")
    errors: list[str] = []
    for path in iter_public_text_files(root):
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if re.search(rf"\b{re.escape(marker)}\b", text, flags=re.IGNORECASE):
                errors.append(f"Unfinished marker in {path.relative_to(root)}: {marker}")
    return errors


def main() -> int:
    root = repository_root()
    errors: list[str] = []
    for check in (
        validate_required_files,
        validate_relative_links,
        validate_privacy,
        validate_placeholders,
    ):
        errors.extend(check(root))
    if errors:
        for error in errors:
            print(f"- {error}")
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
