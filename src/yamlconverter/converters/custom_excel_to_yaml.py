"""
YAML ↔ Excel Converter - Excel to YAML
Modulo per conversione custom Excel in YAML
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
import openpyxl
import re
import traceback
from typing import Any, Dict, List, Optional
from collections import defaultdict
from yamlconverter.utils.i18n import get_i18n


def quote_yaml_value(value: str) -> str:
    """
    Quota un valore per YAML in modo sicuro gestendo caratteri speciali.
    
    Strategia:
    - Se contiene " ma non ', usa singoli apici (no escape necessario)
    - Se contiene ' ma non ", usa doppi apici
    - Se contiene entrambi, usa doppi apici con escape di backslash e "
    - Altrimenti usa doppi apici standard
    
    Args:
        value: Valore da quotare
        
    Returns:
        Valore quotato correttamente per YAML
    """
    value = str(value).strip()
    
    has_double = '"' in value
    has_single = "'" in value
    
    if has_double and not has_single:
        # Usa singoli apici - nessun escape necessario per "
        return f"'{value}'"
    elif has_double and has_single:
        # Contiene entrambi - usa doppi apici con escape
        # Prima escape backslash, poi doppi apici
        escaped = value.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'
    elif has_single and not has_double:
        # Contiene solo singoli apici - usa doppi apici
        return f'"{value}"'
    else:
        # Nessun carattere speciale - usa doppi apici standard
        return f'"{value}"'


def parse_name_to_structure(name: str) -> tuple:
    """
    Analizza una stringa Name e la converte in una struttura di percorso.
    
    Esempi (nuovo formato):
        "SAP_SOAP[0]" -> ('SAP_SOAP', 0)
        "SAP_SOAP[1]" -> ('SAP_SOAP', 1)
        "SIMPLE_KEY" -> ('SIMPLE_KEY',)
    
    Args:
        name: Stringa Name dal formato Excel
        
    Returns:
        Tupla con i componenti del percorso
    """
    parts = []
    
    # Pattern per identificare chiavi con indici array
    # Es: "KEY[0]" -> ["KEY", "[0]"]
    segments = re.split(r'\.', name)
    
    for segment in segments:
        # Cerca pattern tipo "key[index]"
        match = re.match(r'^(.+?)\[(\d+)\]$', segment)
        if match:
            key = match.group(1)
            index = int(match.group(2))
            parts.append(key)
            parts.append(index)
        else:
            parts.append(segment)
    
    return tuple(parts)


def rebuild_yaml_structure(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Ricostruisce la struttura YAML gerarchica da una lista di record Name/Secret/Value.
    
    Args:
        rows: Lista di dizionari con chiavi 'Name', 'Secret' e 'Value'
        
    Returns:
        Dizionario con struttura YAML gerarchica
    """
    # Struttura temporanea per raggruppare i dati
    connections = defaultdict(list)
    connection_first_seen = {}
    
    for row in rows:
        name = row.get('Name', '')
        secret = row.get('Secret', '')
        value = row.get('Value', '')
        
        if not name:
            continue
        
        # Analizza la struttura del nome
        parts = parse_name_to_structure(name)
        
        if len(parts) >= 2:
            # Formato: CONNECTION_NAME[index]
            connection_name = parts[0]
            index = parts[1]
            
            # Traccia la prima occorrenza
            if connection_name not in connection_first_seen:
                connection_first_seen[connection_name] = index
            
            # Assicura che ci siano abbastanza elementi nella lista
            while len(connections[connection_name]) <= index:
                connections[connection_name].append({})
            
            # Imposta secret e value come dizionario
            connections[connection_name][index]['secret'] = secret
            connections[connection_name][index]['value'] = value
        
        elif len(parts) == 1:
            # Formato semplice: KEY (senza array)
            if parts[0] not in connection_first_seen:
                connection_first_seen[parts[0]] = 0
            connections[parts[0]] = value
    
    # Costruisce la struttura finale
    result = {
        'Connections': dict(connections)
    }
    
    return result


