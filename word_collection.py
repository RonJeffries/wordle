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

    @classmethod
    def from_strings(cls, *strings):
        words = [Word(string) for string in strings]
        return cls(words)

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

    def eliminate(self, string):
        new_words = [word for word in self.words if word.contains_none(string)]
        return WordCollection(new_words)

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

    def trim(self, count):
        self.words = self.words[0:count]

    def __len__(self):
        return len(self.words)
