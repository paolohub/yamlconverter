# YAML ↔ Excel Converter

Python application with graphical interface to convert YAML configuration files to Excel and vice versa, optimized for **secrets.rlist** format.

> 🤖 **Developed with GitHub Copilot** (Claude Sonnet 4.5) - This project was created with AI assistance to ensure quality code and best practices.

## Features

- 🔄 Bidirectional conversion: YAML → Excel and Excel → YAML
- ⚙️ **Custom secrets.rlist format** with Name/Secret/Value structure (3 columns)
- 🔐 **GPG support** for encryption/decryption of sensitive files
- 🌐 **Multilingual interface** (Italian / English)
- 🎨 Graphical interface with drag & drop
- 📝 Real-time operation logs
- 🚨 Automatic detection of duplicate YAML keys
- 📦 **Standalone executable** for Windows (11.5 MB)

## Requirements

### For Windows executable
- Windows 10 or higher
- **GPG** (optional - only for encryption/decryption features): [gpg4win.org](https://gpg4win.org/)
  - The application works without GPG for normal YAML ↔ Excel conversions
  - GPG is only required for .gpg (encrypted) files

### For source code execution
- Python 3.8 or higher
- pip (Python package manager)

## Installation

### Option 1: Windows Executable (Recommended)

1. Download `YAMLExcelConverter.exe` from the `dist/` folder
2. Run directly - no installation required
3. (Optional) Install GPG only if you need to use encrypted .gpg files: [gpg4win.org](https://gpg4win.org/)

### Option 2: Installation as Python package

1. **Clone or download the project**

2. **Install the package in development mode:**
   ```bash
   pip install -e .
   ```

3. **Launch the application:**
   ```bash
   yamlconverter
   ```

### Option 3: Running from source code

1. **Clone or download the project**

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the application

**From executable:**
```bash
YAMLExcelConverter.exe
```

**From installed package:**
```bash
yamlconverter
```

**From source code:**
```bash
python run.py
```

### Main Features

#### 0. Language Selection

The application supports **Italian** and **English**:
- Use the dropdown menu in the top right to change language
- The interface updates immediately
- Translations cover the entire interface and error messages

#### 1. YAML → Excel

- Select the "YAML → Excel" mode
- Drag the YAML file into the input area (or use "Browse")
- Specify the output Excel file
- **Format**: Automatically uses secrets.rlist format (Name/Secret/Value)
- **Decrypt GPG**: If the input file is .gpg, enter the password

#### 2. Excel → YAML

- Select the "Excel → YAML" mode
- Drag the Excel file into the input area (or use "Browse")
- Specify the output YAML file (.yml)
- **Format**: Automatically uses secrets.rlist format (Name/Secret/Value)
- **Encrypt GPG** (optional): Check the checkbox to create a .gpg output file

#### 3. secrets.rlist Format

The program uses **exclusively** the custom format for `secrets.rlist` files:

**YAML format (hierarchical structure):**
```yaml
Connections:
  EXAMPLE_CONNECTION_1:
    - secret: "$$ENDPOINT$$"
      value: "https://..."
    - secret: "$$USERNAME$$"
      value: "Test"
    - secret: "$$PASSWORD$$"
      value: "pass"
  EXAMPLE_CONNECTION_2:
    - secret: "$$ENDPOINT$$"
      value: "http://..."
```

**Excel format (3 columns: Name/Secret/Value):**
| Name | Secret | Value |
|------|--------|-------|
| EXAMPLE_CONNECTION_1[0] | $$ENDPOINT$$ | https://... |
| EXAMPLE_CONNECTION_1[1] | $$USERNAME$$ | Test |
| EXAMPLE_CONNECTION_1[2] | $$PASSWORD$$ | pass |
| EXAMPLE_CONNECTION_2[0] | $$ENDPOINT$$ | http://... |
| ... | ... | ... |

**YAML indentation rules:**
- `Connections:` - 0 spaces
- `CONNECTION_NAME:` - 2 spaces
- `- secret:` - 4 spaces
- `value:` - 6 spaces

**Features:**
- Automatic detection of duplicate YAML keys
- Unix line endings (LF)
- Quoted values for safety
- .yml extension for output

#### 4. GPG Support

**Decrypt (YAML → Excel):**
- Input .gpg files are automatically recognized
- Enter password when prompted
- The file is temporarily decrypted for conversion

**Encrypt (Excel → YAML):**
- Check the "Encrypt (GPG)" checkbox under the output section
- Enter password when the field appears
- Output saved with .gpg extension
- Symmetric encryption (armor=False for smaller binary files)

### Conversion Examples

#### Example: secrets.rlist with GPG

#### Example: secrets.rlist with GPG

**Input:** `secrets.rlist.yml.gpg` (encrypted file)
1. Drag file to input
2. Enter GPG password
3. Output: `secrets.rlist.xlsx` (unencrypted Excel file)

**Output with encryption:**
1. Excel → YAML: `secrets.rlist.xlsx` → `secrets.rlist.yml`
2. Check "Encrypt (GPG)"
3. Enter password
4. Output: `secrets.rlist.yml.gpg`

## Project Structure

```
yamlconverter/
│
├── src/                       # Main source code
│   └── yamlconverter/         # Python package
│       ├── __init__.py        # Package metadata (v1.0.0)
│       ├── __main__.py        # CLI entry point
│       ├── gui/               # Graphical interface
│       │   ├── __init__.py
│       │   └── main.py        # Main GUI application
│       ├── converters/        # Conversion modules
│       │   ├── __init__.py
│       │   ├── custom_yaml_to_excel.py  # YAML → Excel
│       │   └── custom_excel_to_yaml.py  # Excel → YAML
│       └── utils/             # Utilities
│           ├── __init__.py
│           ├── gpg_utils.py   # GPG encryption/decryption
│           └── i18n.py        # Translation management
│
├── run.py                     # Entry point for direct execution
├── setup.py                   # Setuptools configuration
├── pyproject.toml             # Python build configuration (PEP 517/518)
├── requirements.txt           # Python dependencies
├── CHANGELOG.md               # Version history and changes
├── CONTRIBUTING.md            # Contributing guide
├── LICENSE                    # GPL-3.0 License
│
├── .github/                   # GitHub community files
│   ├── workflows/
│   │   └── build.yml          # Automated CI/CD
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md      # Bug report template
│   │   └── feature_request.md # Feature request template
│   └── PULL_REQUEST_TEMPLATE.md
│
├── scripts/                   # Build scripts
│   ├── build.bat              # Windows build (exe)
│   ├── build_appimage.sh      # Linux build (AppImage)
│   ├── build_exe.spec         # PyInstaller configuration for Windows
│   ├── build_linux.spec       # PyInstaller configuration for Linux
│   ├── pyi_rth_tkinterdnd2.py # tkdnd runtime hook
│   ├── version_info.txt       # Windows version info
│   └── hooks/                 # Custom PyInstaller hooks
│
├── docs/                      # Documentation
│   ├── BUILD_INSTRUCTIONS.md         # Windows build instructions
│   └── BUILD_INSTRUCTIONS_LINUX.md   # Linux build instructions
│
├── examples/                  # Example files
│   ├── secrets.rlist.example.yml     # YAML template
│   └── secrets.rlist.example.xlsx    # Excel template
│
├── translations/              # Interface translation files
│   ├── en.json                # English
│   └── it.json                # Italian
│
└── dist/                      # Build output (generated)
    ├── YAMLExcelConverter.exe # Windows executable (11.5 MB)
    └── YAMLExcelConverter-x86_64.AppImage # Linux AppImage
```

## Optimizations

### Executable version
- **Size**: 11.5 MB (69% reduction compared to pandas version)
- **Removed dependencies**: pandas, numpy (25+ MB)
- **Excel library**: Only openpyxl (lightweight and fast)
- **Single format**: Only custom secrets.rlist (simplified interface)
- **Fast startup**: No pandas/numpy loading at startup

## Advanced Features

### Duplicate Key Detection

The program analyzes the YAML before parsing and detects duplicate keys at the same level:
```yaml
Connections:
  SAP_SOAP:  # First definition
    - secret: "user"
  SAP_SOAP:  # Duplicate! - Warning
    - secret: "pass"
```

### Drag & Drop

- Drag files directly to input/output areas
- Automatic extension detection and validation
- Automatic mode switching based on extensions

### Password Management

- Shared password field between decrypt and encrypt for convenience
- Toggle button to show/hide password (👁/🔒)
- Password validation before conversion

## Building Executable

To create the optimized Windows executable (11.5 MB):

```bash
# Automatic build (recommended) - run from scripts/ directory
cd scripts
build.bat
```

The build script:
- Activates virtual environment
- Cleans previous builds
- Creates executable with PyInstaller
- Verifies success with size info

For complete instructions and troubleshooting, see [docs/BUILD_INSTRUCTIONS.md](docs/BUILD_INSTRUCTIONS.md)

### Manual Build

```bash
# Install PyInstaller (if needed)
pip install pyinstaller

# Build with optimized spec file (from scripts/ directory)
cd scripts
pyinstaller build_exe.spec --clean --distpath=..\dist --workpath=..\build\build_exe
```

The executable will be in `dist/YAMLExcelConverter.exe`

## Development

### Development Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd yamlconverter

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install in development mode
pip install -e .
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=yamlconverter

# Run specific tests
pytest tests/test_converters/
```

## Limitations

- **Format**: Only secrets.rlist format (Name/Secret/Value structure with 3 columns)
- YAML structures not conforming to secrets.rlist format may not be supported
- Excel file must have "Name", "Secret" and "Value" columns
- **GPG**: Only required for encryption/decryption features (.gpg files)

## Troubleshooting

### Error: "ModuleNotFoundError"
Make sure you have installed all dependencies:
```bash
pip install -r requirements.txt
```

### Error: "Unable to load tkdnd library"
If you use the executable on very old systems, Visual C++ Runtime might be missing:
- Download and install [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### GPG Error
- **Note**: GPG is **only** required for .gpg files (encryption/decryption)
- Normal YAML ↔ Excel conversions work without GPG installed
- Verify that GPG is installed: `gpg --version`
- Make sure gpg.exe is in the system PATH
- On Windows, install GPG4Win: [gpg4win.org](https://gpg4win.org/)

### Error during conversion
- Verify that the Excel file has "Name" and "Value" columns
- Check that the YAML follows the secrets.rlist format
- Check the log in the application for error details
- Make sure you have write permissions for the output file

### Application won't start
- Verify you have Python 3.8 or higher: `python --version`
- On some systems you may need to use `python3` instead of `python`

### Antivirus blocks the executable
- Add an exception for YAMLExcelConverter.exe
- The executable is safe but some antivirus software may flag it as a false positive

### Adding new translations
To add support for a new language:
1. Create a new JSON file in `translations/` (e.g., `fr.json` for French)
2. Copy the structure from `it.json` or `en.json`
3. Translate all values
4. Update the `get_available_languages()` method in `i18n.py`
5. Add the new language to the ComboBox in `main.py`

## Dependencies

- **pyyaml** (6.0.1) - YAML parsing and generation
- **openpyxl** (3.1.2) - Excel file manipulation
- **tkinterdnd2** (0.3.0) - Drag & drop in interface
- **python-gnupg** (0.5.2) - GPG wrapper for encryption

## Contributing

Feel free to open issues or pull requests for improvements or bug fixes.

## License

This project is distributed under the **GNU General Public License v3.0** (GPL-3.0).

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

A copy of the license is available in the [LICENSE](LICENSE) file. For more information, visit <https://www.gnu.org/licenses/>.

## Author

**Paolo Cardamone** © 2026

Developed as a utility tool for managing configuration files.

---

**Note**: This application is designed for small/medium-sized configuration files. For very large files, additional optimizations may be required.
