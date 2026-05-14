from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = REPO_ROOT / "requirements.txt"
LOCKFILE = REPO_ROOT / "uv.lock"


def main() -> int:
    errors: list[str] = []

    if not LOCKFILE.exists():
        errors.append("uv.lock is missing. Run `uv lock` and commit the result.")

    if REQUIREMENTS.exists():
        package_lines = [
            (line_number, line.strip())
            for line_number, line in enumerate(REQUIREMENTS.read_text(encoding="utf-8").splitlines(), start=1)
            if line.strip() and not line.lstrip().startswith("#")
        ]
        for line_number, line in package_lines:
            errors.append(
                f"requirements.txt:{line_number} contains `{line}`. "
                "Dependencies must be managed in pyproject.toml with uv."
            )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Dependency policy check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
