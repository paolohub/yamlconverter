# Contributing to YAML ↔ Excel Converter

Grazie per il tuo interesse nel contribuire a questo progetto! 🎉

## Come Iniziare

### 1. Setup dell'Ambiente di Sviluppo

```bash
# Clona il repository
git clone https://github.com/YOUR_USERNAME/yamlconverter.git
cd yamlconverter

# Crea un virtual environment
python -m venv .venv

# Attiva il virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Installa le dipendenze
pip install -r requirements.txt
```

### 2. File di Test

Il repository include file di esempio per testare le funzionalità:

- `secrets.rlist.example.yml` - Template YAML di esempio
- `secrets.rlist.example.xlsx` - Template Excel di esempio

**NOTA:** Non committare mai file `secrets.rlist.yml` o `secrets.rlist.xlsx` reali contenenti dati sensibili! Usa sempre i file `.example.yml` / `.example.xlsx` per i test.

### 3. Eseguire l'Applicazione

```bash
python main.py
```

### 4. Testing

Prima di sottomettere modifiche, testa entrambe le direzioni di conversione:

```bash
# Test YAML → Excel
python custom_yaml_to_excel.py secrets.rlist.example.yml test_output.xlsx

# Test Excel → YAML
python custom_excel_to_yaml.py secrets.rlist.example.xlsx test_output.yml
```

### 5. Build dell'Eseguibile (Opzionale)

Per testare il build dell'eseguibile Windows:

```bash
scripts\build.bat
```

Vedi [docs/BUILD_INSTRUCTIONS.md](docs/BUILD_INSTRUCTIONS.md) per dettagli completi.

## Linee Guida per i Contributi

### Code Style

- Segui le convenzioni PEP 8 per Python
- Usa nomi di variabili descrittivi
- Commenta il codice quando necessario
- Mantieni le funzioni concise e focalizzate

### Commit Messages

Usa messaggi di commit chiari e descrittivi:

```
feat: aggiungi supporto per nuovo formato
fix: correggi parsing di caratteri speciali
docs: aggiorna README con esempi
refactor: riorganizza modulo di conversione
```

### Pull Requests

1. Fai un fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/amazing-feature`)
3. Committa le tue modifiche (`git commit -m 'feat: add amazing feature'`)
4. Pusha sul branch (`git push origin feature/amazing-feature`)
5. Apri una Pull Request

### Cosa Includere nella PR

- Descrizione chiara delle modifiche
- Test effettuati
- Screenshot (se applicabile)
- Riferimenti a issue correlate

## Aree di Contributo

### Idee per Nuove Feature

- Supporto per altri formati Excel
- Validazione più robusta dei dati
- Interfaccia CLI aggiuntiva
- Supporto per batch conversion
- Export/Import di configurazioni
- Temi personalizzabili per l'interfaccia

### Bug Reports

Quando segnali un bug, includi:

- Versione Python utilizzata
- Sistema operativo
- Passi per riprodurre il problema
- Output di errore completo
- File di esempio (se possibile, usa dati fittizi)

## Traduzioni

Per aggiungere supporto per una nuova lingua:

1. Crea un nuovo file in `translations/` (es. `fr.json` per francese)
2. Copia la struttura da `it.json` o `en.json`
3. Traduci tutti i valori
4. Aggiungi la lingua nel ComboBox in `main.py`
5. Testa l'interfaccia con la nuova lingua

## Domande?

Apri una issue con l'etichetta `question` se hai domande sul progetto o sui contributi.

## Licenza

Contribuendo a questo progetto, accetti che i tuoi contributi saranno rilasciati sotto la licenza GPL-3.0.
