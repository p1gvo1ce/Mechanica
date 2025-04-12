import aiosqlite
import datetime
import asyncio
import time
from fastapi import FastAPI, Query
from typing import List, Optional
from pathlib import Path
import re
import datetime

app = FastAPI()

# Путь не тот, что ты видишь — путь тот, что исполняется.
CURRENT_DIR = Path(__file__).parent
PROJECT_ROOT = CURRENT_DIR.parent.parent

DB_PATH = PROJECT_ROOT / "logs" / "logs.db"

def parse_dsl(dsl_string: str):
    """
    Превращает строку-заклинание в SQL-запрос, понятный машине.

    🕯 Поддерживаемые обряды:
        - AND / OR / NOT — логические связки для построения цепей проклятий
        - level, module, message, timestamp — допустимые поля вызова
        - message — интерпретируется как регулярное выражение, ибо текст — это тень смысла
        - timestamp — принимает знаки: >, <, >=, <=, ибо время — не линейно, но поддаётся сравнению

    📜 Примеры DSL-заклинаний:
        level:ERROR AND message:"fail.*int"
        NOT module:ai/logic.py AND timestamp:>2025-04-01T00:00:00

    Возвращает:
        - where_clause (str) — часть SQL-запроса для обряда фильтрации
        - params (list) — переменные для подстановки, дабы не тревожить богов инъекциями

    Внимание:
        - Не поддерживает вложенные скобки. Демоны пока боятся глубокой рекурсии.
        - Ошибочные выражения будут проигнорированы без предупреждения. Таков наш путь.
    """

    dsl_string = dsl_string.replace("&&", "AND")
    dsl_string = dsl_string.replace("||", "OR")

    tokens = re.split(r'\s+(AND|OR|NOT)\s+', dsl_string.strip())
    sql_parts = []
    params = []
    message_regex = None

    for token in tokens:
        token = token.strip()
        if token in {"AND", "OR", "NOT"}:
            sql_parts.append(token)
            continue

        match = re.match(r'(\w+):([<>]=?|=)?(.*)', token)
        if not match:
            continue

        field, op, value = match.groups()
        field = field.strip()
        op = op.strip() if op else '='
        value = value.strip().strip('"')

        if field == "timestamp":
            try:
                dt = datetime.datetime.fromisoformat(value)
                timestamp = int(dt.timestamp() * 1000)
                sql_parts.append(f"timestamp {op} ?")
                params.append(timestamp)
            except ValueError:
                continue

        elif field == "message":
            # Мы не фильтруем message в SQL, а передаём его как regex
            message_regex = value
            continue

        elif field in {"level", "module"}:
            sql_parts.append(f"{field} {op} ?")
            params.append(value)

    where_clause = " ".join(sql_parts)
    return where_clause, params, message_regex




@app.get("/logs")
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

@app.get("/levels")
async def get_levels():
    return ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]

@app.get("/modules")
async def get_modules():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        curor = await db.execute("SELECT DISTINCT module FROM logs ORDER BY module")
        rows = await curor.fetchall()
        return [row["module"] for row in rows]

@app.get("/stats")
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

@app.get("/logs/dsl")
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

    # Если есть message_regex, отфильтровываем
    if message_regex is not None:
        pattern = re.compile(message_regex)
        filtered = [dict(r) for r in rows if pattern.search(r["message"] or "")]
        return filtered
    else:
        return [dict(r) for r in rows]
