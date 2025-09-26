from API_news_parse import parseNews
from models.API_filters import filters

if __name__ == '__main__':
    flt = filters()
    flt.setKeywords(flt, ["Russia", "economic"])
    flt.setSortBy(flt, "popularity")
    flt.setUrl(flt, "everything")
    flt.setLanguage(flt, "en")
    for art in parseNews(flt):
        print(art.getTitle())
        print(art.getText())
        print(art.getUrl())
        print(art.getAuthor())
