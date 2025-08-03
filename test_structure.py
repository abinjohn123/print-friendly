#!/usr/bin/env python3
"""
Test script to verify project structure without requiring dependencies
"""

import os
import sys
from pathlib import Path

def test_project_structure():
    """Test that all required files exist"""
    required_files = [
        'main.py',
        'pdf_processor.py', 
        'image_processor.py',
        'utils.py',
        'requirements.txt',
        'CLAUDE.md'
    ]
    
    print("Testing project structure...")
    all_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"[OK] {file}")
        else:
            print(f"[MISSING] {file}")
            all_exist = False
    
    return all_exist

def test_imports():
    """Test basic Python syntax without external dependencies"""
    print("\nTesting Python syntax...")
    
    try:
        # Test basic imports that should work
        import argparse
        import sys
        import os
        from pathlib import Path
        print("[OK] Standard library imports work")
        
        # Test file syntax by compiling without executing
        with open('main.py', 'r') as f:
            compile(f.read(), 'main.py', 'exec')
        print("[OK] main.py syntax is valid")
        
        with open('utils.py', 'r') as f:
            compile(f.read(), 'utils.py', 'exec')
        print("[OK] utils.py syntax is valid")
        
        return True
        
    except SyntaxError as e:
        print(f"[ERROR] Syntax error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

def test_requirements():
    """Check requirements.txt format"""
    print("\nTesting requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
        
        if len(lines) >= 4:
            print(f"[OK] Found {len(lines)} dependencies")
            for line in lines:
                if line.strip():
                    print(f"  - {line.strip()}")
            return True
        else:
            print("[ERROR] Requirements file seems incomplete")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error reading requirements.txt: {e}")
        return False

if __name__ == "__main__":
    print("Print Friendly - Project Structure Test")
    print("=" * 40)
    
    structure_ok = test_project_structure()
    syntax_ok = test_imports()
    requirements_ok = test_requirements()
    
    print("\n" + "=" * 40)
    if structure_ok and syntax_ok and requirements_ok:
        print("SUCCESS: All tests passed! Project structure is ready.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Test with a sample PDF: python main.py sample.pdf -o output.pdf")
    else:
        print("FAILED: Some tests failed. Please fix the issues above.")
        sys.exit(1)