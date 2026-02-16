"""
YAML ↔ Excel Converter
Applicazione GUI per convertire file YAML in Excel e viceversa

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
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import traceback
from tkinterdnd2 import TkinterDnD, DND_FILES
from yamlconverter.converters.custom_yaml_to_excel import custom_yaml_to_excel
from yamlconverter.converters.custom_excel_to_yaml import custom_excel_to_yaml
from yamlconverter.utils.gpg_utils import decrypt_file, encrypt_file
from yamlconverter.utils.i18n import get_i18n, set_language


class YAMLExcelConverterApp:
    def __init__(self, root):
        self.root = root
        self.i18n = get_i18n()
        self.root.title(self.i18n.t("app_title"))
        self.root.geometry("700x600")
        self.root.minsize(700, 600)
        self.root.resizable(True, True)
        
        # Variabili
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.conversion_mode = tk.StringVar(value="yaml_to_excel")
        self.use_gpg_encrypt = tk.BooleanVar(value=False)
        self.gpg_password = tk.StringVar()
        self.show_password = tk.BooleanVar(value=False)
        # Imposta la lingua corrente in base alla lingua del sistema
        self.current_language = tk.StringVar(value=self.i18n.language)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configura il ridimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Header frame con titolo e selezione lingua
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)
        
        # Titolo
        self.title_label = ttk.Label(header_frame, text=self.i18n.t("app_title"), 
                               font=('Arial', 16, 'bold'))
        self.title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Selezione lingua
        lang_frame = ttk.Frame(header_frame)
        lang_frame.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Label(lang_frame, text="🌐", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 5))
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.current_language, 
                                  values=['it', 'en'], state='readonly', width=5)
        lang_combo.pack(side=tk.LEFT)
        lang_combo.bind('<<ComboboxSelected>>', self.change_language)
        
        # Selezione modalità di conversione
        self.mode_frame = ttk.LabelFrame(main_frame, text=self.i18n.t("conversion_mode"), padding="10")
        self.mode_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.radio_yaml_to_excel = ttk.Radiobutton(self.mode_frame, text=self.i18n.t("yaml_to_excel"), 
                                                    variable=self.conversion_mode, 
                                                    value="yaml_to_excel", command=self.on_mode_change)
        self.radio_yaml_to_excel.grid(row=0, column=0, padx=10)
        
        self.radio_excel_to_yaml = ttk.Radiobutton(self.mode_frame, text=self.i18n.t("excel_to_yaml"), 
                                                    variable=self.conversion_mode, 
                                                    value="excel_to_yaml", command=self.on_mode_change)
        self.radio_excel_to_yaml.grid(row=0, column=1, padx=10)
        
        # Info formato (sempre custom)
        self.format_label = ttk.Label(self.mode_frame, text=self.i18n.t("format_info"), 
                 foreground="gray")
        self.format_label.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        # File di input
        self.input_label = ttk.Label(main_frame, text=self.i18n.t("input_file"))
        self.input_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        self.input_entry = ttk.Entry(main_frame, textvariable=self.input_file, width=50)
        self.input_entry.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.browse_input_btn = ttk.Button(main_frame, text=self.i18n.t("browse"), command=self.browse_input)
        self.browse_input_btn.grid(row=3, column=2)
        
        # Configura drag and drop per input
        self.input_entry.drop_target_register(DND_FILES)
        self.input_entry.dnd_bind('<<Drop>>', self.drop_input)
        
        # Frame per password decrypt (dinamico, inizialmente nascosto)
        self.password_frame = ttk.Frame(main_frame)
        self.password_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 10))
        self.password_frame.grid_remove()  # Nasconde inizialmente
        
        self.password_label = ttk.Label(self.password_frame, text=self.i18n.t("gpg_password"))
        self.password_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.password_entry = ttk.Entry(self.password_frame, textvariable=self.gpg_password, show="*", width=40)
        self.password_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Bottone per mostrare/nascondere password
        self.show_password = tk.BooleanVar(value=False)
        self.toggle_password_btn = ttk.Button(self.password_frame, text="👁", width=3, command=self.toggle_password_visibility)
        self.toggle_password_btn.grid(row=0, column=2)
        
        self.password_frame.columnconfigure(1, weight=1)
        
        # File di output
        self.output_label = ttk.Label(main_frame, text=self.i18n.t("output_file"))
        self.output_label.grid(row=5, column=0, sticky=tk.W, pady=(15, 5))
        
        self.output_entry = ttk.Entry(main_frame, textvariable=self.output_file, width=50)
        self.output_entry.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.browse_output_btn = ttk.Button(main_frame, text=self.i18n.t("browse"), command=self.browse_output)
        self.browse_output_btn.grid(row=6, column=2)
        
        # Configura drag and drop per output
        self.output_entry.drop_target_register(DND_FILES)
        self.output_entry.dnd_bind('<<Drop>>', self.drop_output)
        
        # Frame per encrypt (dinamico, inizialmente nascosto)
        self.encrypt_frame = ttk.Frame(main_frame)
        self.encrypt_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        self.encrypt_frame.grid_remove()  # Nasconde inizialmente
        
        self.encrypt_check = ttk.Checkbutton(self.encrypt_frame, text=self.i18n.t("encrypt_output"), 
                       variable=self.use_gpg_encrypt, command=self.update_output_extension)
        self.encrypt_check.pack(side=tk.LEFT)
        
        # Frame per password encrypt (dinamico, inizialmente nascosto)
        self.password_encrypt_frame = ttk.Frame(main_frame)
        self.password_encrypt_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 10))
        self.password_encrypt_frame.grid_remove()  # Nasconde inizialmente
        
        self.password_encrypt_label = ttk.Label(self.password_encrypt_frame, text=self.i18n.t("gpg_password"))
        self.password_encrypt_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.password_encrypt_entry = ttk.Entry(self.password_encrypt_frame, textvariable=self.gpg_password, show="*", width=40)
        self.password_encrypt_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Bottone per mostrare/nascondere password encrypt
        self.toggle_password_encrypt_btn = ttk.Button(self.password_encrypt_frame, text="👁", width=3, command=self.toggle_password_visibility)
        self.toggle_password_encrypt_btn.grid(row=0, column=2)
        
        self.password_encrypt_frame.columnconfigure(1, weight=1)
        
        # Pulsante di conversione
        self.convert_btn = ttk.Button(main_frame, text=self.i18n.t("convert"), command=self.convert, 
                                style='Accent.TButton')
        self.convert_btn.grid(row=9, column=0, columnspan=3, pady=30, ipadx=20, ipady=5)
        
        # Area di log
        self.log_frame = ttk.LabelFrame(main_frame, text=self.i18n.t("log"), padding="10")
        self.log_frame.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        main_frame.rowconfigure(10, weight=1)
        
        # Scrollbar per il log
        scrollbar = ttk.Scrollbar(self.log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(self.log_frame, height=10, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Messaggio iniziale
        self.log(self.i18n.t("welcome_message") + "\n")
        
        # Imposta lo stato iniziale della UI
        self.update_encrypt_visibility()
    
    def change_language(self, event=None):
        """Cambia la lingua dell'interfaccia"""
        new_lang = self.current_language.get()
        set_language(new_lang)
        self.i18n = get_i18n()
        
        # Aggiorna tutti i testi dell'interfaccia
        self.root.title(self.i18n.t("app_title"))
        self.title_label.config(text=self.i18n.t("app_title"))
        self.mode_frame.config(text=self.i18n.t("conversion_mode"))
        self.radio_yaml_to_excel.config(text=self.i18n.t("yaml_to_excel"))
        self.radio_excel_to_yaml.config(text=self.i18n.t("excel_to_yaml"))
        self.format_label.config(text=self.i18n.t("format_info"))
        self.input_label.config(text=self.i18n.t("input_file"))
        self.browse_input_btn.config(text=self.i18n.t("browse"))
        self.output_label.config(text=self.i18n.t("output_file"))
        self.browse_output_btn.config(text=self.i18n.t("browse"))
        self.password_label.config(text=self.i18n.t("gpg_password"))
        self.password_encrypt_label.config(text=self.i18n.t("gpg_password"))
        self.encrypt_check.config(text=self.i18n.t("encrypt_output"))
        self.convert_btn.config(text=self.i18n.t("convert"))
        self.log_frame.config(text=self.i18n.t("log"))
        
        # Messaggio di cambio lingua
        lang_name = self.i18n.t("English") if new_lang == 'en' else self.i18n.t("Italiano")
        self.log(f"{self.i18n.t('language_changed')} {lang_name}\n")
    
    def update_file_labels(self):
        """Aggiorna i placeholder dei file in base alla modalità selezionata"""
        pass  # I label sono già generici
    
    def on_mode_change(self):
        """Chiamata quando l'utente cambia la modalità di conversione"""
        self.update_file_labels()
        self.update_encrypt_visibility()
        self.update_password_visibility()
    
    def toggle_password_visibility(self):
        """Mostra/nasconde la password in chiaro per entrambi i campi password"""
        if self.show_password.get():
            # Nasconde la password
            self.password_entry.config(show="*")
            self.password_encrypt_entry.config(show="*")
            self.toggle_password_btn.config(text="👁")
            self.toggle_password_encrypt_btn.config(text="👁")
            self.show_password.set(False)
        else:
            # Mostra la password
            self.password_entry.config(show="")
            self.password_encrypt_entry.config(show="")
            self.toggle_password_btn.config(text="🔒")
            self.toggle_password_encrypt_btn.config(text="🔒")
            self.show_password.set(True)
    
    def update_password_visibility(self):
        """Mostra/nasconde i campi password in base all'input o encrypt"""
        input_path = self.input_file.get()
        mode = self.conversion_mode.get()
        use_encrypt = self.use_gpg_encrypt.get()
        
        # Mostra password decrypt se input è .gpg in modalità yaml_to_excel
        if mode == "yaml_to_excel" and input_path.lower().endswith('.gpg'):
            self.password_frame.grid()
        else:
            self.password_frame.grid_remove()
            
        # Mostra password encrypt se encrypt è selezionato in modalità excel_to_yaml
        if mode == "excel_to_yaml" and use_encrypt:
            self.password_encrypt_frame.grid()
        else:
            self.password_encrypt_frame.grid_remove()
            
        # Pulisce la password quando i campi vengono nascosti
        if not (self.password_frame.winfo_viewable() or self.password_encrypt_frame.winfo_viewable()):
            self.gpg_password.set("")
    
    def update_encrypt_visibility(self):
        """Mostra/nasconde il frame encrypt in base alla modalità"""
        mode = self.conversion_mode.get()
        
        if mode == "excel_to_yaml":
            self.encrypt_frame.grid()
        else:
            self.encrypt_frame.grid_remove()
            self.use_gpg_encrypt.set(False)
            # Nascondi anche il frame password encrypt se visibile
            self.password_encrypt_frame.grid_remove()
    
    def update_output_extension(self):
        """Aggiunge o rimuove .gpg dall'estensione output quando encrypt è selezionato"""
        output_path = self.output_file.get()
        if not output_path:
            return
        
        if self.use_gpg_encrypt.get():
            # Aggiunge .gpg se non c'è già
            if not output_path.lower().endswith('.gpg'):
                self.output_file.set(output_path + '.gpg')
        else:
            # Rimuove .gpg se presente
            if output_path.lower().endswith('.gpg'):
                self.output_file.set(output_path[:-4])
        
        # Aggiorna la visibilità del campo password
        self.update_password_visibility()
    
    def detect_conversion_mode(self, input_path, output_path):
        """Rileva e imposta la modalità di conversione in base alle estensioni dei file"""
        input_ext = os.path.splitext(input_path)[1].lower() if input_path else ''
        output_ext = os.path.splitext(output_path)[1].lower() if output_path else ''
        
        # Estensioni valide
        yaml_exts = ['.yml', '.yaml', '.gpg']
        excel_exts = ['.xlsx', '.xls']
        
        # Valida le estensioni
        valid_input = input_ext in yaml_exts + excel_exts
        valid_output = output_ext in yaml_exts + excel_exts
        
        if not valid_input and input_path:
            self.log(f"⚠ {self.i18n.t('warning_extension_not_recognized')} ({input_ext}). {self.i18n.t('supported_formats')}: .yml, .yaml, .gpg, .xlsx\n")
            return False
        
        if not valid_output and output_path:
            self.log(f"⚠ {self.i18n.t('warning_extension_not_recognized')} ({output_ext}). {self.i18n.t('supported_formats')}: .yml, .yaml, .gpg, .xlsx\n")
            return False
        
        # Se è presente solo l'input, deduce la modalità dall'estensione dell'input
        if input_path and not output_path:
            if input_ext in yaml_exts:
                if self.conversion_mode.get() != "yaml_to_excel":
                    self.conversion_mode.set("yaml_to_excel")
                    self.log(f"✓ {self.i18n.t('mode_changed')}: {self.i18n.t('yaml_to_excel')}\n")
                self.update_password_visibility()
                self.update_encrypt_visibility()
                return True
            elif input_ext in excel_exts:
                if self.conversion_mode.get() != "excel_to_yaml":
                    self.conversion_mode.set("excel_to_yaml")
                    self.log(f"✓ {self.i18n.t('mode_changed')}: {self.i18n.t('excel_to_yaml')}\n")
                self.update_password_visibility()
                self.update_encrypt_visibility()
                return True
        
        # Determina la modalità di conversione quando sono presenti sia input che output
        if input_ext in yaml_exts and output_ext in excel_exts:
            if self.conversion_mode.get() != "yaml_to_excel":
                self.conversion_mode.set("yaml_to_excel")
                self.log(f"✓ {self.i18n.t('mode_changed')}: {self.i18n.t('yaml_to_excel')}\n")
            self.update_password_visibility()
            self.update_encrypt_visibility()
            return True
        elif input_ext in excel_exts and output_ext in yaml_exts:
            if self.conversion_mode.get() != "excel_to_yaml":
                self.conversion_mode.set("excel_to_yaml")
                self.log(f"✓ {self.i18n.t('mode_changed')}: {self.i18n.t('excel_to_yaml')}\n")
            self.update_password_visibility()
            self.update_encrypt_visibility()
            return True
        elif input_ext and output_ext:
            # Entrambe le estensioni sono presenti ma non compatibili
            if (input_ext in yaml_exts and output_ext in yaml_exts) or \
               (input_ext in excel_exts and output_ext in excel_exts):
                self.log(f"⚠ {self.i18n.t('warning_same_format')}\n")
                return False
        
        self.update_password_visibility()
        self.update_encrypt_visibility()
        return valid_input or valid_output
    
    def drop_input(self, event):
        """Gestisce il drop del file di input"""
        # Estrae il percorso del file dall'evento drop
        files = self.root.tk.splitlist(event.data)
        if files:
            file_path = files[0].strip('{}')  # Rimuove eventuali parentesi graffe
            file_path = os.path.normpath(file_path)  # Normalizza il path per il sistema operativo
            self.input_file.set(file_path)
            self.log(f"{self.i18n.t('input_file_dropped')}: {file_path}\n")
            
            # Suggerisce automaticamente il file di output (stessa logica di browse_input)
            base_name = os.path.splitext(file_path)[0]
            input_ext = os.path.splitext(file_path)[1].lower()
            
            # Se il file è .gpg, rimuove anche l'estensione .yml/.yaml dal base_name
            if input_ext == '.gpg':
                # Controlla se il base_name termina con .yml o .yaml
                if base_name.lower().endswith('.yml'):
                    base_name = base_name[:-4]
                elif base_name.lower().endswith('.yaml'):
                    base_name = base_name[:-5]
            
            # Determina l'estensione di output in base all'input
            if input_ext in ['.yml', '.yaml', '.gpg']:
                self.output_file.set(os.path.normpath(base_name + ".xlsx"))
            elif input_ext in ['.xlsx', '.xls']:
                self.output_file.set(os.path.normpath(base_name + ".yml"))
            
            # Rileva e imposta la modalità di conversione
            self.detect_conversion_mode(file_path, self.output_file.get())
    
    def drop_output(self, event):
        """Gestisce il drop del file di output"""
        # Estrae il percorso del file dall'evento drop
        files = self.root.tk.splitlist(event.data)
        if files:
            file_path = files[0].strip('{}')  # Rimuove eventuali parentesi graffe
            file_path = os.path.normpath(file_path)  # Normalizza il path per il sistema operativo
            self.output_file.set(file_path)
            self.log(f"{self.i18n.t('output_file_dropped')}: {file_path}\n")
            
            # Rileva e imposta la modalità di conversione
            self.detect_conversion_mode(self.input_file.get(), file_path)
        
    def browse_input(self):
        """Apre il dialog per selezionare il file di input"""
        mode = self.conversion_mode.get()
        
        if mode == "yaml_to_excel":
            filetypes = [("YAML files", "*.yaml *.yml *.gpg"), ("All files", "*.*")]
        else:
            filetypes = [("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        
        filename = filedialog.askopenfilename(title="Seleziona file di input", filetypes=filetypes)
        if filename:
            self.input_file.set(filename)
            # Suggerisce un nome per l'output
            base_name = os.path.splitext(filename)[0]
            input_ext = os.path.splitext(filename)[1].lower()
            
            # Se il file è .gpg, rimuove anche l'estensione .yml/.yaml dal base_name
            if input_ext == '.gpg':
                # Controlla se il base_name termina con .yml o .yaml
                if base_name.lower().endswith('.yml'):
                    base_name = base_name[:-4]
                elif base_name.lower().endswith('.yaml'):
                    base_name = base_name[:-5]
            
            # Determina l'estensione di output in base all'input
            if input_ext in ['.yml', '.yaml', '.gpg']:
                self.output_file.set(os.path.normpath(base_name + ".xlsx"))
            elif input_ext in ['.xlsx', '.xls']:
                self.output_file.set(os.path.normpath(base_name + ".yml"))
            
            self.log(f"{self.i18n.t('input_file_selected')}: {filename}\n")
            
            # Rileva e imposta la modalità di conversione
            self.detect_conversion_mode(filename, self.output_file.get())
    
    def browse_output(self):
        """Apre il dialog per selezionare il file di output"""
        mode = self.conversion_mode.get()
        
        if mode == "yaml_to_excel":
            filetypes = [("Excel files", "*.xlsx"), ("All files", "*.*")]
            default_ext = ".xlsx"
        else:
            filetypes = [("YAML files", "*.yaml *.yml"), ("All files", "*.*")]
            default_ext = ".yml"  # Sempre .yml per formato custom
        
        filename = filedialog.asksaveasfilename(title="Seleziona file di output", 
                                               filetypes=filetypes, defaultextension=default_ext)
        if filename:
            self.output_file.set(filename)
            self.log(f"{self.i18n.t('output_file_selected')}: {filename}\n")
            
            # Rileva e imposta la modalità di conversione
            self.detect_conversion_mode(self.input_file.get(), filename)
    
    def log(self, message):
        """Aggiunge un messaggio al log"""
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def convert(self):
        """Esegue la conversione"""
        input_file = self.input_file.get()
        output_file = self.output_file.get()
        mode = self.conversion_mode.get()
        use_encrypt = self.use_gpg_encrypt.get()
        password = self.gpg_password.get()
        
        # Determina se input è crittografato
        input_is_encrypted = input_file.lower().endswith('.gpg')
        
        # Determina il path del file in chiaro (senza .gpg)
        if output_file.lower().endswith('.gpg'):
            clear_output_file = output_file[:-4]  # Rimuove .gpg
        else:
            clear_output_file = output_file
        
        # Validazione
        if not input_file or not output_file:
            messagebox.showerror(self.i18n.t("error"), self.i18n.t("input_file_required") + " / " + self.i18n.t("output_file_required"))
            return
        
        if not os.path.exists(input_file):
            messagebox.showerror(self.i18n.t("error"), self.i18n.t("file_not_found"))
            return
        
        # Valida password GPG
        if input_is_encrypted and not password:
            messagebox.showerror(self.i18n.t("error"), self.i18n.t("password_required"))
            return
        
        if use_encrypt and not password:
            messagebox.showerror(self.i18n.t("error"), self.i18n.t("password_required"))
            return
        
        # Valida le estensioni
        if not self.detect_conversion_mode(input_file, output_file):
            err_msg = self.i18n.t("invalid_excel") if mode == "excel_to_yaml" else self.i18n.t("invalid_yaml")
            messagebox.showerror(self.i18n.t("error"), err_msg)
            return
        
        # Controlla se il file di output esiste già
        file_to_check = None
        if mode == "excel_to_yaml":
            # Per Excel → YAML: controlla il file .yml e/o .gpg se encrypt è attivo
            if os.path.exists(clear_output_file) or (use_encrypt and os.path.exists(output_file)):
                file_to_check = output_file if use_encrypt else clear_output_file
        elif mode == "yaml_to_excel":
            # Per YAML → Excel: controlla il file .xlsx
            if os.path.exists(output_file):
                file_to_check = output_file
        
        if file_to_check:
            # Chiedi conferma all'utente
            response = messagebox.askyesno(
                self.i18n.t("file_exists"),
                self.i18n.t("file_exists_overwrite"),
                icon='warning'
            )
            if not response:
                self.log(f"✗ {self.i18n.t('conversion_failed')}: {self.i18n.t('file_exists')}\n")
                return
        
        # Esegue la conversione
        self.log(f"\n{'='*50}\n")
        self.log(f"{self.i18n.t('starting_conversion')}: {mode}\n")
        self.log(f"Input: {input_file}\n")
        self.log(f"Output: {clear_output_file}\n")
        if use_encrypt:
            self.log(f"{self.i18n.t('output_encrypted')}: {output_file}\n")
        self.log(f"{self.i18n.t('format_info')}\n")
        if input_is_encrypted:
            self.log(f"{self.i18n.t('input_encrypted')}: {self.i18n.t('yes')}\n")
        if use_encrypt:
            self.log(f"{self.i18n.t('encrypt_output_label')}: {self.i18n.t('yes')}\n")
        self.log(f"{'='*50}\n")
        
        try:
            success = False
            warnings = []
            temp_input = None
            
            # Decripta input se è un file .gpg
            if input_is_encrypted:
                self.log(f"{self.i18n.t('decrypting_file')}...\n")
                success_decrypt, decrypted_content, error = decrypt_file(input_file, password, self.i18n)
                if not success_decrypt:
                    self.log(f"✗ {self.i18n.t('error_occurred')}\n{error}\n")
                    messagebox.showerror(self.i18n.t("error"), f"{self.i18n.t('decryption_failed')}\n{error}")
                    return
                
                # Salva il contenuto decrittato nella stessa cartella del file criptato
                # Rimuove l'estensione .gpg dal nome del file
                temp_input = input_file[:-4] if input_file.lower().endswith('.gpg') else input_file + '.decrypted'
                # Normalizza line endings a LF prima di salvare
                normalized_content = decrypted_content.replace('\r\n', '\n').replace('\r', '\n')
                with open(temp_input, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(normalized_content)
                self.log(f"✓ {self.i18n.t('decrypting_file')} - OK\n")
                self.log(f"{self.i18n.t('decrypted_file_saved')}: {temp_input}\n")
            
            # Determina quale file usare per l'input (decrittato o originale)
            actual_input = temp_input if input_is_encrypted else input_file
            
            # Prepara file temporaneo per output se serve encryption
            # Il file in chiaro sarà sempre salvato nel path senza .gpg
            actual_output = clear_output_file
            
            # Esegui conversione (sempre custom format)
            if mode == "yaml_to_excel":
                self.log(f"{self.i18n.t('conversion_with_format')}\n")
                success, warnings, error_msg = custom_yaml_to_excel(actual_input, output_file, self.i18n)
                if warnings:
                    for warning in warnings:
                        self.log(warning + "\n")
                if not success and error_msg:
                    self.log(f"✗ {error_msg}\n")
            else:  # excel_to_yaml
                self.log(f"{self.i18n.t('conversion_with_format')}\n")
                success, warnings, error_msg = custom_excel_to_yaml(input_file, actual_output, self.i18n)
                if warnings:
                    for warning in warnings:
                        self.log(warning + "\n")
                if not success and error_msg:
                    self.log(f"✗ {error_msg}\n")
            
            # Non elimina più il file decriptato, ora rimane salvato nella stessa cartella del file criptato
            
            # Se necessario, cripta il file di output (già salvato in chiaro in clear_output_file)
            if success and use_encrypt and mode == "excel_to_yaml":
                self.log(f"{self.i18n.t('encrypting_file')}...\n")
                with open(clear_output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                success_encrypt, error = encrypt_file(content, output_file, password, self.i18n)
                
                if not success_encrypt:
                    self.log(f"✗ {self.i18n.t('error_occurred')}:\n{error}\n")
                    messagebox.showerror(self.i18n.t("error"), f"{self.i18n.t('encryption_failed')}\n{error}")
                    return
                
                self.log(f"✓ {self.i18n.t('encrypting_file')} - OK\n")
            
            if success:
                self.log(f"✓ {self.i18n.t('conversion_complete')}\n")
                msg = f"{self.i18n.t('conversion_success')}\n\n{output_file}"
                if warnings:
                    msg += "\n\n" + "\n".join(warnings)
                messagebox.showinfo(self.i18n.t("success"), msg)
            else:
                self.log(f"✗ {self.i18n.t('conversion_failed')}\n")
                messagebox.showerror(self.i18n.t("error"), self.i18n.t("conversion_failed"))
        
        except Exception as e:
            error_details = traceback.format_exc()
            self.log(f"✗ {self.i18n.t('error_occurred')}: {str(e)}\n")
            self.log("\n" + error_details + "\n")
            messagebox.showerror(self.i18n.t("error"), f"{self.i18n.t('error_occurred')}:\n{str(e)}")



def main():
    """Funzione principale"""
    import sys
    import os
    import platform
    
    # Fix per PyInstaller: configura il percorso di tkdnd
    if getattr(sys, 'frozen', False):
        # Siamo in un eseguibile PyInstaller
        import tkinterdnd2
        tkdnd_dir = os.path.join(sys._MEIPASS, 'tkdnd')
        
        # Determina la sottocartella in base al sistema operativo
        system = platform.system()
        if system == 'Windows':
            tkdnd_subdir = 'win64'
        elif system == 'Linux':
            tkdnd_subdir = 'linux64'
        elif system == 'Darwin':  # macOS
            tkdnd_subdir = 'osx64'
        else:
            tkdnd_subdir = 'win64'  # fallback
        
        # Sovrascrivi il percorso del modulo tkinterdnd2
        original_init = tkinterdnd2.TkinterDnD.Tk.__init__
        
        def patched_init(self, *args, **kwargs):
            # Chiama il costruttore della classe base (tk.Tk)
            tk.Tk.__init__(self, *args, **kwargs)
            
            # Carica tkdnd manualmente con il percorso corretto
            module_path = os.path.join(tkdnd_dir, tkdnd_subdir)
            self.tk.call('lappend', 'auto_path', module_path)
            try:
                self.tk.call('package', 'require', 'tkdnd')
            except tk.TclError:
                raise RuntimeError(f'Unable to load tkdnd library from {module_path}')
        
        tkinterdnd2.TkinterDnD.Tk.__init__ = patched_init
    
    root = TkinterDnD.Tk()
    app = YAMLExcelConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
