import logging

import pandas as pd
import requests

API_URL = "https://opensky-network.org/api/states/all"
OUTPUT_FILE = "te.xlsx"

logger = logging.getLogger("opensky")

def extract():
    logger.info("EXTRACT: отправляем запрос к OpenSky API")

    response = requests.get(API_URL, timeout=50)

    # Если API вернул ошибку HTTP — вызываем исключение
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, dict):
        raise ValueError("Некорректный формат ответа API")

    aircrafts = data.get("states")

    if not isinstance(aircrafts, list):
        raise ValueError("В ответе API отсутствует список states")

    if len(aircrafts) == 0:
        logger.warning("EXTRACT: API вернул пустой список самолётов")

    logger.info(
        "EXTRACT: получено %s самолётов",
        len(aircrafts)
    )

    return data

def transform(data):
    logger.info("TRANSFORM: начинаем обработку данных")

    aircrafts = data["states"]

    columns = [
        "код_icao24",
        "позывной",
        "страна_происхождения",
        "время_позиции",
        "последний_контакт",
        "долгота",
        "широта",
        "барометрическая_высота",
        "на_земле",
        "скорость",
        "истинный_курс",
        "вертикальная_скорость",
        "датчики",
        "геометрическая_высота",
        "код_ответчика",
        "spi_сигнал",
        "источник_позиции"
    ]

    df = pd.DataFrame(aircrafts, columns=columns)

    logger.info(
        "TRANSFORM: создан DataFrame из %s строк",
        len(df)
    )

    df["позывной"] = df["позывной"].str.strip()

    countries_count = df["страна_происхождения"].nunique()

    logger.info(
        "TRANSFORM: обнаружено %s уникальных стран",
        countries_count
    )

    flying_count = (df["на_земле"] == False).sum()

    logger.info(
        "TRANSFORM: самолётов в воздухе — %s",
        flying_count
    )

    missing_coordinates = df[
        ["широта", "долгота"]
    ].isna().any(axis=1).sum()

    if missing_coordinates > 0:
        logger.warning(
            "TRANSFORM: у %s самолётов отсутствуют координаты",
            missing_coordinates
        )

    logger.info("TRANSFORM: обработка завершена")

    return df

def load(df):
    logger.info("LOAD: начинаем сохранение данных")

    country_counts = df[
        "страна_происхождения"
    ].value_counts()

    country_counts.to_excel(
 
        OUTPUT_FILE,
        engine="openpyxl"
    )

    logger.info(
        "LOAD: данные сохранены в файл %s",
        OUTPUT_FILE
    )

    logger.info(
        "LOAD: сохранено %s стран",
        len(country_counts)
    )

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    logger.info("Запуск ETL из main.py")

    try:
        data = extract()
        df = transform(data)
        load(df)

    except Exception:
        logger.exception("Ошибка выполнения ETL")
        raise

    else:
        logger.info("ETL успешно завершён")
