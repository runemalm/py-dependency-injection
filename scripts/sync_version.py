import re
from pathlib import Path

VERSION_FILE = Path("src/dependency_injection/version.py")
PYPROJECT_FILE = Path("pyproject.toml")


def get_version():
    content = VERSION_FILE.read_text()
    match = re.search(r'__version__ = ["\']([^"\']+)["\']', content)
    if not match:
        raise RuntimeError("Version not found in version.py")
    return match.group(1)


def update_pyproject(version: str):
    content = PYPROJECT_FILE.read_text()
    new_content = re.sub(r'version\s*=\s*"[^"]+"', f'version = "{version}"', content)
    PYPROJECT_FILE.write_text(new_content)
    print(f"✅ Synced pyproject.toml version to {version}")


if __name__ == "__main__":
    version = get_version()
    update_pyproject(version)
