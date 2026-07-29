@echo off
setlocal
cd /d "%~dp0"

where uv >nul 2>nul
if errorlevel 1 (
  echo [오류] uv가 설치되어 있지 않습니다.
  echo https://docs.astral.sh/uv/getting-started/installation/ 에서 uv를 설치하세요.
  pause
  exit /b 1
)

if not exist data mkdir data
uv sync
if errorlevel 1 (
  echo [오류] 개발 환경 준비에 실패했습니다.
  pause
  exit /b 1
)

uv run streamlit run app.py
if errorlevel 1 pause

