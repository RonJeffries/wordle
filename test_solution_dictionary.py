import time

import pytest

from score_description import ScoreDescription
from solution_dictionary import SolutionDictionary, Statistic
from word import Word
from word_collection import WordCollection


class TestSolutionDictionary:

    def test_solution_dictionary(self):
        all_guesses = WordCollection.from_file("valid_combined.txt")
        all_solutions = WordCollection.from_file("valid_solutions.txt")
        guesses = all_guesses[0:10000:500]
        assert isinstance(guesses, WordCollection)
        assert len(guesses) <= 20
        assert Word("berth") in guesses
        solutions = all_solutions[0:2000:100]
        assert len(solutions) <= 20
        assert Word("frail") in solutions
        solution_dict = SolutionDictionary(guesses, solutions)
        guess = Word("berth")
        solution = Word("frail")
        score = guess.score(solution)
        assert score == 100
        solutions = solution_dict.solutions_for(guess, score)
        expected = ScoreDescription.from_strings(score, "frail", "grasp", "rival")
        assert solutions == expected

    @pytest.mark.skip("30 seconds is too long")
    def test_full_timing(self):
        all_guesses = WordCollection.from_file("valid_combined.txt")
        all_solutions = WordCollection.from_file("valid_solutions.txt")
        t0 = time.time()
        dict = SolutionDictionary(all_guesses, all_solutions)
        delta_time = time.time() - t0
        print(delta_time)
        assert delta_time < 45  # really about 30 seconds
        assert False

    def test_easy_statistics(self):
        all_guesses = WordCollection.from_file("valid_combined.txt")
        guesses = all_guesses[0:10000:500]
        all_solutions = WordCollection.from_file("valid_solutions.txt")
        solutions = all_solutions[0:2000:100]
        sd = SolutionDictionary(guesses, solutions)
        stats = sd.create_statistics()
        print(Statistic.header)
        for stat in stats:
            print(stat)
        stat = stats[0]
        assert stat.number_of_buckets == 15
        assert stat.max_words == 3
        # assert False

    def test_drive_out_scored_words(self):
        scored = ScoreDescription(10101)
        assert scored.score == 10101
        assert not scored.words
        scored.add_word(Word("abcde"))
        scored.add_word(Word("fghij"))
        assert len(scored.words) == 2

    def test_chunked_dictionary(self):
        all_guesses = WordCollection.from_file("valid_combined.txt")
        guesses_1 = all_guesses[0:10]
        guesses_2 = all_guesses[10:20]
        all_solutions = WordCollection.from_file("valid_solutions.txt")
        solutions = all_solutions[0:2000:100]
        d1 = SolutionDictionary(guesses_1, solutions)
        d2 = SolutionDictionary(guesses_2, solutions)
        assert len(d1.dict) == 10
        d1.append(d2)
        assert len(d1.dict) == 20

    def test_make_slice_of_descriptions(self):
        all_guesses = WordCollection.from_file("valid_combined.txt")
        guesses_1 = all
        all_solutions = WordCollection.from_file("valid_solutions.txt")





