import pytest


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
    #
    # def test_word_class_exists(self):
    #     word = Word("abate")
        