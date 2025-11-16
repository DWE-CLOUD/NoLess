#!/usr/bin/env python3
"""
Pre-deployment checks for NoLess package
Run this before committing a new release
"""
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"🔍 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.stdout:
            print(result.stdout)
        
        if result.returncode != 0:
            print(f"❌ FAILED: {description}")
            if result.stderr:
                print(result.stderr)
            return False
        
        print(f"✅ PASSED: {description}")
        return True
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def check_version_sync():
    """Check if version in __init__.py and setup.py match"""
    print(f"\n{'='*60}")
    print(f"🔍 Checking version synchronization")
    print(f"{'='*60}")
    
    init_file = Path("noless/__init__.py")
    setup_file = Path("setup.py")
    
    try:
        init_content = init_file.read_text()
        setup_content = setup_file.read_text()
        
        import re
        init_version = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', init_content)
        setup_version = re.search(r'version="([^"]+)"', setup_content)
        
        if not init_version or not setup_version:
            print("❌ Could not find version strings")
            return False
        
        init_ver = init_version.group(1)
        setup_ver = setup_version.group(1)
        
        print(f"  __init__.py version: {init_ver}")
        print(f"  setup.py version:    {setup_ver}")
        
        if init_ver != setup_ver:
            print(f"❌ FAILED: Version mismatch!")
            return False
        
        print(f"✅ PASSED: Versions match ({init_ver})")
        return True
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("🚀 NoLess Pre-Deployment Checks")
    print("="*60)
    
    checks = []
    
    # Check version synchronization
    checks.append(check_version_sync())
    
    # Run tests
    checks.append(run_command(
        "python -m unittest discover -s tests",
        "Running unit tests"
    ))
    
    # Check if dist directory should be cleaned
    if Path("dist").exists():
        print("\n⚠️  Warning: dist/ directory exists. Clean it before building:")
        print("   Remove-Item -Recurse -Force dist")
    
    # Try to build
    checks.append(run_command(
        "python -m build",
        "Building package"
    ))
    
    # Check built packages
    if Path("dist").exists():
        checks.append(run_command(
            "twine check dist/*",
            "Validating package with twine"
        ))
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    passed = sum(checks)
    total = len(checks)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All checks passed! Ready to deploy.")
        print("\nNext steps:")
        print("  1. git add .")
        print("  2. git commit -m 'Prepare release vX.Y.Z'")
        print("  3. git tag -a vX.Y.Z -m 'Release vX.Y.Z'")
        print("  4. git push origin main --tags")
        return 0
    else:
        print(f"\n❌ {total - passed} check(s) failed. Please fix before deploying.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
