# Build Instructions - YAML Excel Converter

## Quick Build

Per creare l'eseguibile Windows, esegui semplicemente:

```batch
scripts\build.bat
```

L'eseguibile sarà disponibile in `dist/YAMLExcelConverter.exe` (~11.5 MB)

## Requisiti Build

- Python 3.8+
- Ambiente Python con dipendenze del progetto (`.venv/` consigliato, non obbligatorio)
- PyInstaller installato: `pip install pyinstaller`
- Tutte le dipendenze da `requirements.txt`

## Setup Iniziale

Se è la prima volta:

```batch
# 1. Crea virtual environment
python -m venv .venv

# 2. Attiva environment
.venv\Scripts\activate

# 3. Installa dipendenze
pip install -r requirements.txt

# 4. Installa PyInstaller
pip install pyinstaller

# 5. Build
scripts\build.bat
```

## File di Build

### scripts/build.bat
Script batch automatico che:
1. Usa `.venv` se disponibile, altrimenti usa l'ambiente Python corrente
2. Pulisce build precedenti
3. Esegue PyInstaller con configurazione ottimizzata
4. Verifica successo e mostra info eseguibile

Lo script risolve i path dalla root del progetto, quindi funziona sia in locale che in CI.

### scripts/build_exe.spec
Configurazione PyInstaller con:
- **Ottimizzazioni**: Esclusi pandas/numpy (25+ MB risparmiati)
- **Hidden imports**: Solo moduli necessari
- **Data files**: File nativi tkinterdnd2 per drag & drop
- **Runtime hooks**: Fix per tkdnd in ambiente pacchettizzato
- **Excludes**: Librerie pesanti non utilizzate

### scripts/pyi_rth_tkinterdnd2.py
Runtime hook per configurare tkdnd quando l'app è pacchettizzata.
Risolve il problema del caricamento della libreria nativa.

### scripts/version_info.txt (opzionale)
File version info per Windows.
Per usarlo, decommenta `version_file=version_info.txt` in scripts/build_exe.spec

## Build Manuale

Se preferisci eseguire manualmente:

```batch
# Opzionale: attiva environment
.venv\Scripts\activate

# Pulisci
rmdir /s /q build dist

# Build
pyinstaller scripts/build_exe.spec --clean
```

## Ottimizzazioni Applicate

### Esclusioni (-69% dimensione)
- ❌ pandas (15+ MB)
- ❌ numpy (10+ MB)
- ❌ matplotlib, scipy, PIL
- ❌ pytest, IPython, jupyter
- ❌ Moduli standard (yaml_to_excel, excel_to_yaml)

### Solo Dipendenze Core
- ✅ openpyxl (leggero, sostituisce pandas per Excel)
- ✅ pyyaml (parsing YAML)
- ✅ tkinterdnd2 (drag & drop GUI)
- ✅ python-gnupg (GPG encryption)

### Risultato
- **Dimensione**: 11.5 MB (vs 37.4 MB originale)
- **Avvio**: Più veloce (nessun caricamento pandas/numpy)
- **Funzionalità**: Complete (formato custom + GPG)

## Troubleshooting

### Avviso: "Virtual environment non trovato"
`scripts\build.bat` può continuare usando l'ambiente Python corrente.
Se preferisci un ambiente isolato:

```batch
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller
```

### Errore: "PyInstaller non trovato"
```batch
.venv\Scripts\activate
pip install pyinstaller
```

### Errore: "Unable to load tkdnd library"
Verifica che `pyi_rth_tkinterdnd2.py` sia presente e referenziato in build_exe.spec

### Build lento
Prima build può richiedere 2-5 minuti. Build successive sono più veloci grazie alla cache.

## Note CI (GitHub Actions)

- I job Windows e Linux usano `actions/setup-python` con cache pip.
- I job di build verificano gli artifact prima dell'upload.
- Il job release verifica gli asset scaricati prima della pubblicazione.

## Customizzazioni

### Aggiungere Icona
1. Crea file `icon.ico` (256x256 o 128x128)
2. In `build_exe.spec`, cambia: `icon=None` → `icon='icon.ico'`

### Aggiungere Version Info
1. In `build_exe.spec`, cambia: `version_file=None` → `version_file='version_info.txt'`
2. Modifica `version_info.txt` con le tue info

### Modificare Nome Eseguibile
In `build_exe.spec`, cambia: `name='YAMLExcelConverter'` → `name='TuoNome'`

## Testing Post-Build

Dopo il build, testa:
1. ✅ Avvio applicazione
2. ✅ Drag & drop file
3. ✅ Conversione YAML → Excel
4. ✅ Conversione Excel → YAML
5. ✅ GPG decrypt (se hai file .gpg)
6. ✅ GPG encrypt
7. ✅ Rilevamento chiavi duplicate

## Distribuzione

L'eseguibile in `dist/YAMLExcelConverter.exe` è:
- **Standalone**: Nessuna installazione Python richiesta
- **Portable**: Può essere copiato su qualsiasi PC Windows
- **Requirements**: Solo Windows 10+ e GPG (per encryption)

Distribuisci insieme a:
- `dist/README.txt` - Guida utente
- Template (opzionale): `secrets.rlist.yml`, `secrets.rlist.xlsx`
