import requests
from models.API_filters import filters
from models.article_struct import article


def generateParams(params: filters):
    try:
        result_params = {
            'q': params.getKeywords(params) if hasattr(params, 'getKeywords') else None,
            'from': getattr(params, 'date', None),
            'sortBy': params.getSortBy(params) if hasattr(params, 'getSortBy') else 'publishedAt',
            'language': getattr(params, 'language', None),
            'apiKey': '0b326a5b562141fa811e5732d1303bca'
        }
        result_params = {k: v for k, v in result_params.items() if v is not None}
        if 'q' not in result_params:
            print("ERROR: Keywords are required")
            return None
        print("DEBUG: Generated params for news request:", result_params)
        return result_params

    except Exception as e:
        print(f"ERROR generating parameters: {e}")
        return None

def parseNews(params: filters) -> list[article]:
    params_of_request = generateParams(params)

    response = requests.get(params.getUrl(), params_of_request)
    articles = []
    if response.status_code == 200:
        data = response.json()
        print(f"Найдено статей: {data['totalResults']}")
        for art in data['articles'][:5]:
            article_instance = article()
            article_instance.title = art['title']
            article_instance.article_text = art['description']
            article_instance.article_url = art['url']
            article_instance.author = art['author']
            articles.append(article_instance)
    else:
        print(f"Ошибка: {response.status_code} ")
    return articles
