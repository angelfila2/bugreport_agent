"""Keyword retrieval for local troubleshooting notes."""
import re

from bugpilot.config import NOTES_DIR


def search_notes(query: str) -> list[dict]:
    """Search troubleshooting notes for guidance relevant to a query."""
    terms = set(re.findall(r"\w+", query.lower()))
    matches = []
    for path in sorted(NOTES_DIR.glob("*.md")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            score = len(terms & set(re.findall(r"\w+", line.lower())))
            if score:
                matches.append({"source": path.name, "line_number": number,
                                "excerpt": line, "score": score})
    if not matches:
        return []

    best_score = max(match["score"] for match in matches)

    return [
        match for match in matches
        if match["score"] == best_score
    ][:5]
