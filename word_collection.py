from collections import defaultdict

from word import Word


class WordCollection:
    @classmethod
    def from_file(cls, file_name):
        result = cls()
        with open(file_name, "r") as word_file:
            lines = word_file.read().splitlines()
            for word in lines:
                result.append(Word(word))
        return result

    def __init__(self, words=None):
        if words:
            self.words = words
        else:
            self.words = []

    def __iter__(self):
        return iter(self.words)

    def append(self, word):
        assert isinstance(word, Word)
        self.words.append(word)

    def append_unique(self, word_collection):
        return set(self.words + word_collection.words)

    def frequencies(self):
        def default_value():
            return 0
        freq = defaultdict(default_value)
        for word in self.words:
            for c in word.word:
                freq[c] += 1
        return freq

    def has_word(self, word):
        for my_word in self.words:
            if my_word.word == word.word:
                return True
        return False

    def __len__(self):
        return len(self.words)
