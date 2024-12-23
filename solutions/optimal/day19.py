from functools import reduce
from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class OnsenSplitter(BaseLinesSplitter):
    def split(self):
        split_index = self.lines.index("")
        towels = reduce(lambda x, y: x + y, [l.split(", ") for l in self.lines[:split_index]])
        designs = [l for l in self.lines[split_index+1:]]
        return set(towels), designs

class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=19, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = OnsenSplitter(self.test_data).split()
        self.data = OnsenSplitter(self.data).split()

    def setup(self, data):
        self.towels, self.designs = data
    
    def solve_design(self, s, just_one = True):
        dp = [0] * (len(s) + 1)
        dp[0] = 1
        for i in range(1, len(s) + 1):
            for word in self.towels:
                word_len = len(word)
                if i >= word_len and s[i - word_len:i] == word and dp[i - word_len]>0:
                    dp[i] += dp[i - word_len]
                    if just_one:
                        break
        return dp[len(s)]


    def part_1(self, data):
        self.setup(data)
        return sum([1 for d in self.designs if self.solve_design(d)>0])
    
    def part_2(self, data):
        self.setup(data)
        return sum([self.solve_design(d, just_one=False) for d in self.designs])
