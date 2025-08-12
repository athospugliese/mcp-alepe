#!/usr/bin/env python3
"""
Simple entry point for Railway deployment.
"""
import sys
import os

# Add src to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import main

if __name__ == "__main__":
    main()