import requests
import pandas as pd

url = 'https://opensky-network.org/api/states/all'
response = requests.get(url, timeout=50)

if response.status_code == 200:
    # print("Response: 200")
    data = response.json()
    
    aircrafts = data['states']
    columns = [
    'код_icao24', 'позывной', 'страна_происхождения', 'время_позиции', 'последний_контакт',
    'долгота', 'широта', 'барометрическая_высота', 'на_земле', 'скорость',
    'истинный_курс', 'вертикальная_скорость', 'датчики', 'геометрическая_высота',
    'код_ответчика', 'spi_сигнал', 'источник_позиции']

    df = pd.DataFrame(aircrafts, columns=columns)
    print(df.head())
    counts_aitcrafts = len(df)

    a = df['страна_происхождения'].value_counts()
    # print(a.head(5))

    b = a.head(5) / len(df) * 100
    # print(b)

    sum_us= (df['страна_происхождения'] == 'United States').sum()
    # print(sum_us)
    print(df.info())

    df_2 = df[['время_позиции','долгота','широта','последний_контакт']]
    print(df_2.describe())

    air = (df['на_земле'] == False).sum()
    print(air)
    air_2 = df[df['на_земле'] == False]
    print(len(air_2))


#     count_aircrafts = len(aircrafts)
#     print(f"Всего самолётов: {count_aircrafts}")

#     countries = []
#     for plane in aircrafts:
#         # plane — это страна согласно документации OpenSky API
#         country_name = plane
#         if country_name:  # проверка, чтобы не добавить пустые значения
#             countries.append(country_name)

#     unique_countries = set(countries)
#     print(f"Уникальных стран: {len(unique_countries)}")

#     counts_country = {}
#     for c in countries:
#         counts_country[c] = counts_country.get(c, 0) + 1
    
#     top5 = sorted(counts_country.items(), key=lambda item: item, reverse=True)[:5]
    
#     top5_names = []
#     for item in top5:
#         top5_names.append(item)

#     print("Топ 5 стран:", top5_names)
# else:
#     print(f"Ошибка запроса: {response.status_code}")
