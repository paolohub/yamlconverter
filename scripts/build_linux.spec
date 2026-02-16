# -*- mode: python ; coding: utf-8 -*-
"""
Configurazione PyInstaller per YAML Excel Converter - Linux AppImage
Versione ottimizzata: ~12 MB

Ottimizzazioni applicate:
- Esclusi pandas e numpy (25+ MB risparmiati)
- Solo formato custom secrets.rlist
- Librerie minimali: openpyxl, pyyaml, tkinterdnd2, python-gnupg
"""
import os
from pathlib import Path

block_cipher = None

# Percorso root del progetto (build script fa cd alla root prima di eseguire)
root_dir = Path(os.getcwd()).absolute()
src_dir = root_dir / 'src'

# Trova il percorso di tkinterdnd2 per includere file nativi Linux
import tkinterdnd2
tkdnd_path = Path(tkinterdnd2.__file__).parent / 'tkdnd'

a = Analysis(
    [str(root_dir / 'run.py')],
    pathex=[str(src_dir)],
    binaries=[],
    datas=[
        # File nativi tkinterdnd2 per drag & drop su Linux
        (str(tkdnd_path / 'linux64'), 'tkdnd/linux64'),
        # File di traduzione
        (str(root_dir / 'translations'), 'translations'),
    ],
    hiddenimports=[
        # Dipendenze core
        'tkinterdnd2',      # Drag & drop interface
        'gnupg',            # GPG encryption/decryption
        'yaml',             # YAML parsing
        'openpyxl',         # Excel manipulation (sostituisce pandas)
        # Package yamlconverter
        'yamlconverter',
        'yamlconverter.gui',
        'yamlconverter.gui.main',
        'yamlconverter.converters',
        'yamlconverter.converters.custom_yaml_to_excel',
        'yamlconverter.converters.custom_excel_to_yaml',
        'yamlconverter.utils',
        'yamlconverter.utils.gpg_utils',
        'yamlconverter.utils.i18n',
    ],
    hookspath=[str(root_dir / 'scripts' / 'hooks')],
    hooksconfig={},
    runtime_hooks=[str(root_dir / 'scripts' / 'pyi_rth_tkinterdnd2.py')],
    excludes=[
        # Escludi librerie pesanti non necessarie
        'pandas',           # 15+ MB (sostituito con openpyxl)
        'numpy',            # 10+ MB (non necessario)
        'matplotlib',       # Non usato
        'scipy',            # Non usato
        'PIL',              # Non usato
        'Pillow',           # Non usato
        'pytest',           # Testing - non necessario in produzione
        'IPython',          # Non usato
        'notebook',         # Non usato
        'jupyter',          # Non usato
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='YAMLExcelConverter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                    # Compressione UPX attiva
    console=False,               # GUI mode - nessuna console
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='YAMLExcelConverter',
)
