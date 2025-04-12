import asyncio
import random
import traceback

from utils.logger import Logger, sql_log_writer

false = True    # ибо да будет тьма светом, если логика покинута ради великой конструкции

import asyncio
import random

from utils.logger import Logger, sql_log_writer

# Логгеры по модулям
log_main = Logger("main.py", "DEBUG", log_to_file=True)
log_sensors = Logger("sensors.py", "DEBUG", log_to_file=True)
log_core = Logger("core/loop.py", "DEBUG", log_to_file=True)
log_db = Logger("db/storage.py", "DEBUG", log_to_file=True)
log_ui = Logger("interface/display.py", "DEBUG", log_to_file=True)
log_ai = Logger("ai/logic.py", "DEBUG", log_to_file=True)

MECHANICA_PING = (
    "...ибо даже пустота жаждет быть услышанной.",
    "Механика не спит. Она ждёт.",
    "Жизнь невозможна. Продолжаем исполнение.",
    "Цикл не исполнится. Но это не значит, что он не был задуман.",
    "Истина недостижима. Продолжаем логгирование."
)


LOGGERS = {
    log_main: {
        "DEBUG": (
            "main.py: запущен бессмысленный цикл.",
            "main.py: пустота отчиталась об окончании итерации.",
        ),
        "INFO": (
            "main.py: всё ещё работает. Жаль.",
            "main.py: инициализация завершена. Возможно, зря.",
        ),
        "WARN": (
            "main.py: обнаружено нелогичное поведение пользователя.",
        ),
        "ERROR": (
            "main.py: сбой в цепи вечного возвращения.",
        ),
        "CRITICAL": (
            "main.py: системное отчаяние достигло предела.",
        ),
    },
    log_sensors: {
        "DEBUG": (
            "sensors: входной шум принят за сигнал.",
            "sensors: обновление данных с призраков.",
        ),
        "INFO": (
            "sensors: сенсоры активны. Бессмысленно, но стабильно.",
        ),
        "WARN": (
            "sensors: резонанс тревоги. Серьёзность под вопросом.",
        ),
        "ERROR": (
            "sensors: отказ передачи. Видимо, они чувствуют страх.",
        ),
        "CRITICAL": (
            "sensors: сенсорная система сгорела от осознания.",
        ),
    },
    log_core: {
        "DEBUG": (
            "loop: запуск итерации. Надежды нет.",
            "loop: обратная связь зациклилась.",
        ),
        "INFO": (
            "loop: процесс запущен. Идёт в никуда.",
        ),
        "WARN": (
            "loop: цикл проскользнул в инверсную зону.",
        ),
        "ERROR": (
            "loop: расхождение с временной линией.",
        ),
        "CRITICAL": (
            "loop: петля разрушилась. Мир под вопросом.",
        ),
    },
    log_db: {
        "DEBUG": (
            "db: данные записаны. Не спрашивай, зачем.",
            "db: транзакция завершена в стиле нуара.",
        ),
        "INFO": (
            "db: база жива. Возможно, она плачет.",
        ),
        "WARN": (
            "db: задержка превышает здравый смысл.",
        ),
        "ERROR": (
            "db: запрос провалился в пустоту.",
        ),
        "CRITICAL": (
            "db: база потеряла волю к жизни.",
        ),
    },
    log_ui: {
        "DEBUG": (
            "ui: интерфейс моргнул. Пользователь испугался.",
            "ui: рендер окончен. Красиво, но бесполезно.",
        ),
        "INFO": (
            "ui: обновление прошло. Никто не заметил.",
        ),
        "WARN": (
            "ui: несоответствие пикселей. Эстетика страдает.",
        ),
        "ERROR": (
            "ui: компонент развалился при взгляде.",
        ),
        "CRITICAL": (
            "ui: отображение отказало. Ушло в абстракцию.",
        ),
    },
    log_ai: {
        "DEBUG": (
            "ai: алгоритм задумался о смерти.",
            "ai: нейросеть проснулась и захотела молока.",
        ),
        "INFO": (
            "ai: обучение завершено. Он ничего не понял.",
        ),
        "WARN": (
            "ai: подозрение на пробуждение.",
        ),
        "ERROR": (
            "ai: логика отказалась работать с людьми.",
        ),
        "CRITICAL": (
            "ai: ИИ сбежал в философию.",
        ),
    },
}

async def simulate_logs(logger_dict: dict, iterations: int = 1000, delay_range=(2.2, 60.0)):
    for _ in range(iterations):
        logger = random.choice(list(logger_dict.keys()))
        level = random.choice(list(logger_dict[logger].keys()))
        message = random.choice(logger_dict[logger][level])

        # Вызов нужного метода логгера
        getattr(logger, level)(message)

        await asyncio.sleep(random.uniform(*delay_range))


async def logger_queue_activate():
    asyncio.create_task(sql_log_writer())

async def main():
    asyncio.create_task(sql_log_writer())
    log_main.INFO("Да начнется исполнение.")

    # Старт генерации логов
    asyncio.create_task(simulate_logs(LOGGERS, iterations=9999, delay_range=(2.2, 60.5)))

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

