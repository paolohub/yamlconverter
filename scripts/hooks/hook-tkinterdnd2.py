"""
Custom PyInstaller hook for tkinterdnd2
Fixes the warning about win-x64 vs win64 directory naming
"""
from PyInstaller.utils.hooks import collect_data_files
import os
import sys

# Collect all data files from tkinterdnd2
datas = collect_data_files('tkinterdnd2', include_py_files=False)

# The tkdnd native libraries are in the tkdnd subdirectory
# Platform-specific subdirectories:
# - Windows: win64 (not win-x64)
# - Linux: linux64
# - macOS: osx64

# This hook prevents the warning:
# "WARNING: hook-tkinterdnd2: platform-specific sub-directory 'tkdnd/win-x64' does not exist!"
# by correctly handling the actual directory structure used by tkinterdnd2
