@echo off
title IREF - Indice de Resoluciones Estudiantiles FIUBA

cd /d "%~dp0"

echo.
echo =====================================
echo      Iniciando IREF...
echo =====================================
echo.

start http://localhost:8501

streamlit run app.py

pause