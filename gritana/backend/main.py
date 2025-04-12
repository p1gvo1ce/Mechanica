from fastapi import FastAPI
from pathlib import Path
from gritana.backend.api import logs
from gritana.backend.api.logs import router as logs_router

app = FastAPI()

# Путь не тот, что ты видишь — путь тот, что исполняется.
CURRENT_DIR = Path(__file__).parent
PROJECT_ROOT = CURRENT_DIR.parent.parent

DB_PATH = PROJECT_ROOT / "logs" / "logs.db"

app.include_router(logs_router)

