"""
YAML ↔ Excel Converter - YAML to Excel
Modulo per conversione custom YAML in Excel
Formato specifico per secrets.rlist

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
import yaml
from openpyxl import Workbook
import traceback
from typing import Any, Dict, List, Optional
from yamlconverter.utils.i18n import get_i18n


def flatten_to_name_secret_value(data: Dict[str, Any], parent_key: str = '') -> List[Dict[str, str]]:
    """
    Appiattisce la struttura YAML gerarchica in una lista di record Name/Secret/Value.
    
    Formato atteso YAML:
    Connections:
      CONNECTION_NAME:
        - secret: "$$SECRET_NAME$$"
          value: "secret_value"
        - secret: "$$ANOTHER_SECRET$$"
          value: "another_value"
    
    Formato output Excel (nuovo formato con 3 colonne):
    Name: CONNECTION_NAME[0], Secret: $$SECRET_NAME$$, Value: secret_value
    Name: CONNECTION_NAME[1], Secret: $$ANOTHER_SECRET$$, Value: another_value
    
    Args:
        data: Dizionario YAML da convertire
        parent_key: Chiave parent per la ricorsione
        
    Returns:
        Lista di dizionari con chiavi 'Name', 'Secret' e 'Value'
    """
    rows = []
    
    # Se c'è una chiave "Connections" al primo livello, la saltiamo
    if parent_key == '' and 'Connections' in data:
        data = data['Connections']
    
    for key, value in data.items():
        # Costruisce il nome completo
        full_key = f"{parent_key}.{key}" if parent_key else key
        
        if isinstance(value, list):
            # Lista di elementi (tipicamente dizionari con secret/value)
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    # Ogni elemento della lista è un dizionario con secret/value
                    # Crea una singola riga con Name[index], Secret, Value
                    name = f"{full_key}[{index}]"
                    secret = str(item.get('secret', ''))
                    val = str(item.get('value', ''))
                    rows.append({'Name': name, 'Secret': secret, 'Value': val})
                else:
                    # Elemento semplice nella lista
                    name = f"{full_key}[{index}]"
                    rows.append({'Name': name, 'Secret': '', 'Value': str(item)})
        
        elif isinstance(value, dict):
            # Dizionario annidato - ricorsione
            rows.extend(flatten_to_name_secret_value(value, full_key))
        
        else:
            # Valore semplice
            rows.append({'Name': full_key, 'Secret': '', 'Value': str(value)})
    
    return rows


def custom_yaml_to_excel(yaml_file: str, excel_file: str, i18n=None) -> tuple:
    """
    Converte un file YAML in formato custom per secrets.rlist in Excel.
    
    Args:
        yaml_file: Path del file YAML di input
        excel_file: Path del file Excel di output
        i18n: Oggetto i18n per la localizzazione (opzionale)
        
    Returns:
        Tupla (success, warnings) dove success è bool e warnings è lista di stringhe
    """
    # Inizializza i18n se non passato
    if i18n is None:
        i18n = get_i18n()
    
    warnings = []
    try:
        # Prima controlla duplicati leggendo il file come testo
        # (yaml.safe_load sovrascrive automaticamente le chiavi duplicate)
        duplicates = set()
        with open(yaml_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
            # Cerca pattern di chiavi al livello 1 (sotto Connections)
            # Pattern: 2 spazi + nome + ':'
            import re
            level1_keys = []
            in_connections = False
            
            for line in lines:
                # Rileva quando siamo dentro Connections
                if re.match(r'^Connections:\s*$', line):
                    in_connections = True
                    continue
                
                if in_connections:
                    # Chiave di livello 0 (fine Connections)
                    if re.match(r'^[A-Za-z]', line) and ':' in line:
                        break
                    
                    # Chiave di livello 1 (2 spazi)
                    match = re.match(r'^  ([A-Za-z0-9_-]+):\s*$', line)
                    if match:
                        key_name = match.group(1)
                        if key_name in level1_keys:
                            duplicates.add(key_name)
                        level1_keys.append(key_name)
        
        if duplicates:
            warnings.append(f"{i18n.t('warning_duplicates_found')}:")
            for dup in sorted(duplicates):
                warnings.append(f"  - {dup} {i18n.t('converted_only_first')}")
            try:
                print("\n".join(warnings))
            except UnicodeEncodeError:
                pass  # Ignora errori di encoding nei print
        
        # Legge il file YAML
        with open(yaml_file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
        
        if yaml_data is None:
            raise ValueError(i18n.t("empty_yaml"))
        
        # Converte in formato Name/Secret/Value
        rows = flatten_to_name_secret_value(yaml_data)
        
        if not rows:
            raise ValueError(i18n.t("no_data_to_convert"))
        
        # Crea workbook e worksheet
        wb = Workbook()
        ws = wb.active
        ws.title = 'Connections'
        
        # Scrive gli header
        ws.append(['Name', 'Secret', 'Value'])
        
        # Scrive i dati
        for row in rows:
            ws.append([row.get('Name', ''), row.get('Secret', ''), row.get('Value', '')])
        
        # Salva il file Excel
        wb.save(excel_file)
        
        try:
            print(f"{i18n.t('converted')} {yaml_file} -> {excel_file}")
            print(f"  {len(rows)} {i18n.t('rows_created')}")
        except UnicodeEncodeError:
            pass  # Ignora errori di encoding
        return (True, warnings, None)
    
    except yaml.YAMLError as e:
        error_msg = f"{i18n.t('yaml_syntax_error')}: {e}\n\n"
        error_msg += f"{i18n.t('suggestions')}:\n"
        error_msg += f"- {i18n.t('suggestion_quotes')}\n"
        error_msg += f"- {i18n.t('suggestion_indentation')}\n"
        error_msg += f"- {i18n.t('suggestion_no_tabs')}"
        try:
            print(f"{i18n.t('error')}: {error_msg}")
        except UnicodeEncodeError:
            pass
        return (False, warnings, error_msg)
    except Exception as e:
        error_details = traceback.format_exc()
        error_msg = f"{i18n.t('error_conversion_yaml_excel')}: {e}\n\n{i18n.t('error_details')}:\n{error_details}"
        try:
            print(f"{i18n.t('error')}: {error_msg}")
        except UnicodeEncodeError:
            pass
        return (False, warnings, error_msg)


if __name__ == "__main__":
    # Test del modulo
    import sys
    from yamlconverter.utils.i18n import get_i18n
    
    i18n = get_i18n()
    
    if len(sys.argv) == 3:
        yaml_file = sys.argv[1]
        excel_file = sys.argv[2]
        success, warnings, error = custom_yaml_to_excel(yaml_file, excel_file, i18n)
        sys.exit(0 if success else 1)
    else:
        print(f"{i18n.t('usage')}: python custom_yaml_to_excel.py <file.yml> <file.xlsx>")
        sys.exit(1)
