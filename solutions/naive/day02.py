from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class IntSplitter(BaseLinesSplitter):
    def split(self):
        return [[int(el) for el in l.split(" ") if el!=""] for l in self.lines]

class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=2, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = IntSplitter(self.test_data).split()
        self.data = IntSplitter(self.data).split()


    @staticmethod
    def check_safe_one(line):
        diffs_line = [line[i] - line[i+1] for i in range(len(line)-1)]
        min_diff = min(diffs_line)
        max_diff = max(diffs_line)

        if (min_diff<=0) and (max_diff>=0): return False

        abs_diffs = [abs(min_diff), abs(max_diff)]
        if (min(abs_diffs)<1) or (max(abs_diffs)>3): return False
        
        return True


    @staticmethod
    def check_safe(line):
        line_tests = [list(line) for _ in range(len(line)+1)]
        for i in range(len(line)):
            del line_tests[i+1][i]

        for line_test in line_tests:
            if Solver.check_safe_one(line_test): return True
        return False

    def part_1(self, data):
        return sum([int(Solver.check_safe_one(line)) for line in data])
    
    def part_2(self, data):
        return sum([int(Solver.check_safe(line)) for line in data])