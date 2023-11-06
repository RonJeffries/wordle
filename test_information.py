import pickle
import time
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
from math import log2

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

    def test_known_values_function(self):
        solutions = ["azzzz", "zbzzz", "zzczz", "zzzdz"]
        guess = "dcbay"
        _guess, info = expected_information(guess, solutions)
        assert info == 2

    def test_first_info_function(self):
        collection_of_words = WordCollection.from_file("valid_solutions.txt").words
        solutions = [word.word for word in collection_of_words]
        word = "abate"
        _guess, expected_info = expected_information(word, solutions)
        assert expected_info == pytest.approx(4.63, abs=0.05)

    @pytest.mark.skip("28 seconds")
    def test_all_words(self):
        collection_of_solution_words = WordCollection.from_file("valid_solutions.txt").words
        solutions = [word.word for word in collection_of_solution_words]
        collection_of_all_guess_words = WordCollection.from_file("valid_combined.txt").words
        guesses = [guess.word for guess in collection_of_all_guess_words]
        t0 = time.time()
        unordered = map(expected_information, guesses, repeat(solutions))
        ordered = sorted(unordered, key=lambda pair: pair[1], reverse=True)
        print(time.time() - t0)
        print(ordered[0:10])
        assert False

    @pytest.mark.skip("6.5 sec at 8, 7.8 at 4")
    def test_all_words_concurrent(self):
        collection_of_solution_words = WordCollection.from_file("valid_solutions.txt").words
        solutions = [word.word for word in collection_of_solution_words]
        collection_of_all_guess_words = WordCollection.from_file("valid_combined.txt").words
        guesses = [guess.word for guess in collection_of_all_guess_words]
        t0 = time.time()
        with ProcessPoolExecutor(8) as exec:
            unordered = exec.map(expected_information, guesses, repeat(solutions))
        ordered = sorted(unordered, key=lambda pair: pair[1], reverse=True)
        print(time.time() - t0)
        print(ordered[0:10])
        assert False

    @pytest.mark.skip("slow because of calc not pickling")
    def test_pickling(self):
        collection_of_solution_words = WordCollection.from_file("valid_solutions.txt").words
        solutions = [word.word for word in collection_of_solution_words]
        collection_of_all_guess_words = WordCollection.from_file("valid_combined.txt").words
        guesses = [guess.word for guess in collection_of_all_guess_words]
        unordered = map(expected_information, guesses, repeat(solutions))
        ordered = sorted(unordered, key=lambda pair: pair[1], reverse=True)
        t0 = time.time()
        dump = pickle.dumps((guesses, solutions))
        pickle.loads(dump)
        dump = pickle.dumps(ordered)
        pickle.loads(dump)
        print(time.time() - t0)
        # assert False

def expected_information(guess, solutions):
    buckets = {}
    total = len(solutions)
    for solution in solutions:
        score = compute_score(guess, solution)
        try:
            buckets[score] += 1
        except KeyError:
            buckets[score] = 1
    info = 0
    for count in buckets.values():
        probability =count /total
        info += probability*log2(1/probability)
    return guess, info


def compute_score(guess, solution):
    answer = [0, 0, 0, 0, 0]
    available_letters = list(solution)  # cannot cache this, we destroy it
    for i in range(5):
        if guess[i] == solution[i]:
            answer[i] = 2
            available_letters[i] = 0
    for i in range(5):
        if answer[i] != 2:
            if (w := guess[i]) in available_letters:
                answer[i] = 1
                available_letters[available_letters.index(w)] = 0
    return answer[4] + 10*(answer[3] + 10*(answer[2] + 10*(answer[1] + 10*answer[0])))
    # a0, a1, a2, a3, a4 = answer  # no improvement
    # return (a4 << 16) + (a3 << 12) + (a2 << 8) + (a1 << 4) + a0



