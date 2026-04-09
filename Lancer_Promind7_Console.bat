@echo off
REM Lanceur avec fenêtre (debug). Pour sans terminal : double-clic sur Lancer_Promind7_Console.vbs

cd /d "%~dp0"

set "PROMIND7_STAGE_EMPLOI_SCRIPT_ROOT=D:\01-ProM7-consulting\01-Promind7\02-Contenus\01-Scripts\Parcours stage & emploi"

IF EXIST ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
) ELSE (
    echo Avertissement : .venv introuvable, utilisation du Python du PATH.
)

echo Lancement Promind7 Console...
python -m streamlit run promind7_console.py

pause
