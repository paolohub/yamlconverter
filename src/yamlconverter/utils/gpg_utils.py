"""
YAML ↔ Excel Converter - GPG Utilities
Modulo per gestire la crittografia/decrittografia GPG dei file

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
import gnupg
from yamlconverter.utils.i18n import get_i18n


def decrypt_file(input_file: str, password: str, i18n=None) -> tuple:
    """
    Decripta un file GPG con password.
    
    Args:
        input_file: Path del file criptato
        password: Password per decrittare
        i18n: Oggetto i18n per la localizzazione (opzionale)
        
    Returns:
        Tupla (success, decrypted_content, error_message)
    """
    if i18n is None:
        i18n = get_i18n()
    
    try:
        gpg = gnupg.GPG()
        
        # Legge il file criptato
        with open(input_file, 'rb') as f:
            encrypted_data = f.read()
        
        # Decripta
        decrypted = gpg.decrypt(encrypted_data, passphrase=password)
        
        if decrypted.ok:
            return (True, decrypted.data.decode('utf-8'), None)
        else:
            return (False, None, f"{i18n.t('gpg_decryption_error')}: {decrypted.status}")
    
    except Exception as e:
        return (False, None, f"{i18n.t('generic_error')}: {str(e)}")


def encrypt_file(content: str, output_file: str, password: str, i18n=None) -> tuple:
    """
    Cripta un file con password usando GPG (symmetric encryption).
    
    Args:
        content: Contenuto da criptare
        output_file: Path del file di output
        password: Password per criptare
        i18n: Oggetto i18n per la localizzazione (opzionale)
        
    Returns:
        Tupla (success, error_message)
    """
    if i18n is None:
        i18n = get_i18n()
    
    try:
        gpg = gnupg.GPG()
        
        # Cripta il contenuto con cifratura simmetrica
        encrypted = gpg.encrypt(
            content.encode('utf-8'),
            recipients=None,
            symmetric=True,
            passphrase=password,
            armor=False  # Output binario
        )
        
        if encrypted.ok:
            # Scrive il file criptato
            with open(output_file, 'wb') as f:
                f.write(encrypted.data)
            return (True, None)
        else:
            return (False, f"{i18n.t('gpg_encryption_error')}: {encrypted.status}")
    
    except Exception as e:
        return (False, f"{i18n.t('generic_error')}: {str(e)}")


def is_encrypted_file(file_path: str) -> bool:
    """
    Verifica se un file è criptato con GPG.
    
    Args:
        file_path: Path del file da verificare
        
    Returns:
        True se il file è criptato, False altrimenti
    """
    try:
        with open(file_path, 'rb') as f:
            # Legge i primi byte per verificare la firma GPG
            header = f.read(6)
            # File GPG iniziano con questi magic bytes
            # 0x85 = GPG encrypted data packet tag
            # 0x8c = GPG compressed data packet
            return header[0] in [0x85, 0x8c] or header.startswith(b'\x84') or header.startswith(b'\x8c')
    except Exception:
        return False
