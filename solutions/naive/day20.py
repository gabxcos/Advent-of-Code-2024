from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class MazeSplitter(BaseLinesSplitter):
    def split(self):
        lines = [list(l) for l in self.lines]
        width = len(lines[0])
        height = len(lines)

        walls = []
        start = None
        end = None

        for x in range(0, width):
            for y in range(0, height):
                pos = x + 1j * y
                if lines[y][x]=="#":
                    walls.append(pos)
                elif lines[y][x]=="S":
                    start = pos
                elif lines[y][x]=="E":
                    end = pos

        return (width, height), walls, start, end

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
        super().__init__(day=20, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = MazeSplitter(self.test_data).split()
        self.data = MazeSplitter(self.data).split()

    def setup(self, data):
        (self.width, self.height), self.walls, self.start, self.end = data
        self.delta = 100 if (self.height > 20) else 64
        self.runners = [MazeRunner(self.start, [])]
        self.winning_path = None
        self.winning_score = None

    def valid_runner(self, r: MazeRunner):
        x, y = (r.pos.real, r.pos.imag)
        if not ((0 <= x < self.width) and (0 <= y < self.height)):
            return False
        return (not r.loop)
    
    def find_original_path(self):
        while (len(self.runners)>0) and (self.winning_path is None):
            new_runners = []
            for r in self.runners:
                for m in [1, -1, 1j, -1j]:
                    new_r = r.move(m)
                    if (not (new_r.pos in self.walls)) and (self.valid_runner(new_r)):
                        new_runners.append(new_r)

            not_winners = list(filter(lambda r: (r.pos != self.end), new_runners))
            self.runners = not_winners

            # Manage winners
            winners = list(filter(lambda r: (r.pos == self.end), new_runners))
            if len(winners)>0:
                winner = sorted(winners, key = lambda r : len(r.visited))[0]
                self.winning_path = winner.visited + [self.end]
                self.winning_score = len(self.winning_path)
    
    def check_cheat_2(self, start_pos):
        start_index = self.winning_path.index(start_pos)
        good_jumps = []
        for end_pos in self.winning_path[start_index+self.delta+1:]:
            dist = int(abs(start_pos.real - end_pos.real) + abs(start_pos.imag - end_pos.imag))
            if dist <= 2:
                good_jumps.append(end_pos)
        return len(good_jumps)


    def check_cheat_20(self, start_pos):
        def dist(start_pos, end_pos):
            return int(abs(start_pos.real - end_pos.real) + abs(start_pos.imag - end_pos.imag))

        start_index = self.winning_path.index(start_pos)
        possible_end_pos = {end_pos : (i+self.delta-dist(start_pos, end_pos)) for i, end_pos in enumerate(self.winning_path[start_index+self.delta:]) if (dist(start_pos, end_pos)<=20) and ((i-dist(start_pos, end_pos))>=0) }
        
        if self.debug:
            print(possible_end_pos)

        return len(possible_end_pos)

    def part_1(self, data):
        self.setup(data)
        self.find_original_path()
        good_jumps = [self.check_cheat_2(start_pos) for start_pos in self.winning_path[:-self.delta]]
        return sum(good_jumps)
    
    def part_2(self, data):
        self.setup(data)
        self.find_original_path()
        good_jumps = []
        for i, start_pos in enumerate(self.winning_path[:-self.delta+1]):
            good_jumps.append(self.check_cheat_20(start_pos))
            if self.debug:
                print(f"{i+1} / {len(self.winning_path)-self.delta+1}")
        return sum(good_jumps)
