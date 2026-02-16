@echo off
setlocal enabledelayedexpansion
REM ========================================
REM  YAML Excel Converter - Build Script
REM  Versione Ottimizzata: 11.5 MB
REM ========================================
echo ========================================
echo  YAML Excel Converter - Build Script
echo  Versione Ottimizzata
echo ========================================
echo.

echo [1/4] Attivazione virtual environment...
call ..\.venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRORE: Virtual environment non trovato!
    echo Creare con: python -m venv .venv
    pause
    exit /b 1
)

echo.
echo [2/4] Pulizia build precedenti...
if exist ..\build (
    rmdir /s /q ..\build
    echo   - Rimossa cartella build
)
if exist ..\dist (
    rmdir /s /q ..\dist
    echo   - Rimossa cartella dist
)

echo.
echo [3/4] Creazione eseguibile ottimizzato...
echo   - Escluse dipendenze: pandas, numpy (25+ MB risparmiati)
echo   - Solo formato custom secrets.rlist
pyinstaller build_exe.spec --clean --distpath=..\dist --workpath=..\build\build_exe
if errorlevel 1 (
    echo.
    echo ERRORE durante la compilazione!
    pause
    exit /b 1
)

echo.
echo [4/4] Verifica build...
if exist ..\dist\YAMLExcelConverter.exe (
    echo.
    echo ========================================
    echo BUILD COMPLETATO CON SUCCESSO!
    echo ========================================
    echo Eseguibile: ..\dist\YAMLExcelConverter.exe
    echo.
    
    REM Calcola dimensione file in MB
    for %%F in (..\dist\YAMLExcelConverter.exe) do (
        set fileSize=%%~zF
    )
    
    REM Converti byte in MB usando PowerShell
    for /f %%i in ('powershell -NoProfile -Command "[math]::Round(!fileSize!/1MB, 2)"') do set sizeMB=%%i
    
    echo Dimensione: !sizeMB! MB
    echo.
    echo Caratteristiche:
    echo   - Formato: secrets.rlist ^(custom^)
    echo   - GPG: Supporto encrypt/decrypt
    echo   - Drag ^& Drop: Abilitato
    echo   - Dimensione ottimizzata: -69%%
    echo ========================================
) else (
    echo.
    echo ========================================
    echo ERRORE: Build fallito!
    echo ========================================
    echo L'eseguibile non e' stato creato.
    echo Controlla i messaggi di errore sopra.
    echo ========================================
)
echo.

pause
