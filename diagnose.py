#!/usr/bin/env python
"""
Diagnostic script to check Python environment and dependencies
"""

import sys
import subprocess

print("="*60)
print("Python Environment Diagnostic")
print("="*60)

print(f"\nPython Executable: {sys.executable}")
print(f"Python Version: {sys.version}")
print(f"Python Prefix: {sys.prefix}")

print("\n" + "="*60)
print("Checking Required Packages")
print("="*60)

packages = ['reportlab', 'APScheduler', 'openai', 'anthropic', 'requests']

for pkg in packages:
    try:
        mod = __import__(pkg)
        version = getattr(mod, '__version__', 'unknown')
        print(f"✓ {pkg:20} - installed (version: {version})")
    except ImportError:
        print(f"✗ {pkg:20} - NOT installed")

print("\n" + "="*60)
print("Installing Missing Packages")
print("="*60)

missing = []
for pkg in ['reportlab', 'APScheduler']:
    try:
        __import__(pkg)
    except ImportError:
        missing.append(pkg)

if missing:
    print(f"\nMissing packages: {', '.join(missing)}")
    print(f"\nInstalling with: pip install {' '.join(missing)}")
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install'] + missing,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ Installation successful!")
    else:
        print("✗ Installation failed:")
        print(result.stderr)
else:
    print("All required packages are already installed!")

print("\n" + "="*60)
print("Final Check")
print("="*60)

try:
    from reportlab.lib import colors
    print("✓ reportlab can be imported successfully")
except ImportError as e:
    print(f"✗ reportlab import failed: {e}")

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    print("✓ APScheduler can be imported successfully")
except ImportError as e:
    print(f"✗ APScheduler import failed: {e}")

print("\n✓ Diagnostic complete!")
