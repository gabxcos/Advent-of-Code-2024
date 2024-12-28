from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class OnsenSplitter(BaseLinesSplitter):
    def split(self):
        split_index = self.lines.index("")

        towels = []
        for line in self.lines[:split_index]:
            towels.extend(line.split(", "))

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
        res = []
        for i,d in enumerate(self.designs):
            r = self.solve_design(d)
            res.append(min(1, r))
            if self.debug:
                print(f"{i} : {d} --> {r}")
        return sum(res)
    
    def part_2(self, data):
        self.setup(data)
        res = []
        for i,d in enumerate(self.designs):
            r = self.solve_design(d, just_one=False)
            res.append(r)
            if self.debug:
                print(f"{i} : {d} --> {r}")
        return sum(res)
