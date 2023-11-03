import pytest

from solution_dictionary import GuessDescription
from word import Word
from word_collection import WordCollection


class TestInformation:

    def test_first_info(self):
        all_solutions = WordCollection.from_file("valid_solutions.txt")
        word = Word("abate")
        gd = GuessDescription(word, all_solutions)
        keys = gd.score_descriptions.keys()
        print(22000, gd.score_descriptions[22000])
        assert len(keys) == 84  # just because it is.
        total_words = sum(len(sd.words) for sd in gd.score_descriptions.values())
        assert total_words == 2315
        expected_info = gd.expected_information()
        assert expected_info == pytest.approx(4.63, abs=0.05)

    def test_known_values(self):
        solutions = WordCollection.from_strings("azzzz", "zbzzz", "zzczz", "zzzdz")
        guess = Word("dcbay")
        gd = GuessDescription(guess, solutions)
        keys = set(gd.score_descriptions.keys())
        expected = {10, 100, 1000, 10000}
        assert keys == expected
        info = gd.expected_information()
        assert info == 2


