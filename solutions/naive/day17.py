import time
from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class ProgramSplitter(BaseLinesSplitter):
    def split(self):
        A = int(self.lines[0].split(" ")[-1])
        B = int(self.lines[1].split(" ")[-1])
        C = int(self.lines[2].split(" ")[-1])

        program = [int(op) for op in self.lines[4].split(" ")[-1].split(",")]
        return A, B, C, program
    
class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=17, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = ProgramSplitter(self.test_data).split()
        self.data = ProgramSplitter(self.data).split()

    def setup(self, data):
        self.A, self.B, self.C, self.program = data
        self.outs = []
        self.pc = 0

    def get_combo(self, operand):
        if 0 <= operand < 4:
            return operand
        elif operand == 4:
            return self.A
        elif operand == 5:
            return self.B
        elif operand == 6:
            return self.C
        else:
            print(f"Received unexpected combo operand: {operand}")
            exit()
        
    def adv(self, operand):
        self.A = self.A // (2**self.get_combo(operand))

    def bxl(self, operand):
        self.B = self.B ^ operand

    def bst(self, operand):
        self.B = self.get_combo(operand) % 8

    def jnz(self, operand):
        if self.A != 0:
            self.pc = operand - 2

    def bxc(self, operand):
        self.B = self.B ^ self.C

    def out(self, operand):
        self.outs.append(self.get_combo(operand) % 8)

    def bdv(self, operand):
        self.B = self.A // (2**self.get_combo(operand))

    def cdv(self, operand):
        self.C = self.A // (2**self.get_combo(operand))

    @staticmethod
    def get_func(opcode):
        return {
            0: "adv",
            1: "bxl",
            2: "bst",
            3: "jnz",
            4: "bxc",
            5: "out",
            6: "bdv",
            7: "cdv"
        }[opcode]

    def operate(self):
        opcode = self.program[self.pc]
        operand = self.program[self.pc + 1]

        func = self.__getattribute__(Solver.get_func(opcode))
        func(operand)

        self.pc += 2

    
    def print_op(self):
        opcode = self.program[self.pc]
        operand = self.program[self.pc + 1]
        return {
            0: f"adv: A = {self.A} // (2^{self.get_combo(operand)})",
            1: f"bxl: B = {self.B} ^ {operand}",
            2: f"bst: B = {self.get_combo(operand)} mod 8",
            3: f"jnz: {'Doing nothing' if (self.A==0) else 'Jumping to PC = '+str(operand)}",
            4: f"bxc: B = {self.B} ^ {self.C}",
            5: f"out: Output {self.get_combo(operand)} mod 8",
            6: f"bdv: B = {self.A} // (2^{self.get_combo(operand)})",
            7: f"cdv: C = {self.A} // (2^{self.get_combo(operand)})",
        }[opcode]
    
    def valid_output(self, complete=False):
        if complete and (len(self.outs) != len(self.program)):
                return False
            
        if len(self.outs) < 1:
            return True
        
        if len(self.outs) > len(self.program):
            return False
        
        return all([(self.program[i]==el) for i, el in enumerate(self.outs)])

    def part_1(self, data):
        self.setup(data)
        while self.pc < (len(self.program) - 1):
            if self.debug:
                print(f"A={self.A}, B={self.B}, C={self.C} -> {self.print_op()} -> OUT={self.outs} - - - (Program: {self.program})")
            self.operate()
        print(",".join([str(o) for o in self.outs]))
        return int("".join([str(o) for o in self.outs]))
    
    def part_2(self, data):
        self.setup(data)
        first = True
        candidates = []
        for code in self.program[::-1]:
            r = None
            new_candidates = []
            if first:
                r = range(1,10)
            else:
                r = []
                for c in candidates:
                    r.extend([c*8+i for i in range(9)])
            first = False

            for solution in r:
                self.setup(data)
                self.A = solution
                while (self.pc < (len(self.program) - 1)) and (self.valid_output()):
                    self.operate()

                if self.outs[0]==code:
                    new_candidates.append(solution)
            
            candidates = new_candidates
            if self.debug:
                print(candidates)

        return min(candidates)