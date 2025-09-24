import requests
from datetime import datetime, timedelta


def parseNews():
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': 'Apple OR Russia',
        'from': yesterday,
        'sortBy': 'popularity',
        'apiKey': '0b326a5b562141fa811e5732d1303bca'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"Найдено статей: {data['totalResults']}")
        for article in data['articles'][:5]:
            print(f"Заголовок: {article['title']}")
    else:
        print(f"Ошибка: {response.status_code}")


if __name__ == '__main__':
    parseNews()