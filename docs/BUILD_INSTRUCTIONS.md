# Build Instructions - YAML Excel Converter

## Quick Build

To create the Windows executable, simply run:

```batch
scripts\build.bat
```

The executable will be available in `dist/YAMLExcelConverter.exe` (~11.5 MB)

## Build Requirements

- Python 3.8+
- Virtual environment in `.venv/`
- PyInstaller installed: `pip install pyinstaller`
- All dependencies from `requirements.txt`

## Initial Setup

If it's the first time:

```batch
# 1. Create virtual environment
python -m venv .venv

# 2. Activate environment
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install PyInstaller
pip install pyinstaller

# 5. Build
scripts\build.bat
```

## Build Files

### scripts/build.bat
Automated batch script that:
1. Activates virtual environment
2. Cleans previous builds
3. Executes PyInstaller with optimized configuration
4. Verifies success and displays executable info

### scripts/build_exe.spec
PyInstaller configuration with:
- **Optimizations**: Excluded pandas/numpy (25+ MB saved)
- **Hidden imports**: Only necessary modules
- **Data files**: Native tkinterdnd2 files for drag & drop
- **Runtime hooks**: Fix for tkdnd in packaged environment
- **Excludes**: Heavy unused libraries

### scripts/pyi_rth_tkinterdnd2.py
Runtime hook to configure tkdnd when the app is packaged.
Resolves the native library loading issue.

### scripts/version_info.txt (optional)
Version info file for Windows.
To use it, uncomment `version_file=version_info.txt` in scripts/build_exe.spec

## Manual Build

If you prefer to run manually:

```batch
# Activate environment
.venv\Scripts\activate

# Clean
rmdir /s /q build dist

# Build
pyinstaller scripts/build_exe.spec --clean
```

## Optimizations Applied

### Exclusions (-69% size)
- ❌ pandas (15+ MB)
- ❌ numpy (10+ MB)
- ❌ matplotlib, scipy, PIL
- ❌ pytest, IPython, jupyter
- ❌ Standard modules (yaml_to_excel, excel_to_yaml)

### Core Dependencies Only
- ✅ openpyxl (lightweight, replaces pandas for Excel)
- ✅ pyyaml (YAML parsing)
- ✅ tkinterdnd2 (drag & drop GUI)
- ✅ python-gnupg (GPG encryption)

### Result
- **Size**: 11.5 MB (vs 37.4 MB original)
- **Startup**: Faster (no pandas/numpy loading)
- **Functionality**: Complete (custom format + GPG)

## Troubleshooting

### Error: "Virtual environment not found"
```batch
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller
```

### Error: "PyInstaller not found"
```batch
.venv\Scripts\activate
pip install pyinstaller
```

### Error: "Unable to load tkdnd library"
Verify that `pyi_rth_tkinterdnd2.py` is present and referenced in build_exe.spec

### Slow build
First build can take 2-5 minutes. Subsequent builds are faster thanks to caching.

## Customizations

### Add Icon
1. Create `icon.ico` file (256x256 or 128x128)
2. In `build_exe.spec`, change: `icon=None` → `icon='icon.ico'`

### Add Version Info
1. In `build_exe.spec`, change: `version_file=None` → `version_file='version_info.txt'`
2. Modify `version_info.txt` with your info

### Modify Executable Name
In `build_exe.spec`, change: `name='YAMLExcelConverter'` → `name='YourName'`

## Post-Build Testing

After building, test:
1. ✅ Application startup
2. ✅ Drag & drop files
3. ✅ Conversion YAML → Excel
4. ✅ Conversion Excel → YAML
5. ✅ GPG decrypt (if you have .gpg files)
6. ✅ GPG encrypt
7. ✅ Duplicate key detection

## Distribution

The executable in `dist/YAMLExcelConverter.exe` is:
- **Standalone**: No Python installation required
- **Portable**: Can be copied to any Windows PC
- **Requirements**: Only Windows 10+ and GPG (for encryption)

Distribute along with:
- `dist/README.txt` - User guide
- Templates (optional): `secrets.rlist.yml`, `secrets.rlist.xlsx`
