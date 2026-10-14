"""Tests for AI-driven walkthrough validation helpers."""

from __future__ import annotations

import json
import shlex
import sys
from pathlib import Path

import pytest

from tools import validate_walkthroughs
from tools.validate_walkthroughs import build_prompt, run_ai_cli


def test_build_prompt_includes_rules_filename_and_walkthrough() -> None:
    prompt = build_prompt(
        "## Summary must exist.",
        "# Example\n\n## Summary\nContent",
        "Example-walkthrough.md",
    )
    input_data = json.loads(prompt.split("Input data (JSON):\n", maxsplit=1)[1])

    assert input_data == {
        "filename": "Example-walkthrough.md",
        "rules": "## Summary must exist.",
        "walkthrough": "# Example\n\n## Summary\nContent",
    }
    assert "Do not modify the walkthrough." in prompt


def test_run_ai_cli_passes_prompt_and_returns_output() -> None:
    command = (
        f"{shlex.quote(sys.executable)} -c "
        f"{shlex.quote('import sys; print(sys.argv[1])')} {{prompt}}"
    )

    assert run_ai_cli(command, "test prompt") == "test prompt\n"


def test_run_ai_cli_requires_prompt_placeholder() -> None:
    with pytest.raises(ValueError, match="must include a \\{prompt\\} placeholder"):
        run_ai_cli("copilot -p", "test prompt")


def test_main_writes_one_report_for_each_walkthrough(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    modules_dir = tmp_path / "modules"
    modules_dir.mkdir()
    (modules_dir / "B-walkthrough.md").write_text("B content", encoding="utf-8")
    (modules_dir / "A-walkthrough.md").write_text("A content", encoding="utf-8")
    (modules_dir / "ignored.md").write_text("Ignore me", encoding="utf-8")
    rules_file = tmp_path / "rules.md"
    rules_file.write_text("Validation instructions", encoding="utf-8")
    output_dir = tmp_path / "results"
    prompts: list[str] = []

    def fake_run_ai_cli(command: str, prompt: str) -> str:
        prompts.append(prompt)
        return f"Validated {len(prompts)}\n"

    monkeypatch.setattr(validate_walkthroughs, "run_ai_cli", fake_run_ai_cli)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "validate_walkthroughs.py",
            "--modules-dir",
            str(modules_dir),
            "--rules-file",
            str(rules_file),
            "--output-dir",
            str(output_dir),
            "--command",
            "test-cli {prompt}",
        ],
    )

    validate_walkthroughs.main()

    assert (output_dir / "A-walkthrough-validation.md").read_text(encoding="utf-8") == (
        "Validated 1\n"
    )
    assert (output_dir / "B-walkthrough-validation.md").read_text(encoding="utf-8") == (
        "Validated 2\n"
    )
    assert len(prompts) == 2
    assert "Validation instructions" in prompts[0]
    assert "A content" in prompts[0]
    assert "B content" in prompts[1]
    assert "ignored.md" not in capsys.readouterr().out
