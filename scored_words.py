from word import Word
from word_collection import WordCollection


class ScoredWords:
    def __init__(self, score):
        self.score = score
        self.words = WordCollection()

    def add_word(self, word: Word):
        self.words.append(word)
