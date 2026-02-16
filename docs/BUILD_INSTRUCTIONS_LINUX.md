# Build Instructions - YAML Excel Converter (Linux AppImage)

## Quick Build

To create the Linux AppImage, run:

```bash
chmod +x scripts/build_appimage.sh
./scripts/build_appimage.sh
```

The AppImage will be available in `YAMLExcelConverter-x86_64.AppImage` (~12 MB)

## Build Requirements

### System Packages
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-venv python3-tk gnupg wget

# Optional for creating icon
sudo apt-get install imagemagick

# Fedora/RHEL
sudo dnf install python3 python3-tkinter gnupg wget

# Arch Linux
sudo pacman -S python python-pip tk gnupg wget
```

### Python
- Python 3.8+
- Virtual environment (created automatically by the script)
- All dependencies from `requirements.txt`

## Initial Setup

If it's the first time:

```bash
# 1. Clone or copy the repository
cd yamlconverter

# 2. Make the script executable
chmod +x scripts/build_appimage.sh

# 3. Run the build
./scripts/build_appimage.sh
```

The script automatically:
1. Creates virtual environment (if it doesn't exist)
2. Installs Python dependencies
3. Installs PyInstaller
4. Compiles the application
5. Creates the AppDir structure
6. Downloads appimagetool (if necessary)
7. Generates the AppImage

## Running AppImage

```bash
# Make executable (first time only)
chmod +x YAMLExcelConverter-x86_64.AppImage

# Run
./YAMLExcelConverter-x86_64.AppImage
```

## System Installation

The AppImage doesn't require installation, but if you want better integration:

### Method 1: Copy to /opt (Recommended)
```bash
sudo cp YAMLExcelConverter-x86_64.AppImage /opt/
sudo chmod +x /opt/YAMLExcelConverter-x86_64.AppImage
```

### Method 2: Copy to ~/Applications
```bash
mkdir -p ~/Applications
cp YAMLExcelConverter-x86_64.AppImage ~/Applications/
chmod +x ~/Applications/YAMLExcelConverter-x86_64.AppImage
```

### Desktop Integration
Create a desktop launcher:

```bash
cat > ~/.local/share/applications/yamlexcelconverter.desktop << EOF
[Desktop Entry]
Type=Application
Name=YAML Excel Converter
Comment=Convert between YAML and Excel formats with GPG support
Exec=$HOME/Applications/YAMLExcelConverter-x86_64.AppImage
Icon=yamlexcelconverter
Categories=Utility;Office;
Terminal=false
EOF
```

## Build Files

### scripts/build_appimage.sh
Automated bash script that:
1. Verifies prerequisites
2. Creates/activates virtual environment
3. Installs dependencies
4. Cleans previous builds
5. Executes PyInstaller with Linux configuration
6. Creates AppDir structure
7. Generates .desktop file
8. Creates icon (if ImageMagick available)
9. Compiles final AppImage
10. Displays output information

### scripts/build_linux.spec
PyInstaller configuration for Linux with:
- **Optimizations**: Excluded pandas/numpy (25+ MB saved)
- **Hidden imports**: Only necessary modules
- **Data files**: Native tkinterdnd2 files for Linux drag & drop
- **Runtime hooks**: Fix for tkdnd in packaged environment
- **Excludes**: Heavy unused libraries
- **COLLECT**: Bundle for AppImage (not single-file)

### pyi_rth_tkinterdnd2.py
Runtime hook to configure tkdnd when the app is packaged.
Resolves the native library loading issue (same file as Windows).

## Manual Build

If you prefer to run manually:

```bash
# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# 3. Build with PyInstaller
pyinstaller build_linux.spec --clean

# 4. Create AppDir structure
mkdir -p AppDir/usr/bin
cp -r dist/YAMLExcelConverter/* AppDir/usr/bin/

# 5. Create .desktop file
# (see build_appimage.sh for content)

# 6. Download appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# 7. Generate AppImage
ARCH=x86_64 ./appimagetool-x86_64.AppImage AppDir YAMLExcelConverter-x86_64.AppImage
```

## Optimizations Applied

### Exclusions (-69% size)
- ❌ pandas (15+ MB)
- ❌ numpy (10+ MB)
- ❌ matplotlib, scipy, PIL
- ❌ pytest, IPython, jupyter

### Core Dependencies Only
- ✅ openpyxl (lightweight, replaces pandas for Excel)
- ✅ pyyaml (YAML parsing)
- ✅ tkinterdnd2 (drag & drop GUI)
- ✅ python-gnupg (GPG encryption)

### Linux Result
- **Size**: ~12 MB AppImage
- **Startup**: Fast (no pandas/numpy loading)
- **Functionality**: Complete (custom format + GPG)
- **Portability**: Runs on any modern Linux distro

## Troubleshooting

### tkinterdnd2 not working
```bash
# Install additional tk dependencies
sudo apt-get install tk-dev tcl-dev
```

### GPG not found
```bash
sudo apt-get install gnupg
```

### Error "ImportError: libpython3.x.so"
The AppImage should include everything, but if necessary:
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev

# Rebuild after installation
./scripts/build_appimage.sh
```

### Icon not displayed
If ImageMagick is not installed, the icon won't be created automatically.
You can manually create a 256x256 PNG icon and copy it to:
```
AppDir/usr/share/icons/hicolor/256x256/apps/yamlexcelconverter.png
```

## Compatibility

The AppImage is tested and working on:
- Ubuntu 20.04, 22.04, 24.04
- Debian 11, 12
- Fedora 37+
- Arch Linux (current)
- Linux Mint 20+
- Pop!_OS 22.04+

Should work on any modern Linux distribution with:
- Kernel 3.10+
- GLIBC 2.23+
- X11 or Wayland

## Windows vs Linux Build Comparison

| Feature | Windows | Linux |
|---------|---------|-------|
| Format | .exe | .AppImage |
| Size | ~11.5 MB | ~12 MB |
| Installer | No (portable) | No (portable) |
| System Dependencies | None | None |
| Drag & Drop | tkdnd/win64 | tkdnd/linux64 |
| GPG | Requires Gpg4win | gnupg (usually preinstalled) |

## Multi-Platform Build

To create both versions:

**On Windows:**
```batch
scripts\build.bat
```

**On Linux:**
```bash
./scripts/build_appimage.sh
```

Cross-compilation is not possible, so you need a Windows machine for the Windows build and a Linux machine for the Linux build.
