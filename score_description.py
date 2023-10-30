from word import Word
from word_collection import WordCollection


class ScoreDescription:
    def __init__(self, score, words=None):
        self.score = score
        if words:
            self.words = words
        else:
            self.words = WordCollection()

    @classmethod
    def from_strings(cls, score, *strings):
        words = WordCollection.from_strings(*strings)
        return cls(score, words)

    def add_word(self, word: Word):
        self.words.append(word)

    def __eq__(self, other):
        return self.score == other.score and self._matches(other)

    def __iter__(self):
        return iter(self.words)

    def __len__(self):
        return len(self.words)

    def _matches(self, other):
        my_words = set(self.words.words)
        his_words = set(other.words.words)
        return my_words == his_words
