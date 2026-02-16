#!/usr/bin/env python3
"""
YAML Excel Converter - Entry Point
Run this file to start the application
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yamlconverter.gui.main import main

if __name__ == '__main__':
    main()
