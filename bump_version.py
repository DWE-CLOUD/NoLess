#!/usr/bin/env python3
"""
Version bumping utility for NoLess
Usage: python bump_version.py [major|minor|patch]
"""
import re
import sys
from pathlib import Path


def get_current_version(setup_file: Path) -> str:
    """Extract current version from setup.py"""
    content = setup_file.read_text(encoding="utf-8")
    match = re.search(r'version="(\d+\.\d+\.\d+)"', content)
    if not match:
        raise ValueError("Could not find version in setup.py")
    return match.group(1)


def bump_version(version: str, part: str) -> str:
    """Bump version number"""
    major, minor, patch = map(int, version.split("."))
    
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid part: {part}. Use 'major', 'minor', or 'patch'")
    
    return f"{major}.{minor}.{patch}"


def update_version_in_file(setup_file: Path, old_version: str, new_version: str):
    """Update version in setup.py"""
    content = setup_file.read_text(encoding="utf-8")
    new_content = content.replace(
        f'version="{old_version}"',
        f'version="{new_version}"'
    )
    setup_file.write_text(new_content, encoding="utf-8")


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["major", "minor", "patch"]:
        print("Usage: python bump_version.py [major|minor|patch]")
        print("\nExamples:")
        print("  python bump_version.py patch  # 0.1.0 -> 0.1.1")
        print("  python bump_version.py minor  # 0.1.0 -> 0.2.0")
        print("  python bump_version.py major  # 0.1.0 -> 1.0.0")
        sys.exit(1)
    
    part = sys.argv[1]
    setup_file = Path(__file__).parent / "setup.py"
    
    if not setup_file.exists():
        print(f"Error: {setup_file} not found")
        sys.exit(1)
    
    try:
        current_version = get_current_version(setup_file)
        new_version = bump_version(current_version, part)
        
        print(f"Current version: {current_version}")
        print(f"New version: {new_version}")
        
        response = input("Update version? (y/n): ")
        if response.lower() == "y":
            update_version_in_file(setup_file, current_version, new_version)
            print(f"✅ Version updated to {new_version}")
            print(f"\nNext steps:")
            print(f"  1. git add setup.py")
            print(f"  2. git commit -m 'Bump version to {new_version}'")
            print(f"  3. git tag -a v{new_version} -m 'Release v{new_version}'")
            print(f"  4. git push origin main --tags")
        else:
            print("❌ Version update cancelled")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
