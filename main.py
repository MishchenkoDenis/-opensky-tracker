import requests

url = 'https://opensky-network.org/api/states/all'
response = requests.get(url)

if response.status_code == 200:
    print("Response: 200")
    data = response.json()
    
    aircrafts = data['states']
    
    count_aircrafts = len(aircrafts)
    print(f"Всего самолётов: {count_aircrafts}")

    countries = []
    for plane in aircrafts:
        # plane — это страна согласно документации OpenSky API
        country_name = plane
        if country_name:  # проверка, чтобы не добавить пустые значения
            countries.append(country_name)

    unique_countries = set(countries)
    print(f"Уникальных стран: {len(unique_countries)}")

    counts_country = {}
    for c in countries:
        counts_country[c] = counts_country.get(c, 0) + 1
    
    top5 = sorted(counts_country.items(), key=lambda item: item, reverse=True)[:5]
    
    top5_names = []
    for item in top5:
        top5_names.append(item)

    print("Топ 5 стран:", top5_names)
else:
    print(f"Ошибка запроса: {response.status_code}")
