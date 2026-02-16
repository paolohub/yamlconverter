"""
YAML ↔ Excel Converter - Internationalization
Modulo per la gestione delle traduzioni multilingua

Copyright (C) 2026  Paolo Cardamone

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import json
import os
import locale
from typing import Dict, Any


def get_system_language() -> str:
    """
    Rileva la lingua del sistema operativo.
    
    Returns:
        Codice lingua ('it', 'en', ecc.)
    """
    try:
        # Ottiene la lingua del sistema
        system_locale = locale.getdefaultlocale()[0]
        if system_locale:
            # Estrae solo il codice lingua (es: 'it' da 'it_IT')
            lang_code = system_locale.split('_')[0].lower()
            # Verifica se la lingua è supportata
            supported_languages = ['it', 'en']
            if lang_code in supported_languages:
                return lang_code
    except Exception:
        pass
    
    # Default: inglese
    return 'en'


class I18n:
    """Classe per gestire le traduzioni multilingua"""
    
    def __init__(self, language: str = None, translations_dir: str = None):
        """
        Inizializza il sistema di traduzioni.
        
        Args:
            language: Codice lingua (es: 'it', 'en'). Se None, usa la lingua di sistema.
            translations_dir: Directory contenente i file di traduzione. 
                            Se None, usa la directory 'translations' del package.
        """
        # Se non viene specificata una lingua, usa quella del sistema
        if language is None:
            language = get_system_language()
        self.language = language
        
        # Imposta la directory delle traduzioni
        if translations_dir is None:
            # Default: cerca nella root del progetto
            self.translations_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                'translations'
            )
        else:
            self.translations_dir = translations_dir
        
        self.translations: Dict[str, Any] = {}
        self.load_translations()
    
    def load_translations(self):
        """Carica le traduzioni dalla directory translations/"""
        translation_file = os.path.join(self.translations_dir, f'{self.language}.json')
        
        if os.path.exists(translation_file):
            with open(translation_file, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        else:
            # Fallback alle traduzioni italiane integrate
            self.translations = self._get_fallback_translations()
    
    def _get_fallback_translations(self) -> Dict[str, Any]:
        """Traduzioni di fallback integrate nel codice"""
        if self.language == 'en':
            return {
                "app_title": "YAML ↔ Excel Converter",
                "conversion_mode": "Conversion Mode",
                "yaml_to_excel": "YAML → Excel",
                "excel_to_yaml": "Excel → YAML",
                "format_info": "Format: secrets.rlist (Name/Value)",
                "input_file": "Input File (drag here):",
                "browse": "Browse...",
                "output_file": "Output File:",
                "gpg_password": "GPG Password:",
                "encrypt_output": "Encrypt output with GPG (creates .gpg file)",
                "convert": "Convert",
                "log": "Log:",
                "clear_log": "Clear Log",
                "language": "Language:",
                "success": "Success",
                "error": "Error",
                "warning": "Warning",
                "conversion_success": "Conversion completed successfully!",
                "input_file_required": "Please select an input file",
                "output_file_required": "Please select an output file",
                "file_not_found": "Input file not found",
                "password_required": "Password required to decrypt the GPG file",
                "decryption_failed": "Failed to decrypt file. Check your password.",
                "encryption_failed": "Failed to encrypt file.",
                "conversion_failed": "Conversion failed. Check the log for details.",
                "gpg_not_installed": "GPG is not installed or not found in the system PATH.",
                "invalid_excel": "Invalid Excel file or missing Name/Value columns",
                "invalid_yaml": "Invalid YAML file format",
                "starting_conversion": "Starting conversion...",
                "reading_file": "Reading file...",
                "writing_file": "Writing file...",
                "decrypting_file": "Decrypting GPG file...",
                "encrypting_file": "Encrypting file with GPG...",
                "conversion_complete": "Conversion complete!",
                "error_occurred": "An error occurred:",
            }
        else:  # italiano
            return {
                "app_title": "Convertitore YAML ↔ Excel",
                "conversion_mode": "Modalità di Conversione",
                "yaml_to_excel": "YAML → Excel",
                "excel_to_yaml": "Excel → YAML",
                "format_info": "Formato: secrets.rlist (Name/Value)",
                "input_file": "File di Input (trascina qui):",
                "browse": "Sfoglia...",
                "output_file": "File di Output:",
                "gpg_password": "Password GPG:",
                "encrypt_output": "Cripta output con GPG (crea file .gpg)",
                "convert": "Converti",
                "log": "Log:",
                "clear_log": "Pulisci Log",
                "language": "Lingua:",
                "success": "Successo",
                "error": "Errore",
                "warning": "Avviso",
                "conversion_success": "Conversione completata con successo!",
                "input_file_required": "Seleziona un file di input",
                "output_file_required": "Seleziona un file di output",
                "file_not_found": "File di input non trovato",
                "password_required": "Password necessaria per decifrare il file GPG",
                "decryption_failed": "Impossibile decifrare il file. Verifica la password.",
                "encryption_failed": "Impossibile cifrare il file.",
                "conversion_failed": "Conversione fallita. Controlla il log per i dettagli.",
                "gpg_not_installed": "GPG non è installato o non è nel PATH di sistema.",
                "invalid_excel": "File Excel non valido o colonne Name/Value mancanti",
                "invalid_yaml": "Formato YAML non valido",
                "starting_conversion": "Inizio conversione...",
                "reading_file": "Lettura file...",
                "writing_file": "Scrittura file...",
                "decrypting_file": "Decifratura file GPG...",
                "encrypting_file": "Cifratura file con GPG...",
                "conversion_complete": "Conversione completata!",
                "error_occurred": "Si è verificato un errore:",
            }
    
    def t(self, key: str, default: str = None) -> str:
        """
        Ottiene la traduzione per una chiave.
        
        Args:
            key: Chiave della traduzione
            default: Valore di default se la chiave non esiste
            
        Returns:
            Stringa tradotta
        """
        return self.translations.get(key, default or key)
    
    def get(self, key: str, default: str = None) -> str:
        """
        Alias per t() - ottiene la traduzione per una chiave.
        
        Args:
            key: Chiave della traduzione
            default: Valore di default se la chiave non esiste
            
        Returns:
            Stringa tradotta
        """
        return self.t(key, default)
    
    @property
    def current_language(self) -> str:
        """Restituisce la lingua corrente"""
        return self.language
    
    def set_language(self, language: str):
        """Cambia la lingua corrente"""
        self.language = language
        self.load_translations()
    
    def get_available_languages(self) -> list:
        """Restituisce la lista delle lingue disponibili"""
        languages = []
        if os.path.exists(self.translations_dir):
            for file in os.listdir(self.translations_dir):
                if file.endswith('.json'):
                    lang_code = file[:-5]  # Remove .json
                    languages.append(lang_code)
        return languages if languages else ['it', 'en']


# Istanza globale
_i18n = I18n()


def get_i18n() -> I18n:
    """Ottiene l'istanza globale di I18n"""
    return _i18n


def t(key: str, default: str = None) -> str:
    """Shortcut per ottenere una traduzione"""
    return _i18n.t(key, default)


def set_language(language: str):
    """Shortcut per cambiare lingua"""
    _i18n.set_language(language)
