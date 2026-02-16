"""
Main entry point for YAML Excel Converter CLI.
"""
import sys
import os

# Add src directory to path for development
if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from yamlconverter.gui.main import main
    main()
