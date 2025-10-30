# tests/conftest.py
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # katalog projektu
sys.path.insert(0, str(ROOT))               # pozwala na "import src.xxx"
sys.path.insert(0, str(ROOT / "src"))       # ewentualnie bez prefiksu "src"