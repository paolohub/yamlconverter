#!/bin/bash
# ========================================
#  YAML Excel Converter - Build Script Linux AppImage
#  Versione Ottimizzata: ~12 MB
# ========================================

set -e  # Exit on error

# Cambia directory alla root del progetto (parent di scripts/)
cd "$(dirname "$0")/.."

echo "========================================"
echo " YAML Excel Converter - Build AppImage"
echo " Versione Ottimizzata"
echo "========================================"
echo ""

# Colori per output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Funzione per stampare messaggi colorati
print_step() {
    echo -e "${GREEN}[$1]${NC} $2"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Verifica prerequisiti
print_step "0/7" "Verifica prerequisiti..."

if ! command -v python3 &> /dev/null; then
    print_error "Python3 non trovato! Installare con: sudo apt-get install python3"
    exit 1
fi

if ! command -v gpg &> /dev/null; then
    print_warning "GPG non trovato. Installare con: sudo apt-get install gnupg"
fi

# Crea virtual environment se non esiste
if [ ! -d ".venv" ]; then
    print_step "1/7" "Creazione virtual environment..."
    python3 -m venv .venv
else
    print_step "1/7" "Virtual environment già esistente"
fi

# Attiva virtual environment
print_step "2/7" "Attivazione virtual environment..."
source .venv/bin/activate

# Installa/aggiorna dipendenze
print_step "3/7" "Installazione dipendenze..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

# Pulizia build precedenti
print_step "4/7" "Pulizia build precedenti..."
rm -rf build dist AppDir *.AppImage
echo "  - Rimossa cartella build, dist, AppDir"

# Creazione eseguibile con PyInstaller
print_step "5/7" "Creazione eseguibile ottimizzato con PyInstaller..."
echo "  - Escluse dipendenze: pandas, numpy (25+ MB risparmiati)"
echo "  - Solo formato custom secrets.rlist"
pyinstaller scripts/build_linux.spec --clean --distpath=dist --workpath=build/build_linux

if [ ! -f "dist/YAMLExcelConverter/YAMLExcelConverter" ]; then
    print_error "Build PyInstaller fallita!"
    exit 1
fi

# Preparazione struttura AppDir
print_step "6/7" "Creazione struttura AppImage..."

# Crea struttura AppDir
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps

# Copia l'applicazione
cp -r dist/YAMLExcelConverter/* AppDir/usr/bin/

# Crea file .desktop
cat > AppDir/usr/share/applications/yamlexcelconverter.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=YAML Excel Converter
Comment=Convert between YAML and Excel formats with GPG support
Exec=YAMLExcelConverter
Icon=yamlexcelconverter
Categories=Utility;Office;
Terminal=false
EOF

# Crea un'icona semplice (PNG 256x256) - puoi sostituirla con una tua
# Per ora creiamo un'icona placeholder usando ImageMagick se disponibile
if command -v convert &> /dev/null; then
    convert -size 256x256 xc:lightblue \
            -gravity center -pointsize 48 -fill darkblue \
            -annotate +0+0 'YAML\n↕\nExcel' \
            AppDir/usr/share/icons/hicolor/256x256/apps/yamlexcelconverter.png
else
    print_warning "ImageMagick non trovato. Icona non creata. Installare con: sudo apt-get install imagemagick"
    # Crea un file placeholder
    touch AppDir/usr/share/icons/hicolor/256x256/apps/yamlexcelconverter.png
fi

# Crea link simbolici nella root di AppDir
ln -sf usr/bin/YAMLExcelConverter AppDir/AppRun
ln -sf usr/share/applications/yamlexcelconverter.desktop AppDir/yamlexcelconverter.desktop
ln -sf usr/share/icons/hicolor/256x256/apps/yamlexcelconverter.png AppDir/yamlexcelconverter.png

# Rendi AppRun eseguibile
chmod +x AppDir/AppRun
chmod +x AppDir/usr/bin/YAMLExcelConverter

# Download appimagetool se non esiste
if [ ! -f "appimagetool-x86_64.AppImage" ]; then
    print_step "6.5/7" "Download appimagetool..."
    wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
    chmod +x appimagetool-x86_64.AppImage
fi

# Crea AppImage
print_step "7/7" "Creazione AppImage finale..."
ARCH=x86_64 ./appimagetool-x86_64.AppImage AppDir YAMLExcelConverter-x86_64.AppImage

if [ -f "YAMLExcelConverter-x86_64.AppImage" ]; then
    echo ""
    echo "========================================"
    echo " BUILD COMPLETATO CON SUCCESSO!"
    echo "========================================"
    echo ""
    SIZE=$(du -h YAMLExcelConverter-x86_64.AppImage | cut -f1)
    echo "File creato: YAMLExcelConverter-x86_64.AppImage"
    echo "Dimensione: $SIZE"
    echo ""
    echo "Per eseguire:"
    echo "  chmod +x YAMLExcelConverter-x86_64.AppImage"
    echo "  ./YAMLExcelConverter-x86_64.AppImage"
    echo ""
    echo "Per installare:"
    echo "  Copia il file .AppImage dove preferisci"
    echo "  Rendilo eseguibile e crea un link sul desktop"
    echo ""
else
    print_error "Creazione AppImage fallita!"
    exit 1
fi

# Pulizia file temporanei (opzionale)
read -p "Vuoi pulire i file temporanei di build? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_step "Cleanup" "Rimozione file temporanei..."
    rm -rf build dist AppDir
    echo "  - File temporanei rimossi"
fi

echo ""
echo "Build completata!"
