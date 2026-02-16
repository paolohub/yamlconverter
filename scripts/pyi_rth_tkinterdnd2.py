"""
PyInstaller runtime hook per tkinterdnd2.
Configura il percorso della libreria tkdnd per l'eseguibile pacchettizzato.
"""
import sys
import os

# Quando l'app è pacchettizzata con PyInstaller, sys._MEIPASS contiene
# il percorso temporaneo dove vengono estratti i file
if hasattr(sys, '_MEIPASS'):
    # Imposta la variabile d'ambiente TCL_LIBRARY se non è già impostata
    tkdnd_dir = os.path.join(sys._MEIPASS, 'tkdnd')
    if os.path.exists(tkdnd_dir):
        os.environ['TKDND_LIBRARY'] = tkdnd_dir
