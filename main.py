import asyncio

from utils.logger import Logger, sql_log_writer
import traceback

main_logger = Logger("main log", "DEBUG", log_to_file=True)


async def logger_queue_activate():
    asyncio.create_task(sql_log_writer())

async def main():
    asyncio.create_task(sql_log_writer())

    try:
        int("Не число")
    except Exception as e:
        main_logger.CRITICAL(
            "НЕОБРАБОТАННАЯ КРИТИЧЕСКАЯ ОШИБКА",
            traceback=traceback.format_exc()
        )
        await asyncio.sleep(1)
        exit(1)

if __name__ == '__main__':
    asyncio.run(main())

