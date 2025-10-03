from datetime import datetime
from .check_validation import checkDataLangValidation, checkDataSortByValidation


class filters:
    __language: str = "ru"  # 'ru' or 'en'
    __sort_by: str = "popularity"  # 'popularity' or 'publishedAt' or 'relevancy'
    __key_words: str = ""  # Array of string
    __date_from: str = datetime.now()
    __url_type: str = ""  # 'topHeadlines' or 'everything'

    def __init__(self, date=None, key_words=None, sort_by=None, lang=None):
        self.date = date
        self.key_words = key_words  # "first_second_"
        self.sort_by = sort_by
        self.language = lang

    def getUrl(self):
        return self.__url_type

    def setUrlTopHeadlines(self):
        self.__url_type = "https://newsapi.org/v2/top-headlines"

    def setUrlEverything(self):
        self.__url_type = 'https://newsapi.org/v2/everything'

    @staticmethod
    def setUrl(self, key):
        if key == "topHeadlines":
            self.setUrlTopHeadlines()
        elif key == "everything":
            self.setUrlEverything()

    @staticmethod
    def getKeywords(self):
        return self.key_words

    @staticmethod
    def setKeywords(self, key_words):  # This method should get array of words
        str = ""
        for word in key_words:
            str += word + "+OR+"
        self.key_words = str[0:-4]

    @staticmethod
    def getSortBy(self):
        return self.sort_by

    @staticmethod
    def setSortBy(self, sort_by):
        if checkDataSortByValidation(sort_by):
            self.sort_by = sort_by
        else:
            print("Validation sortBy error")

    @staticmethod
    def getLanguage(self, lang):
        return self.language

    @staticmethod
    def setLanguage(self, lang):
        if checkDataLangValidation(lang):
            self.language = lang
        else:
            print("Validation lang error")
