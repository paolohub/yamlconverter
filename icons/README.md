# Icone dell'Applicazione

Questa cartella contiene le icone per l'applicazione YAML Excel Converter.

## File Disponibili

- **icon.svg** - Icona vettoriale sorgente (scalabile senza perdita di qualità)
- **icon.png** - Icona principale PNG 256x256 (per uso generico)
- **icon.ico** - Icona Windows multi-risoluzione (usata dall'eseguibile .exe)
- **icon_XXxXX.png** - Varianti PNG a diverse risoluzioni (16x16, 32x32, 48x48, 64x64, 128x128, 256x256, 512x512)

## Design dell'Icona

L'icona rappresenta la funzionalità principale dell'applicazione:

- **Documento YAML** (rosso) a sinistra - rappresenta i file di configurazione YAML
- **Foglio Excel** (verde) a destra - rappresenta i fogli di calcolo Excel
- **Frecce bidirezionali** (blu) al centro - indicano la conversione bidirezionale tra i formati

## Rigenerare le Icone

Per rigenerare le icone (ad esempio dopo aver modificato il design):

```bash
# Installa Pillow se non già presente
pip install Pillow

# Esegui lo script di generazione
python scripts/generate_icon.py
```

Lo script genererà automaticamente tutte le varianti PNG e il file ICO per Windows.

## Utilizzo negli Script di Build

Le icone sono automaticamente integrate negli eseguibili:

- **Windows** (`build_exe.spec`): usa `icons/icon.ico`
- **Linux AppImage** (`build_appimage.sh`): usa `icons/icon.png`

## Modificare l'Icona

Se vuoi personalizzare l'icona:

1. Modifica il file `scripts/generate_icon.py` per cambiare colori, forme o layout
2. Oppure modifica direttamente `icon.svg` con un editor vettoriale (Inkscape, Adobe Illustrator, ecc.)
3. Rigenera le icone bitmap con lo script

## Note Tecniche

- **Formato SVG**: Scalabile, perfetto per future modifiche
- **Formato PNG**: Usato su Linux e come base per altre conversioni
- **Formato ICO**: Contiene multiple risoluzioni (16, 32, 48, 64, 128, 256) per Windows
- **Risoluzione principale**: 256x256 px (standard per icone moderne)
- **Colori**:
  - YAML: #cb5e5e (rosso)
  - Excel: #217346 (verde)
  - Frecce: #4287f5 (blu)
