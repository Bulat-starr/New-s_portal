from API_news_parse import parseNews
from models.API_filters import filters

if __name__ == '__main__':
    flt = filters()
    flt.setKeywords(flt, ["Russia"])
    flt.setSortBy(flt, "popularity")
    flt.setUrl(flt, "everything")
    flt.setLanguage(flt, "en")
    number_of_news = 5
    for art in parseNews(flt, number_of_news):
        print("Название: ")
        print(art.getTitle())
        print("Описание: ")
        print(art.getText())
        print("URL: ")
        print(art.getUrl())
        print("Содержание: ")
        print(art.getContent())
        print("Автор: ")
        print(art.getAuthor())
        print()



