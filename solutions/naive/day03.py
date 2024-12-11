from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter
import re

class WholeLineSplitter(BaseLinesSplitter):
    def split(self):
        return "".join(self.lines)

class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=3, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = WholeLineSplitter(self.test_data).split()
        self.data = WholeLineSplitter(self.data).split()

    def exec_mul(txt):
        l_val = int(txt.split("(")[1].split(",")[0])
        r_val = int(txt.split(",")[1].split(")")[0])
        return l_val * r_val

    def get_matches(text):
        return re.findall(r'mul\([0-9]{1,3},[0-9]{1,3}\)', text)
    
    def get_matches_commands(text):
        return re.findall(r'mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don\'t\(\)', text)

    def part_1(self, data):
        return sum([Solver.exec_mul(txt) for txt in Solver.get_matches(data)])
    
    def part_2(self, data):
        matches = Solver.get_matches_commands(data)
        valid_matches = []
        keep = True
        for txt in matches:
            if txt=="do()":
                keep = True
                continue
            if txt=="don't()":
                keep = False
                continue
            if keep:
                valid_matches.append(txt)

        return sum([Solver.exec_mul(txt) for txt in valid_matches])