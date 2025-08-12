#!/usr/bin/env python3
"""Test script for Railway deployment."""

import os
import sys

# Add src to Python path
sys.path.insert(0, 'src')

# Set PORT environment variable to test Railway mode
os.environ['PORT'] = '8000'

print(f"PORT environment variable: {os.environ.get('PORT')}")
print("Starting Railway test...")

try:
    from src.main import main
    main()
except KeyboardInterrupt:
    print("Server stopped.")
except Exception as e:
    print(f"Error: {e}")