# The thrashed, non-working version is under the `trashed` folder. External help was used for coming up with this solution.
from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter
from itertools import product

class MachineSplitter(BaseLinesSplitter):
    @staticmethod
    def get_move(string, prize = False):
        split_char = "=" if prize else "+"
        x = int(string.split(split_char)[1].split(",")[0])
        y = int(string.split(split_char)[-1])
        return x + y * 1j
    
    def get_machine(self, i):
        A_move = MachineSplitter.get_move(self.lines[4*i])
        B_move = MachineSplitter.get_move(self.lines[4*i+1])
        prize_move = MachineSplitter.get_move(self.lines[4*i+2], True)
        return [A_move, B_move, prize_move]

    def split(self):
        iterations = (len(self.lines)+1)//4
        return [self.get_machine(i) for i in range(iterations)]

    
class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=13, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = MachineSplitter(self.test_data).split()
        self.data = MachineSplitter(self.data).split()

    @staticmethod
    def solve_machine(machine):
        A_move, B_move, prize_move = machine

        min_res = 400
        found_solution = False

        max_iterations = int(max( (prize_move / A_move).real, (prize_move / B_move).real ))+1

        for num_A, num_B in product(range(max_iterations), repeat=2):
            if (num_A * A_move + num_B * B_move) == prize_move:
                found_solution = True
                min_res = min(min_res, 3 * num_A + num_B)
        return min_res if found_solution else 0


    def part_1(self, data):
        return sum([Solver.solve_machine(machine) for machine in data])
    
    def part_2(self, data):
        return 0