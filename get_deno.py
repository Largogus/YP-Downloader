import sys
from pathlib import Path


def get_deno():
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    name = "deno.exe" if sys.platform == "win32" else "deno"
    path = base / name
    return str(path) if path.exists() else None