import pytest


class Word:
    def __init__(self, word):
        self.word = word


class WordCollection:
    def __init__(self):
        self.words = []

    def append(self, word):
        self.words.append(word)

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
        