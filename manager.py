import logging
import time
from pathlib import Path

from main import extract, transform, load

INTERVAL = 60  

# Создаём папку для логов
Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("logs/etl.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("opensky")


def pipeline():
    logger.info("ETL START")

    start_time = time.perf_counter()

    try:
        logger.info("EXTRACT: получение данных")
        data = extract()

        if not isinstance(data, dict) or not isinstance(data.get("states"), list):
            raise ValueError("EXTRACT: API не вернул корректный список states")

        logger.info(
            "EXTRACT: получено %s записей",
            len(data["states"])
        )

        logger.info("TRANSFORM: обработка данных")
        df = transform(data)

        if df is None:
            raise ValueError("TRANSFORM: функция вернула None")

        logger.info(
            "TRANSFORM: обработано %s строк",
            len(df)
        )

        logger.info("LOAD: сохранение данных")
        load(df)

        logger.info("LOAD: операция завершена")

    except Exception:
        logger.exception("ETL FAILED")
        return False

    else:
        duration = time.perf_counter() - start_time

        logger.info(
            "ETL SUCCESS | Время выполнения: %.2f сек.",
            duration
        )

        return True

    finally:
        logger.info("ETL END")


def scheduler():
    logger.info("Scheduler запущен")
    logger.info("Интервал: %s секунд", INTERVAL)

    run_number = 0

    while True:
        run_number += 1

        logger.info("Запуск ETL №%s", run_number)

        pipeline()

        logger.info(
            "Следующий запуск через %s секунд",
            INTERVAL
        )

        time.sleep(INTERVAL)


if __name__ == "__main__":
    try:
        scheduler()

    except KeyboardInterrupt:
        logger.info("Scheduler остановлен пользователем")
