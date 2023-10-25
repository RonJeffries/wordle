import pytest

from collections import defaultdict

class Word:
    def __init__(self, word):
        self.word = word

    def __iter__(self):
        return iter(self.word)


class WordCollection:
    @classmethod
    def from_file(cls, file_name):
        result = cls()
        with open(file_name, "r") as word_file:
            lines = word_file.readlines()
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


class TestWords:
    def test_hookup(self):
        assert 2 + 2 == 4

    def test_reading_guesses(self):
        with open("valid_guesses.txt", "r") as guesses:
            lines = guesses.readlines()
        assert len(lines) == 10657

    def test_reading_solutions(self):
        with open("valid_solutions.txt", "r") as solutions:
            lines = solutions.readlines()
        assert len(lines) == 2315

    def test_word_class_exists(self):
        word = Word("abate")

    def test_drive_word_collection(self):
        w1 = Word("avast")
        w2 = Word("matey")
        words = WordCollection()
        words.append(w1)
        words.append(w2)
        assert len(words) == 2

    def test_frequency(self):
        from collections import defaultdict
        def default_value():
            return 0
        freq = defaultdict(default_value)
        letters = "aaaabbbccd"
        for c in letters:
            freq[c] += 1
        assert freq["a"] == 4
        assert freq["d"] == 1

    def test_words_from_file(self):
        wc = WordCollection.from_file("valid_solutions.txt")
        freq = wc.frequencies()
        assert freq["e"] == 1233

    def test_known_frequencies(self):
        wc = WordCollection()
        for string in ["aaaabbb", "aacc"]:
            wc.append(Word(string))
        freq = wc.frequencies()
        assert freq["a"] == 6
        assert freq["b"] == 3
        assert freq["c"] == 2
