import pickle
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
    def test_full_timing_and_create_file(self):
        all_guesses = WordCollection.from_file("valid_combined.txt")
        all_solutions = WordCollection.from_file("valid_solutions.txt")
        t0 = time.time()
        dict = SolutionDictionary(all_guesses, all_solutions)
        t1 = time.time()
        build_time = t1 - t0
        with open("/users/ron/Desktop/SD.pcl", "wb") as pick:
            pickle.dump(dict, pick)
        save_time = time.time() - t1
        print(f"build: {build_time:.3f}, save: {save_time:.3f}")
        # build: 32.641, save: 3.253
        assert False

    @pytest.mark.skip("3.5 seconds is too long")
    def test_file_read_time(self):
        t0 = time.time()
        with open("/users/ron/Desktop/SD.pcl", "rb") as pick:
            dict = pickle.load(pick)
        t1 = time.time()
        print(f"load time: {t1-t0:.3f}")
        # load time: 3.553
        assert False

    def test_easy_statistics(self):
        all_guesses = WordCollection.from_file("valid_combined.txt")
        guesses = all_guesses[0:10000:500]
        all_solutions = WordCollection.from_file("valid_solutions.txt")
        solutions = all_solutions[0:2000:100]
        sd = SolutionDictionary(guesses, solutions)
        stats = sd.create_statistics()
        print(Statistic.header())
        for stat in stats:
            print(stat)
        # no longer valid, changed sort order
        # stat = stats[0]
        # assert stat.number_of_buckets == 15
        # assert stat.max_words == 3
        # assert False

    @pytest.mark.skip("working")
    def test_statistics(self):
        with open("/users/ron/Desktop/SD.pcl", "rb") as pick:
            sd = pickle.load(pick)
        stats = sd.create_statistics()
        print(Statistic.header())
        for stat in stats[0:20]:
            print(stat)
        print("...")
        for stat in stats[-10:]:
            print(stat)
        assert False

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

    def test_from_slices(self):
        all_guesses = WordCollection.from_file("valid_combined.txt")
        guesses_1 = all_guesses[0:10]
        guesses_2 = all_guesses[10:20]
        print(guesses_2)
        all_solutions = WordCollection.from_file("valid_solutions.txt")
        solutions = all_solutions[0:10]
        sd = SolutionDictionary.from_slices(solutions, guesses_1, guesses_2)
        gd = sd.solutions_for(Word("aahed"), 20000)
        sols = gd.words
        expected = WordCollection.from_strings("abbot", "abort")
        assert sols == expected
        gd = sd.solutions_for(Word("abate"), 22001)
        sols = gd.words
        expected = WordCollection.from_strings("abbey", "abled")
        assert sols == expected

    # def test_write_file(self):
    #     with open("/users/ron/Desktop/scratch.txt", "w") as scratch:
    #         scratch.writelines(["hello\n", "world\n"])

    @pytest.mark.skip("working on it")
    def test_pickling_and_unpickling(self):
        all_guesses = WordCollection.from_file("valid_combined.txt")
        all_solutions = WordCollection.from_file("valid_solutions.txt")
        guesses = all_guesses[0:10000:500]
        solutions = all_solutions[0:2000:100]
        solution_dict = SolutionDictionary(guesses, solutions)
        t0 = time.time()
        with open("/users/ron/Desktop/test.pcl", "wb") as pick:
            pickle.dump(solution_dict, pick)
        t1 = time.time()
        t_write = t1 - t0
        with open("/users/ron/Desktop/test.pcl", "rb") as pick:
            unpickled = pickle.load(pick)
        t_read = time.time() - t1
        print(f"Pickle: {t_write:.5f}, Unpickle: {t_read:.5f}")
        guess = Word("berth")
        solution = Word("frail")
        score = guess.score(solution)
        assert score == 100
        solutions = unpickled.solutions_for(guess, score)
        expected = ScoreDescription.from_strings(score, "frail", "grasp", "rival")
        assert solutions == expected
        assert False






