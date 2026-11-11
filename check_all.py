import subprocess
import sys
from pathlib import Path

COMMANDS = (
    ["ruff", "check", "."],
    ["black", "--check", "."],
    ["mypy", "--strict", "."],
    ["pytest", "-q"],
)


def main() -> int:
    failed = 0
    root = Path(__file__).parent
    lab_dirs = sorted([d for d in root.glob("lab0*") if d.is_dir() and "example_repo" not in str(d)])
    if not lab_dirs:
        return 1
    for lab in lab_dirs:
        for cmd in COMMANDS:
            result = subprocess.run([sys.executable, "-m", *cmd], cwd=lab)
            status = "ok" if result.returncode == 0 else "FAIL"
            failed += result.returncode != 0
            print(f"[{lab.name}] {' '.join(cmd)}: {status}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
