#!/usr/bin/env python
"""Start the Fashion Sales Agent backend"""
import os
import sys
import subprocess

# Ensure we're in the backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)

# Set environment variables
os.environ['USE_FAKE_REDIS'] = 'true'

# Run uvicorn
cmd = [
    sys.executable, '-m', 'uvicorn',
    'app:app',
    '--reload',
    '--log-level', 'info',
    '--host', '127.0.0.1',
    '--port', '8000'
]

print(f"Starting server from: {backend_dir}")
print(f"Command: {' '.join(cmd)}")
print()

subprocess.run(cmd)
