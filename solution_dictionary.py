class SolutionDictionary:
    def __init__(self, guesses, solutions):
        self.dict = self.create_dict(guesses, solutions)

    def create_dict(self, guesses, solutions):
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

    def solutions_for(self, word, score):
        try:
            return self.dict[word][score]
        except KeyError:
            return []
