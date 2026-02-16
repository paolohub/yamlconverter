# YAML ↔ Excel Converter

Applicazione Python con interfaccia grafica per convertire file di configurazione YAML in Excel e viceversa, ottimizzata per il formato **secrets.rlist**.

> 🤖 **Sviluppato con GitHub Copilot** (Claude Sonnet 4.5) - Questo progetto è stato realizzato con l'assistenza di intelligenza artificiale per garantire codice di qualità e best practices.

## Caratteristiche

- 🔄 Conversione bidirezionale: YAML → Excel e Excel → YAML
- ⚙️ **Formato custom secrets.rlist** con struttura Name/Secret/Value (3 colonne)
- 🔐 **Supporto GPG** per encryption/decryption di file sensibili
- � **Interfaccia multilingua** (Italiano / English)
- �🎨 Interfaccia grafica con drag & drop
- 📝 Log delle operazioni in tempo reale
- 🚨 Rilevamento automatico chiavi YAML duplicate
- 📦 **Eseguibile standalone** per Windows (11.5 MB)

## Requisiti

### Per eseguibile Windows
- Windows 10 o superiore
- **GPG** (opzionale - solo per funzionalità encryption/decryption): [gpg4win.org](https://gpg4win.org/)
  - L'applicazione funziona senza GPG per conversioni normali YAML ↔ Excel
  - GPG è necessario solo per file .gpg (criptati)

### Per esecuzione da codice sorgente
- Python 3.8 o superiore
- pip (gestore pacchetti Python)

## Installazione

### Opzione 1: Eseguibile Windows (Raccomandato)

1. Scarica `YAMLExcelConverter.exe` dalla cartella `dist/`
2. Esegui direttamente - nessuna installazione richiesta
3. (Opzionale) Installa GPG solo se devi usare file .gpg criptati: [gpg4win.org](https://gpg4win.org/)

### Opzione 2: Installazione come pacchetto Python

1. **Clona o scarica il progetto**

2. **Installa il pacchetto in modalità development:**
   ```bash
   pip install -e .
   ```

3. **Avvia l'applicazione:**
   ```bash
   yamlconverter
   ```

### Opzione 3: Esecuzione da codice sorgente

1. **Clona o scarica il progetto**

2. **(Raccomandato) Crea un virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Installa le dipendenze:**
   ```bash
   pip install -r requirements.txt
   ```

`scripts\build.bat` usa `.venv` se disponibile, altrimenti usa l'ambiente Python corrente.

## Utilizzo

### Avvio dell'applicazione

**Da eseguibile:**
```bash
YAMLExcelConverter.exe
```

**Da pacchetto installato:**
```bash
yamlconverter
```

**Da codice sorgente:**
```bash
python run.py
```

### Funzionalità principali

#### 0. Selezione Lingua / Language Selection

L'applicazione supporta **Italiano** e **English**:
- Usa il menu a tendina in alto a destra per cambiare lingua
- L'interfaccia si aggiorna immediatamente
- Le traduzioni coprono tutta l'interfaccia e i messaggi di errore

#### 1. YAML → Excel

- Seleziona la modalità "YAML → Excel"
- Trascina il file YAML nell'area di input (o usa "Sfoglia")
- Specifica il file Excel di output
- **Formato**: Automaticamente usa formato secrets.rlist (Name/Secret/Value)
- **Decrypt GPG**: Se il file input è .gpg, inserisci la password

#### 2. Excel → YAML

- Seleziona la modalità "Excel → YAML"
- Trascina il file Excel nell'area di input (o usa "Sfoglia")
- Specifica il file YAML di output (.yml)
- **Formato**: Automaticamente usa formato secrets.rlist (Name/Secret/Value)
- **Encrypt GPG** (opzionale): Seleziona checkbox per creare file .gpg in output

#### 3. Formato secrets.rlist

Il programma usa **esclusivamente** il formato custom per file `secrets.rlist`:

**Formato YAML (struttura gerarchica):**
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

**Formato Excel (3 colonne: Name/Secret/Value):**
| Name | Secret | Value |
|------|--------|-------|
| EXAMPLE_CONNECTION_1[0] | $$ENDPOINT$$ | https://... |
| EXAMPLE_CONNECTION_1[1] | $$USERNAME$$ | Test |
| EXAMPLE_CONNECTION_1[2] | $$PASSWORD$$ | pass |
| EXAMPLE_CONNECTION_2[0] | $$ENDPOINT$$ | http://... |
| ... | ... | ... |

**Regole di indentazione YAML:**
- `Connections:` - 0 spazi
- `CONNECTION_NAME:` - 2 spazi
- `- secret:` - 4 spazi
- `value:` - 6 spazi

**Caratteristiche:**
- Rilevamento automatico chiavi YAML duplicate
- Line ending Unix (LF)
- Valori quotati per sicurezza
- Estensione .yml per output

#### 4. Supporto GPG

**Decrypt (YAML → Excel):**
- File input .gpg vengono automaticamente riconosciuti
- Inserisci password quando richiesto
- Il file viene decriptato temporaneamente per la conversione

**Encrypt (Excel → YAML):**
- Seleziona checkbox "Encrypt (GPG)" sotto la sezione output
- Inserisci password quando appare il campo
- Output salvato con estensione .gpg
- Encryption simmetrica (armor=False per file binari più piccoli)

### Esempi di conversione

#### Esempio: secrets.rlist con GPG

#### Esempio: secrets.rlist con GPG

**Input:** `secrets.rlist.yml.gpg` (file crittografato)
1. Trascina file nell'input
2. Inserisci password GPG
3. Output: `secrets.rlist.xlsx` (file Excel non crittografato)

**Output con encryption:**
1. Excel → YAML: `secrets.rlist.xlsx` → `secrets.rlist.yml`
2. Seleziona "Encrypt (GPG)"
3. Inserisci password
4. Output: `secrets.rlist.yml.gpg`

## Struttura del progetto

```
yamlconverter/
│
├── src/                       # Codice sorgente principale
│   └── yamlconverter/         # Package Python
│       ├── __init__.py        # Metadata package (v1.0.0)
│       ├── __main__.py        # Entry point CLI
│       ├── gui/               # Interfaccia grafica
│       │   ├── __init__.py
│       │   └── main.py        # Applicazione GUI principale
│       ├── converters/        # Moduli di conversione
│       │   ├── __init__.py
│       │   ├── custom_yaml_to_excel.py  # YAML → Excel
│       │   └── custom_excel_to_yaml.py  # Excel → YAML
│       └── utils/             # Utility
│           ├── __init__.py
│           ├── gpg_utils.py   # GPG encryption/decryption
│           └── i18n.py        # Gestione traduzioni
│
├── run.py                     # Entry point per esecuzione diretta
├── setup.py                   # Configurazione setuptools
├── pyproject.toml             # Configurazione build Python (PEP 517/518)
├── requirements.txt           # Dipendenze Python
├── CHANGELOG.md               # Storia versioni e modifiche
├── CONTRIBUTING.md            # Guida per contribuire al progetto
├── LICENSE                    # Licenza GPL-3.0
│
├── .github/                   # GitHub community files
│   ├── workflows/
│   │   └── build.yml          # CI/CD automatico
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md      # Template bug report
│   │   └── feature_request.md # Template richiesta feature
│   └── PULL_REQUEST_TEMPLATE.md
│
├── scripts/                   # Script di build
│   ├── build.bat              # Build Windows (exe)
│   ├── build_appimage.sh      # Build Linux (AppImage)
│   ├── build_exe.spec         # Configurazione PyInstaller Windows
│   ├── build_linux.spec       # Configurazione PyInstaller Linux
│   ├── pyi_rth_tkinterdnd2.py # Runtime hook tkdnd
│   ├── version_info.txt       # Info versione Windows
│   └── hooks/                 # Hook personalizzati PyInstaller
│
├── docs/                      # Documentazione
│   ├── BUILD_INSTRUCTIONS.md         # Istruzioni build Windows
│   └── BUILD_INSTRUCTIONS_LINUX.md   # Istruzioni build Linux
│
├── examples/                  # File di esempio
│   ├── secrets.rlist.example.yml     # Template YAML
│   └── secrets.rlist.example.xlsx    # Template Excel
│
├── translations/              # File traduzione interfaccia
│   ├── en.json                # Inglese
│   └── it.json                # Italiano
│
└── dist/                      # Output build (generato)
    ├── YAMLExcelConverter.exe # Eseguibile Windows (11.5 MB)
    └── YAMLExcelConverter-x86_64.AppImage # AppImage Linux
```

## Ottimizzazioni

### Versione eseguibile
- **Dimensione**: 11.5 MB (riduzione 69% rispetto a versione con pandas)
- **Dipendenze rimosse**: pandas, numpy (25+ MB)
- **Libreria Excel**: Solo openpyxl (leggera e veloce)
- **Formato unico**: Solo secrets.rlist custom (interfaccia semplificata)
- **Avvio rapido**: Nessun caricamento pandas/numpy all'avvio

## Funzionalità avanzate

### Rilevamento chiavi duplicate

Il programma analizza il YAML prima del parsing e rileva chiavi duplicate allo stesso livello:
```yaml
Connections:
  SAP_SOAP:  # Prima definizione
    - secret: "user"
  SAP_SOAP:  # Duplicato! - Warning
    - secret: "pass"
```

### Drag & Drop

- Trascina file direttamente nelle aree di input/output
- Rilevamento automatico estensione e validazione
- Cambio automatico modalità in base alle estensioni

### Gestione Password

- Campo password condiviso tra decrypt e encrypt per comodità
- Pulsante toggle per mostrare/nascondere password (👁/🔒)
- Validazione password prima della conversione

## Build Eseguibile

Per creare l'eseguibile Windows ottimizzato (11.5 MB):

```bash
# Build automatico (raccomandato) - eseguire dalla root del progetto
scripts\build.bat
```

Il build script:
- Usa `.venv` se disponibile (altrimenti usa l'ambiente Python corrente)
- Pulisce build precedenti
- Crea eseguibile con PyInstaller
- Verifica successo con info dimensione

Per istruzioni complete e troubleshooting, vedi [docs/BUILD_INSTRUCTIONS.md](docs/BUILD_INSTRUCTIONS.md)

### Build Manuale

```bash
# Installa PyInstaller (se necessario)
pip install pyinstaller

# Build con spec file ottimizzato (dalla root del progetto)
pyinstaller scripts/build_exe.spec --clean --distpath=dist --workpath=build/build_exe
```

L'eseguibile sarà in `dist/YAMLExcelConverter.exe`

## Sviluppo

### Setup ambiente di sviluppo

```bash
# Clona il repository
git clone <repository-url>
cd yamlconverter

# Crea e attiva virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Installa in modalità development
pip install -e .
```

### Esecuzione test

```bash
# Esegui tutti i test
pytest

# Esegui test con coverage
pytest --cov=yamlconverter

# Esegui test specifici
pytest tests/test_converters/
```

## Limitazioni

- **Formato**: Solo formato secrets.rlist (Name/Secret/Value structure con 3 colonne)
- Strutture YAML non conformi al formato secrets.rlist potrebbero non essere supportate
- File Excel deve avere colonne "Name", "Secret" e "Value"
- **GPG**: Necessario solo per funzionalità encryption/decryption (file .gpg)

## Risoluzione problemi

### Errore: "ModuleNotFoundError"
Assicurati di aver installato tutte le dipendenze:
```bash
pip install -r requirements.txt
```

### Errore: "Unable to load tkdnd library"
Se usi l'eseguibile su sistemi molto vecchi, potrebbe mancare Visual C++ Runtime:
- Scarica e installa [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### Errore GPG
- **Nota**: GPG è necessario **solo** per file .gpg (encryption/decryption)
- Le conversioni normali YAML ↔ Excel funzionano senza GPG installato
- Verifica che GPG sia installato: `gpg --version`
- Assicurati che gpg.exe sia nel PATH di sistema
- Su Windows, installa GPG4Win: [gpg4win.org](https://gpg4win.org/)

### Errore durante la conversione
- Verifica che il file Excel abbia colonne "Name" e "Value"
- Controlla che il YAML segua il formato secrets.rlist
- Controlla il log nell'applicazione per dettagli sull'errore
- Assicurati di avere i permessi di scrittura per il file di output

### L'applicazione non si avvia
- Verifica di avere Python 3.8 o superiore: `python --version`
- Su alcuni sistemi potrebbe essere necessario usare `python3` invece di `python`

### Antivirus blocca l'eseguibile
- Aggiungi un'eccezione per YAMLExcelConverter.exe
- L'eseguibile è sicuro ma alcuni antivirus potrebbero segnalarlo come falso positivo

### Aggiungere nuove traduzioni
Per aggiungere supporto per una nuova lingua:
1. Crea un nuovo file JSON in `translations/` (es. `fr.json` per francese)
2. Copia la struttura da `it.json` o `en.json`
3. Traduci tutti i valori
4. Aggiorna il metodo `get_available_languages()` in `i18n.py`
5. Aggiungi la nuova lingua al ComboBox in `main.py`

## Dipendenze

- **pyyaml** (6.0.1) - Parsing e generazione YAML
- **openpyxl** (3.1.2) - Manipolazione file Excel
- **tkinterdnd2** (0.3.0) - Drag & drop nell'interfaccia
- **python-gnupg** (0.5.2) - Wrapper GPG per encryption

## Contributi

Sentiti libero di aprire issue o pull request per miglioramenti o correzioni di bug.

## Licenza

Questo progetto è distribuito sotto **GNU General Public License v3.0** (GPL-3.0).

Questo programma è software libero: puoi ridistribuirlo e/o modificarlo secondo i termini della GNU General Public License come pubblicata dalla Free Software Foundation, sia la versione 3 della Licenza, sia (a tua scelta) qualsiasi versione successiva.

Questo programma è distribuito nella speranza che sia utile, ma SENZA ALCUNA GARANZIA; senza nemmeno la garanzia implicita di COMMERCIABILITÀ o IDONEITÀ PER UN PARTICOLARE SCOPO. Vedi la GNU General Public License per maggiori dettagli.

Una copia della licenza è disponibile nel file [LICENSE](LICENSE). Per maggiori informazioni, visita <https://www.gnu.org/licenses/>.

## Autore

**Paolo Cardamone** © 2026

Sviluppato come strumento di utilità per la gestione di file di configurazione.

---

**Nota**: Questa applicazione è pensata per file di configurazione di piccole/medie dimensioni. Per file molto grandi potrebbero essere necessarie ottimizzazioni aggiuntive.
