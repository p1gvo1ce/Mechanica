@echo off
title GRITANA :: Пробуждение

REM === Перейти в корень проекта
cd /d "%~dp0"

REM === Запуск бэкенда
echo Запуск бэкенда...
start "" .venv\Scripts\python.exe -m uvicorn gritana.backend.main:app --reload --port 8000

REM === Подождать чуть-чуть, чтобы бэкенд не охуел от нагрузки
timeout /t 2 >nul

REM === Запуск фронтенда
echo Запуск фронтенда...
cd gritana\frontend\gritana-ui
start "" npm run dev

REM === Открытие браузера
timeout /t 1 >nul
start http://localhost:5173
