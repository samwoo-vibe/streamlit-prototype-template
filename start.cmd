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
if not exist .env (
  echo [안내] .env가 없어 .env.example에서 만듭니다. 로컬은 SQLite를 사용합니다.
  copy /y .env.example .env >nul
)
uv sync
if errorlevel 1 (
  echo [오류] 개발 환경 준비에 실패했습니다.
  pause
  exit /b 1
)

uv run alembic upgrade head
if errorlevel 1 (
  echo [오류] 로컬 데이터베이스 준비에 실패했습니다.
  pause
  exit /b 1
)

rem Local development may show tracebacks; the deployed container keeps the
rem secure config.toml default and does not pass this override.
uv run streamlit run app.py --client.showErrorDetails=full
if errorlevel 1 pause
