import requests

url = 'https://opensky-network.org/api/states/all'
response = requests.get(url)

if response.status_code == 200:
    print("Response: 200")
    data = response.json()
    a = data['states']
    lenght = len(a)
    country = []
    for i in a:
        country.append(i[2]) # top5 стран в воздухе
    country_uniqon = set(country)
    print(len(country_uniqon))

    counts_contry = {}
    for i in country:
        counts_contry[i] = counts_contry.get(i, 0) + 1
    top5 = sorted(counts_contry.items(), key=lambda item:item[1], reverse=True)[:5]
    b = []
    for i in top5:
        b.append(i[0])

    print(b)