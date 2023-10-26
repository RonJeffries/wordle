from word import Word
from word_collection import WordCollection


class TestCollectionManipulation:
    def test_elimination(self):
        strings = "abcde fghij aghij fghid".split(" ")
        words = [Word(s) for s in strings]
        coll = WordCollection(words)
        assert len(coll) == 4
