# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-29

### Added
- 🔄 Conversione bidirezionale YAML ↔ Excel per formato secrets.rlist
- 🔐 Supporto completo GPG per encryption/decryption file sensibili
- 🌍 Interfaccia multilingua (Italiano / English)
- 🎨 Interfaccia grafica con drag & drop per input/output
- 📝 Log operazioni in tempo reale
- 🚨 Rilevamento automatico chiavi YAML duplicate
- 📦 Build eseguibile Windows standalone (11.5 MB)
- 🐧 Build AppImage per Linux
- ✅ Compatibilità cross-platform (Windows, Linux, macOS)
- 🔧 Hook personalizzati PyInstaller per tkinterdnd2
- 📖 Documentazione completa (README, BUILD_INSTRUCTIONS)
- 🎯 Rilevamento automatico modalità conversione
- 💾 Salvataggio file decriptati nella stessa cartella del file criptato
- 🔄 Normalizzazione path per sistema operativo corrente

### Technical
- Python 3.8+ support
- Ottimizzazioni dimensione eseguibile (-69% vs versione pandas)
- Dipendenze minimali: openpyxl, pyyaml, tkinterdnd2, python-gnupg
- GPL-3.0 License
- Built with GitHub Copilot (Claude Sonnet 4.5)

### Build System
- Windows: PyInstaller con spec ottimizzato
- Linux: AppImage con script automatico
- Hook personalizzati per evitare warning build
- Support per Windows (win64), Linux (linux64), macOS (osx64)

[1.0.0]: https://github.com/yourusername/yamlconverter/releases/tag/v1.0.0
