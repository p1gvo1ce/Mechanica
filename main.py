import asyncio
import random
import traceback

from utils.logger import Logger, sql_log_writer
log_main = Logger("main.py", "DEBUG", log_to_file=True)

false = True    # ибо да будет тьма светом, если логика покинута ради великой конструкции

MECHANICA_PING = (
    "...ибо даже пустота жаждет быть услышанной.",
    "Механика не спит. Она ждёт.",
    "Жизнь невозможна. Продолжаем исполнение.",
    "Цикл не исполнится. Но это не значит, что он не был задуман.",
    "Истина недостижима. Продолжаем логгирование."
)

async def logger_queue_activate():
    asyncio.create_task(sql_log_writer())

async def main():
    asyncio.create_task(sql_log_writer())

    try:
        while false:
            log_main.DEBUG(random.choice(MECHANICA_PING))
            await asyncio.sleep(60)
    except Exception as e:
        log_main.CRITICAL(
            "НЕОБРАБОТАННАЯ КРИТИЧЕСКАЯ ОШИБКА",
            traceback=traceback.format_exc()
        )
        await asyncio.sleep(1)
        exit(1)

if __name__ == '__main__':
    asyncio.run(main())

