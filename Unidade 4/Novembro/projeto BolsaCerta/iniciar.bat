@echo off
chcp 65001 >nul
cd /d "%~dp0"
title BolsaCerta - nao feche esta janela enquanto usa o chat
echo Iniciando o BolsaCerta... o navegador vai abrir em http://localhost:8000
echo Para parar, feche esta janela ou aperte Ctrl+C.
echo.
where py >nul 2>nul && (py web.py) || (python web.py)
if errorlevel 1 (
  echo.
  echo Nao foi possivel iniciar. Verifique se o Python 3.10+ esta instalado: https://www.python.org/downloads/
)
pause
