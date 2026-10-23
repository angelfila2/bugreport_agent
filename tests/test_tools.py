"""Checks for log access, path restrictions, and evidence retrieval."""
import pytest

from bugpilot.tools import read_log, search_notes


def test_read_log_preserves_evidence_line_numbers():
    assert "2: " in read_log("01_database_unavailable.log")
    assert "connection refused" in read_log("01_database_unavailable.log")


def test_read_log_blocks_path_escape():
    with pytest.raises(ValueError):
        read_log("../notes/troubleshooting.md")


def test_search_finds_citable_unique_constraint_guidance():
    matches = search_notes("duplicate key users_email_key")
    assert matches[0]["source"] == "troubleshooting.md"
    assert "unique email" in matches[0]["excerpt"]
    assert matches[0]["line_number"] > 0
