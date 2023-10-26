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

