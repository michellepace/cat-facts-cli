"""Tests for Play module."""

from cat_facts_cli.play import add


def test_add_two_positive_numbers() -> None:
    """Test adding two positive numbers."""
    result = add(2, 3)
    assert result == 5
