from collections import defaultdict

from word import Word


class WordCollection:
    @classmethod
    def from_file(cls, file_name):
        result = cls()
        with open(file_name, "r") as word_file:
            lines = word_file.read().splitlines()
            for word in (Word(line) for line in lines):
                result.append(Word(word))
        return result

    def __init__(self):
            self.words = []

    def append(self, word):
        self.words.append(word)

    def frequencies(self):
        def default_value():
            return 0
        freq = defaultdict(default_value)
        for word in self.words:
            for c in word.word:
                freq[c] += 1
        return freq

    def __len__(self):
        return len(self.words)
