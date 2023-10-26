import sys

import pytest

from word import Word
from word_collection import WordCollection


class TestCollectionManipulation:
    def test_creation(self):
        strings = "abcde fghij aghij fghid".split(" ")
        words = [Word(s) for s in strings]
        coll = WordCollection(words)
        assert len(coll) == 4

    def test_elimination(self):
        guess = Word("abcde")
        soln = Word("dayyy")
        score = guess.score(soln)
        assert score == [1, 0, 0, 1, 0]
        strings = "abcde fghij ageij fghid".split(" ")
        words = [Word(s) for s in strings]
        coll = WordCollection(words)
        to_eliminate = guess.to_eliminate(score)
        assert to_eliminate == "bce"
        limited_words = coll.eliminate(to_eliminate)
        assert len(limited_words) == 2

    def test_big_elimination(self):
        combined = WordCollection.from_file("valid_combined.txt")
        solution = Word("aback")
        guess = Word("abbas")
        score = guess.score(solution)
        assert score == [2, 2, 0, 1, 0]
        to_eliminate = guess.to_eliminate(score)
        assert to_eliminate == "s"
        remaining = combined.eliminate(to_eliminate)
        assert len(remaining) == 7036
        check = Word("sssss")
        for word in remaining.words:
            assert word.score(check) == [0, 0, 0, 0, 0]

    # @pytest.mark.timeout(300)
    # def test_massive(self):
    #     combined = WordCollection.from_file("valid_combined.txt")
    #     solutions = WordCollection.from_file("valid_solutions.txt")
    #     scores = {}
    #     for word in combined.words:
    #         scores[word.word] = 0
    #         for soln in solutions. words:
    #             score = word.score(soln)
    #             elim = word.to_eliminate(score)
    #             tally = 0
    #             for candidate in combined.words:
    #                 if candidate.contains_none(elim):
    #                     tally += 1
    #             scores[word.word] += tally

    @pytest.mark.timeout(2)
    def test_not_so_massive(self):
        n = 100
        combined = WordCollection.from_file("valid_combined.txt")
        combined.trim(n)
        solutions = WordCollection.from_file("valid_solutions.txt")
        solutions.trim(n)
        scores = {}
        for word in combined.words:  # 12000
            scores[word.word] = 0
            for soln in solutions.words:  # x 2000 = 24 000 000
                score = word.score(soln)
                elim = word.to_eliminate(score)
                tally = 0
                for candidate in combined.words: # x 12000 = 288 000 000 000
                    if candidate.contains_none(elim):
                        tally += 1
                scores[word.word] += tally
        assert  len(scores) == n

    def test_list(self):
        spread = list("abcde")
        assert spread == ["a", "b", "c", "d", "e"]

    def test_list_size(self):
        s0 = sys.getsizeof([])
        assert s0 == 56
        s1 = sys.getsizeof(["a"])
        assert s1 == 64
        s5 = sys.getsizeof(["a", "b", "c", "d", "e"])
        assert s5 == 104

