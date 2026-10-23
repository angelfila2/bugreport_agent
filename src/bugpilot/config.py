"""Local data paths for incident investigation."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
INCIDENTS_DIR = DATA_DIR / "incidents"
NOTES_DIR = DATA_DIR / "notes"
MAX_AGENT_STEPS = 6
