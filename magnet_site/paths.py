"""Repository paths, independent of the caller's working directory."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
DATA = ROOT / "data" / "magnets.csv"
DOS = ROOT / "data" / "dos"
LEGACY_DATA = ROOT / "data" / "legacy"
OUTPUT = ROOT / "docs"
