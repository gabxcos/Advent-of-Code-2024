from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class MemorySplitter(BaseLinesSplitter):
    def split(self):
        mem_bytes = []
        for l in self.lines:
            coords = [int(el) for el in l.split(",")]
            mem_bytes.append(coords[0] + 1j * coords[1])
        return mem_bytes
    
class MazeRunner():
    def __init__(self, pos, visited):
        self.pos = pos
        self.visited = visited
        self.loop = (pos in visited)

    def __repr__(self):
        return "(pos=%r, # visited=%r, loop=%r)" % (self.pos, len(self.visited), self.loop)

    def move(self, move):
        return self.__class__(self.pos+move, self.visited+[self.pos])

class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=18, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = MemorySplitter(self.test_data).split()
        self.data = MemorySplitter(self.data).split()

    def setup(self, data):
        self.to_be_corrupted = data
        self.corrupted = set()
        self.runners = [MazeRunner(0+1j*0, [])]
        self.winners = []
        self.size = 7 if (max([b.real for b in self.to_be_corrupted])<7) else 71
        self.part1_num = 12 if (self.size == 7) else 1024
        self.destination = (self.size-1) + 1j * (self.size-1)
        self.visited_scores = dict()

    def valid_runner(self, r: MazeRunner):
        if (0 <= r.pos.real < self.size) and (0 <= r.pos.imag < self.size) and (r.pos not in self.corrupted):
            return not r.loop
        return False
    
    def keep_best_per_pos(self, runners):
        new_runners = []
        all_pos = set([r.pos for r in runners])
        for pos in all_pos:
            pos_runner = sorted(list(filter(lambda x : (x.pos == pos), runners)), key = lambda r : len(r.visited))[0]
            if (pos_runner.pos not in self.visited_scores) or ((pos_runner.pos in self.visited_scores) and (self.visited_scores[pos_runner.pos] > len(pos_runner.visited))):
                self.visited_scores[pos_runner.pos] = len(pos_runner.visited)
                new_runners.append(pos_runner)
        return new_runners

    def get_top_n_runners(self, runners, top_n):
        runners = sorted(runners, key = lambda r : abs(self.destination - r.pos))
        return runners[:min(top_n, len(runners))]
    
    def print_maze(self):
        for y in range(self.size):
            string = ""
            for x in range(self.size):
                p = x + 1j * y
                if p in self.corrupted:
                    string+="#"
                elif any([p == r.pos for r in self.runners]):
                    string += "O"
                else:
                    string += "."
            print(string)
        print("\n\n")
    
    def reset(self):
        self.runners = [MazeRunner(0+1j*0, [])]
        self.winners = []
        self.visited_scores = dict()

    def part_1(self, data):
        self.setup(data)
        self.corrupted = set(self.to_be_corrupted[:self.part1_num])

        while len(self.runners)>0:
            new_runners = []
            for r in self.runners:
                new_runners.extend([r.move(m) for m in [1, -1, 1j, -1j]])
            new_runners = list(filter(lambda r: self.valid_runner(r), new_runners))
            new_runners = self.keep_best_per_pos(new_runners)

            winning_runners = list(filter(lambda r: (r.pos == self.destination), new_runners))
            non_winning_runners = list(filter(lambda r: (r.pos != self.destination), new_runners))
            non_winning_runners = self.get_top_n_runners(non_winning_runners, 2_000)


            self.runners = non_winning_runners
            self.winners.extend(winning_runners)

            if self.debug:
                print(len(self.runners), len(self.winners))
                self.print_maze()
        return min([len(r.visited) for r in self.winners])
    
    def part_2(self, data):
        self.setup(data)
        self.corrupted = set(self.to_be_corrupted[:self.part1_num])

        for i in range(self.part1_num, len(self.to_be_corrupted)):
            self.reset()
            new_byte = self.to_be_corrupted[i]
            self.corrupted.add(new_byte)

            # Run
            while len(self.runners)>0:
                new_runners = []
                for r in self.runners:
                    new_runners.extend([r.move(m) for m in [1, -1, 1j, -1j]])
                new_runners = list(filter(lambda r: self.valid_runner(r), new_runners))
                new_runners = self.keep_best_per_pos(new_runners)

                winning_runners = list(filter(lambda r: (r.pos == self.destination), new_runners))
                non_winning_runners = list(filter(lambda r: (r.pos != self.destination), new_runners))
                non_winning_runners = self.get_top_n_runners(non_winning_runners, 2_000)


                self.runners = non_winning_runners
                self.winners.extend(winning_runners)
            
            if self.debug: print(i)
            if len(self.winners) == 0:
                break
        return f"{int(new_byte.real)},{int(new_byte.imag)}"
