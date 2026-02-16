# Build Instructions - YAML Excel Converter (Linux AppImage)

## Quick Build

Per creare l'AppImage Linux, esegui:

```bash
chmod +x scripts/build_appimage.sh
./scripts/build_appimage.sh
```

L'AppImage sarà disponibile in `YAMLExcelConverter-x86_64.AppImage` (~12 MB)

## Requisiti Build

### Pacchetti Sistema
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-venv python3-tk gnupg wget

# Opzionale per creare icona
sudo apt-get install imagemagick

# Fedora/RHEL
sudo dnf install python3 python3-tkinter gnupg wget

# Arch Linux
sudo pacman -S python python-pip tk gnupg wget
```

### Python
- Python 3.8+
- Virtual environment (creato automaticamente dallo script)
- Tutte le dipendenze da `requirements.txt`

## Setup Iniziale

Se è la prima volta:

```bash
# 1. Clona o copia il repository
cd yamlconverter

# 2. Rendi lo script eseguibile
chmod +x scripts/build_appimage.sh

# 3. Esegui il build
./scripts/build_appimage.sh
```

Lo script automaticamente:
1. Crea virtual environment (se non esiste)
2. Installa dipendenze Python
3. Installa PyInstaller
4. Compila l'applicazione
5. Crea la struttura AppDir
6. Scarica appimagetool (se necessario)
7. Genera l'AppImage

## Esecuzione AppImage

```bash
# Rendi eseguibile (solo la prima volta)
chmod +x YAMLExcelConverter-x86_64.AppImage

# Esegui
./YAMLExcelConverter-x86_64.AppImage
```

## Installazione Sistema

L'AppImage non richiede installazione, ma se vuoi integrarlo meglio:

### Metodo 1: Copia in /opt (Consigliato)
```bash
sudo cp YAMLExcelConverter-x86_64.AppImage /opt/
sudo chmod +x /opt/YAMLExcelConverter-x86_64.AppImage
```

### Metodo 2: Copia in ~/Applications
```bash
mkdir -p ~/Applications
cp YAMLExcelConverter-x86_64.AppImage ~/Applications/
chmod +x ~/Applications/YAMLExcelConverter-x86_64.AppImage
```

### Integrazione Desktop
Crea un launcher desktop:

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

## File di Build

### scripts/build_appimage.sh
Script bash automatico che:
1. Verifica prerequisiti
2. Crea/attiva virtual environment
3. Installa dipendenze
4. Pulisce build precedenti
5. Esegue PyInstaller con configurazione Linux
6. Crea struttura AppDir
7. Genera file .desktop
8. Crea icona (se ImageMagick disponibile)
9. Compila AppImage finale
10. Mostra informazioni output

### scripts/build_linux.spec
Configurazione PyInstaller per Linux con:
- **Ottimizzazioni**: Esclusi pandas/numpy (25+ MB risparmiati)
- **Hidden imports**: Solo moduli necessari
- **Data files**: File nativi tkinterdnd2 per drag & drop Linux
- **Runtime hooks**: Fix per tkdnd in ambiente pacchettizzato
- **Excludes**: Librerie pesanti non utilizzate
- **COLLECT**: Bundle per AppImage (non single-file)

### pyi_rth_tkinterdnd2.py
Runtime hook per configurare tkdnd quando l'app è pacchettizzata.
Risolve il problema del caricamento della libreria nativa (stesso file di Windows).

## Build Manuale

Se preferisci eseguire manualmente:

```bash
# 1. Crea virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Installa dipendenze
pip install -r requirements.txt
pip install pyinstaller

# 3. Build con PyInstaller
pyinstaller build_linux.spec --clean

# 4. Crea AppDir structure
mkdir -p AppDir/usr/bin
cp -r dist/YAMLExcelConverter/* AppDir/usr/bin/

# 5. Crea .desktop file
# (vedi build_appimage.sh per il contenuto)

# 6. Download appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# 7. Genera AppImage
ARCH=x86_64 ./appimagetool-x86_64.AppImage AppDir YAMLExcelConverter-x86_64.AppImage
```

## Ottimizzazioni Applicate

### Esclusioni (-69% dimensione)
- ❌ pandas (15+ MB)
- ❌ numpy (10+ MB)
- ❌ matplotlib, scipy, PIL
- ❌ pytest, IPython, jupyter

### Solo Dipendenze Core
- ✅ openpyxl (leggero, sostituisce pandas per Excel)
- ✅ pyyaml (parsing YAML)
- ✅ tkinterdnd2 (drag & drop GUI)
- ✅ python-gnupg (GPG encryption)

### Risultato Linux
- **Dimensione**: ~12 MB AppImage
- **Avvio**: Veloce (nessun caricamento pandas/numpy)
- **Funzionalità**: Complete (formato custom + GPG)
- **Portabilità**: Esegue su qualsiasi distro Linux moderna

## Troubleshooting

### tkinterdnd2 non funziona
```bash
# Installa dipendenze tk aggiuntive
sudo apt-get install tk-dev tcl-dev
```

### GPG non trovato
```bash
sudo apt-get install gnupg
```

### Errore "ImportError: libpython3.x.so"
L'AppImage dovrebbe includere tutto, ma se necessario:
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev

# Rebuild dopo l'installazione
./scripts/build_appimage.sh
```

### Icona non visualizzata
Se ImageMagick non è installato, l'icona non viene creata automaticamente.
Puoi creare manualmente un'icona PNG 256x256 e copiarla in:
```
AppDir/usr/share/icons/hicolor/256x256/apps/yamlexcelconverter.png
```

## Compatibilità

L'AppImage è testato e funzionante su:
- Ubuntu 20.04, 22.04, 24.04
- Debian 11, 12
- Fedora 37+
- Arch Linux (current)
- Linux Mint 20+
- Pop!_OS 22.04+

Dovrebbe funzionare su qualsiasi distribuzione Linux moderna con:
- Kernel 3.10+
- GLIBC 2.23+
- X11 o Wayland

## Confronto Build Windows vs Linux

| Caratteristica | Windows | Linux |
|---------------|---------|-------|
| Formato | .exe | .AppImage |
| Dimensione | ~11.5 MB | ~12 MB |
| Installer | No (portable) | No (portable) |
| Dipendenze Sistema | Nessuna | Nessuna |
| Drag & Drop | tkdnd/win64 | tkdnd/linux64 |
| GPG | Richiede Gpg4win | gnupg (di solito preinstallato) |

## Build Multi-Piattaforma

Per creare entrambe le versioni:

**Su Windows:**
```batch
scripts\build.bat
```

**Su Linux:**
```bash
./scripts/build_appimage.sh
```

Non è possibile fare cross-compilation, quindi serve una macchina Windows per la build Windows e una macchina Linux per la build Linux.
