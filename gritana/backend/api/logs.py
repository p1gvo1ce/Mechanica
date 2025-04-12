from typing import List, Optional
from fastapi import APIRouter, Query
import aiosqlite, re, time
from pathlib import Path
from gritana.backend.services.dsl_parser import parse_dsl

router = APIRouter(prefix="/ritual/logs", tags=["ritual"])

# Путь не тот, что ты видишь — путь тот, что исполняется.
CURRENT_DIR = Path(__file__).parent
PROJECT_ROOT = CURRENT_DIR.parent.parent.parent

DB_PATH = PROJECT_ROOT / "logs" / "logs.db"
print(DB_PATH)

@router.get("/")
async def get_logs(
        level: Optional[str] = None,
        module: Optional[str] = None,
        limit: int = 100
):
    print("→ Начало запроса", time.time())
    query = "SELECT * FROM logs WHERE 1=1"
    params = []

    if level:
        query += " AND level = ?"
        params.append(level)

    if module:
        query += " AND module = ?"
        params.append(module)

    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)

    print("→ Перед подключением к БД", time.time())
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        print("→ Подключён. Выполняю запрос...", time.time())
        cursor = await db.execute(query, params)
        logs = await cursor.fetchall()
        print("→ Запрос завершён", time.time())

    return [dict(row) for row in logs]

@router.get("/levels")
async def get_levels():
    return ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]

@router.get("/modules")
async def get_modules():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        curor = await db.execute("SELECT DISTINCT module FROM logs ORDER BY module")
        rows = await curor.fetchall()
        return [row["module"] for row in rows]

@router.get("/stats")
async def get_stats():
    query = """
    SELECT
        strftime('%Y-%m-%d %H:00', timestamp / 1000, 'unixepoch') as hour,
        COUNT(*) as count
    FROM logs
    GROUP BY hour
    ORDER BY hour DESC
    LIMIT 100
    """
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(query)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

@router.get("/dsl")
async def get_logs_dsl(q: str):
    where_clause, params, message_regex = parse_dsl(q)

    query = "SELECT * FROM logs"
    if where_clause:
        query += f" WHERE {where_clause}"
    query += " ORDER BY timestamp DESC LIMIT 100"

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()

    # Если есть message_regex, да будут забыты еретические логи
    if message_regex is not None:
        pattern = re.compile(message_regex)
        filtered = [dict(r) for r in rows if pattern.search(r["message"] or "")]
        return filtered
    else:
        return [dict(r) for r in rows]