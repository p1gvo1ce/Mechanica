import os
import asyncio
from asyncio import create_task
from datetime import datetime, timezone
import aiosqlite


async def init_db():
    """
    Функция созда1т базу каталоги logs/debug и базу данных по адресу logs/log.db
    :return: None
    """
    SQL_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS logs (
    id              INTEGER     PRIMARY KEY AUTOINCREMENT,
    timestamp       INTEGER     NOT NULL,
    level           TEXT        NOT NULL,
    module          TEXT        NOT NULL,
    message         TEXT        NOT NULL,
    traceback       TEXT
);
"""


    os.makedirs("logs/debug", exist_ok=True)
    async with aiosqlite.connect("logs/logs.db") as db:
        await db.execute(SQL_CREATE_TABLE)
        await db.commit()

async def write_log_to_db(time=None, level="none", module="none", message="none", traceback=None):
    """

    :param time: время логируемого события
    :param level: уровень логирования DEBUG, INFO, WARN, ERROR, CRITICAL
    :param module:  Название модуля выводящего логи
    :param message: Сообщение лога
    :param traceback: Трассировка ошибки
    :return: None
    """
    if time == None:
        time = datetime.now(tz=timezone.utc)
    timestamp = int(time.timestamp() * 1000)

    SQL_WRITE_LOG = """
    INSERT INTO logs    (timestamp, level, module, message, traceback)
    VALUES              (?, ?, ?, ?, ?)
    """

    async with aiosqlite.connect("logs/logs.db") as db:
        await db.execute(
            SQL_WRITE_LOG,
            (
                timestamp,
                level,
                module,
                message,
                traceback
            )
        )
        await db.commit()

log_queue = asyncio.Queue()         # создаём буфер логов

async def sql_log_writer():
    while True:
        log = await log_queue.get()
        await write_log_to_db(**log)

async def enqueue_log_entry(time=None, level="none", module="none", message="none", traceback=None):
    await log_queue.put(
            {
                "time": time,
                "level": level,
                "module": module,
                "message": message,
                "traceback": traceback
            }
        )


class Logger():

    LEVELS = {
            "CRITICAL": 0,
            "ERROR": 1,
            "WARN": 2,
            "INFO": 3,
            "DEBUG": 4
        }

    def __init__(self, module_name, log_level="ERROR", log_to_file = False):
        '''
        Класс логирования.
        :param module_name: Название модуля выводящего логи
        :param log_level: уровень логирования DEBUG, INFO, WARN, ERROR, CRITICAL
        '''
        self.module_name = module_name
        self.log_level = self.get_int_level(log_level)
        self.log_to_file = log_to_file

    def get_int_level(self, str_level):
        """
        :param str_level: уровень логирования DEBUG, INFO, WARN, ERROR, CRITICAL
        :return: уровень 0 - 4, где 0 - CRITICAL, 4 - DEBUG
        """
        return self.LEVELS.get(str_level.upper())

    def DEBUG(self, message):
        self.log(message, "DEBUG", color=33)

    def INFO(self, message):
        self.log(message, "INFO", color=34)

    def WARN(self, message):
        self.log(message, "WARN", color=36)

    def ERROR(self, message, traceback=None):
        self.log(message, "ERROR", traceback, color=31)

    def CRITICAL(self, message, traceback=None):
        self.log(message, "CRITICAL", traceback, color=31)

    def EXCEPTION(self, message: str, exc: Exception):
        import traceback as tb

        full_message = f"{message}\n→{str(exc)}"
        self.ERROR(message=full_message, traceback=tb.format_exc())

    def log(self, message="NO LOG MESSAGE", mess_level_in=1, traceback=None, color=31, style=5):
        """

        :param message: сообщение лога
        :param level: уровень запрошенного вывода лога
        :return: ничего
        """
        mess_level = self.get_int_level(mess_level_in)
        log_time = datetime.now(tz=timezone.utc)
        time_frame = log_time.strftime("[%Y.%m.%d %H:%M:%S:%f]")
        log_message = f"[{mess_level_in}] {time_frame} ({self.module_name}) - {message}"

        if self.log_level >= mess_level:
            print(
                f'\033[{style};{color}m{log_message}\033[m'
            )

        if self.log_to_file:
            with open(f"logs/debug/{self.module_name}.log", "a", encoding="utf-8") as f:
                f.write(log_message+"\n")
                if traceback:
                    f.write(traceback+"\n")

        try:
            asyncio.get_running_loop().create_task(
                enqueue_log_entry(log_time, mess_level_in, self.module_name, message, traceback)
            )
        except RuntimeError:
            import threading
            threading.Thread(target=lambda: asyncio.run(
                enqueue_log_entry(log_time, mess_level_in, self.module_name, message, traceback)
            ), daemon=True).start()

asyncio.run(init_db())