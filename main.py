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

    
