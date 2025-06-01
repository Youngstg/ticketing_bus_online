#!/usr/bin/env python3
"""
Test runner script for backend_ticketing project.
Runs all tests and generates coverage report.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a shell command and return the result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=Path(__file__).parent
        )
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Return code: {result.returncode}")
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    """Main test runner function."""
    print("Backend Ticketing Test Runner")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("setup.py"):
        print("Error: Please run this script from the backend_ticketing root directory")
        sys.exit(1)
    
    # Install dependencies if needed
    print("Installing test dependencies...")
    deps_ok = run_command(
        "pip install pytest pytest-cov webtest",
        "Installing test dependencies"
    )
    
    if not deps_ok:
        print("Warning: Could not install all dependencies")
    
    # Run tests with coverage
    test_commands = [
        {
            "command": "python -m pytest tests/ -v",
            "description": "Running basic tests"
        },
        {
            "command": "python -m pytest tests/ -v --cov=backend_ticketing --cov-report=term-missing",
            "description": "Running tests with coverage report"
        },
        {
            "command": "python -m pytest tests/ --cov=backend_ticketing --cov-report=html --cov-report=term",
            "description": "Generating HTML coverage report"
        }
    ]
    
    success_count = 0
    
    for test_cmd in test_commands:
        success = run_command(test_cmd["command"], test_cmd["description"])
        if success:
            success_count += 1
        else:
            print(f"Failed: {test_cmd['description']}")
    
    print(f"\n{'='*60}")
    print(f"Test Summary: {success_count}/{len(test_commands)} commands succeeded")
    
    if success_count >= 2:  # At least basic tests and coverage
        print("✅ Tests completed successfully!")
        print("\nTo view detailed HTML coverage report, open: htmlcov/index.html")
    else:
        print("❌ Some tests failed. Check the output above for details.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())