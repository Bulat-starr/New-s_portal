from datetime import datetime
class filters:
    language: str = "ru"
    sort_by: str = "popularity"
    key_words: str = ""
    date_from: str = datetime.now()

    def __init__(self, date=None, key_words=None, sort_by=None, lang=None):
        self.date = date
        self.key_words = key_words # "first_second_"
        self.sort_by = sort_by
        self.language = lang

    @staticmethod
    def getKeywords(self):
        result = ""
        generated_array = self.key_words.split('_')
        for word in generated_array:
            result+=word + "+OR+"
        return "q=" + result[:5]

    @staticmethod
    def setKeywords(self, key_words):
        self.key_words = key_words

    @staticmethod
    def setLanguage(self, lang):
        self.language = lang