def format_yaml_custom(data: Dict[str, Any]) -> str:
    """
    Formatta manualmente il YAML con indentazione custom per secrets.rlist.
    
    Args:
        data: Dizionario con struttura YAML
        
    Returns:
        Stringa YAML formattata
    """
    lines = []
    connections = data.get('Connections', {})
    
    lines.append('Connections:')
    
    for conn_name, items in connections.items():
        lines.append(f'  {conn_name}:')
        
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    # Primo campo (secret) con 4 spazi + trattino
                    first_key = True
                    for key, value in item.items():
                        # Assicura che key e value siano puliti
                        clean_key = str(key).strip()
                        clean_value = str(value).strip()
                        # Quota il valore in modo sicuro
                        quoted_value = quote_yaml_value(clean_value)
                        if first_key:
                            lines.append(f'    - {clean_key}: {quoted_value}')
                            first_key = False
                        else:
                            # Campi successivi (value) con 6 spazi
                            lines.append(f'      {clean_key}: {quoted_value}')
        else:
            # Valore semplice
            quoted_items = quote_yaml_value(str(items))
            lines.append(f'    - {quoted_items}')
    
    return '\n'.join(lines) + '\n'


def custom_excel_to_yaml(excel_file: str, yaml_file: str, i18n=None) -> tuple:
    """
    Converte un file Excel in formato custom per secrets.rlist in YAML.
    
    Args:
        excel_file: Path del file Excel di input
        yaml_file: Path del file YAML di output
        i18n: Oggetto i18n per la localizzazione (opzionale)
        
    Returns:
        Tupla (success, warnings) dove success è bool e warnings è lista di stringhe
    """
    # Inizializza i18n se non passato
    if i18n is None:
        i18n = get_i18n()
    
    warnings = []
    try:
        # Legge il file Excel
        wb = openpyxl.load_workbook(excel_file)
        ws = wb.active
        
        # Legge i dati
        rows = []
        headers = []
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i == 0:
                # Prima riga: headers
                headers = [cell if cell else '' for cell in row]
                # Verifica che abbia le colonne corrette
                if 'Name' not in headers or 'Secret' not in headers or 'Value' not in headers:
                    raise ValueError(i18n.t("missing_columns"))
                name_idx = headers.index('Name')
                secret_idx = headers.index('Secret')
                value_idx = headers.index('Value')
            else:
                # Dati
                if row[name_idx]:  # Salta righe vuote
                    # Pulisce i valori rimuovendo newline interni e spazi trailing/leading
                    name_value = str(row[name_idx]).strip().replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ') if row[name_idx] else ''
                    secret_value = str(row[secret_idx]).strip().replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ') if row[secret_idx] else ''
                    value_value = str(row[value_idx]).strip().replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ') if row[value_idx] else ''
                    # Rimuove spazi multipli consecutivi
                    name_value = ' '.join(name_value.split())
                    secret_value = ' '.join(secret_value.split())
                    value_value = ' '.join(value_value.split())
                    rows.append({
                        'Name': name_value,
                        'Secret': secret_value,
                        'Value': value_value
                    })
        
        # Ricostruisce la struttura YAML
        yaml_data = rebuild_yaml_structure(rows)
        
        # Scrive il file YAML con formattazione custom e line ending Unix (LF)
        with open(yaml_file, 'w', encoding='utf-8', newline='\n') as f:
            yaml_content = format_yaml_custom(yaml_data)
            f.write(yaml_content)
        
        try:
            print(f"{i18n.t('converted')} {excel_file} -> {yaml_file}")
            connections = yaml_data.get('Connections', {})
            print(f"  {len(connections)} {i18n.t('connections_rebuilt')}")
        except UnicodeEncodeError:
            pass
        return (True, warnings, None)
    
    except Exception as e:
        error_details = traceback.format_exc()
        error_msg = f"{i18n.t('error_conversion_excel_yaml')}: {e}\n\n{i18n.t('error_details')}:\n{error_details}"
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
        excel_file = sys.argv[1]
        yaml_file = sys.argv[2]
        success, warnings, error = custom_excel_to_yaml(excel_file, yaml_file, i18n)
        sys.exit(0 if success else 1)
    else:
        print(f"{i18n.t('usage')}: python custom_excel_to_yaml.py <file.xlsx> <file.yml>")
        sys.exit(1)
