"""Read incident logs from the configured directory with source line numbers."""
from bugpilot.config import INCIDENTS_DIR


def read_log(filename: str) -> str:
    """Read an incident log by filename and return numbered lines."""
    path = (INCIDENTS_DIR / filename).resolve()
    if not path.is_relative_to(INCIDENTS_DIR.resolve()) or path.suffix != ".log":
        raise ValueError("Choose a .log file inside data/incidents.")
    return "\n".join(
        f"{number}: {line}"
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
    )
