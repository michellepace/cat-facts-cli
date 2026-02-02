"""Tests for CLI entry point."""

from typer.testing import CliRunner

from cat_facts_cli.cli import app

runner = CliRunner()


def test_default_invocation_prints_greeting() -> None:
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello from cat-facts-cli!" in result.output
