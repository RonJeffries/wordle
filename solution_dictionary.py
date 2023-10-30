
class Statistic:
    def __init__(self, word, buckets):
        self.word = word
        self.number_of_buckets = buckets

    def __repr__(self):
        return f"S('{self.word.word}' buckets: {self.number_of_buckets:3d}"


class SolutionDictionary:
    def __init__(self, guesses, solutions):
        self.dict = self.create_dict(guesses, solutions)

    @staticmethod
    def create_dict(guesses, solutions):
        solutions_dict = {}  # guess -> dict (score -> [solutions])
        for guess in guesses:
            guess_dict = {}  # score -> [solutions]
            solutions_dict[guess] = guess_dict
            for solution in solutions:
                score = guess.score(solution)
                if not score in guess_dict:
                    guess_dict[score] = []
                guess_dict[score].append(solution)
        return solutions_dict

    def create_statistics(self):
        stats = []
        for word in self.dict:
            word_dict = self.dict[word]
            stat = Statistic(word, len(word_dict))
            stats.append(stat)

        def my_key(stat: Statistic):
            return -stat.number_of_buckets

        stats.sort(key=my_key)
        return stats

    def solutions_for(self, guess, score):
        try:
            return self.dict[guess][score]
        except KeyError:
            return []
