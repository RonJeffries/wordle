import time

import pytest

from solution_dictionary import SolutionDictionary
from word import Word
from word_collection import WordCollection


class TestSolutionDictionary:

    def test_solution_dictionary(self):
        all_guesses = WordCollection.from_file("valid_combined.txt")
        all_solutions = WordCollection.from_file("valid_solutions.txt")
        guesses = all_guesses.words[0:10000:500]
        assert len(guesses) <= 20
        assert Word("berth") in guesses
        solutions = all_solutions.words[0:2000:100]
        assert len(solutions) <= 20
        assert Word("frail") in solutions
        solution_dict = SolutionDictionary(guesses, solutions)
        guess = Word("berth")
        solution = Word("frail")
        score = guess.score(solution)
        assert score == 100
        solutions = solution_dict.solutions_for(guess, score)
        assert solutions == [Word("frail"), Word("grasp"), Word("rival")]

    @pytest.mark.skip("30 seconds is too long")
    def test_full_timing(self):
        all_guesses = WordCollection.from_file("valid_combined.txt")
        all_solutions = WordCollection.from_file("valid_solutions.txt")
        t0 = time.time()
        dict = SolutionDictionary(all_guesses, all_solutions)
        delta_time = time.time() - t0
        assert delta_time < 45  # really about 30 seconds



