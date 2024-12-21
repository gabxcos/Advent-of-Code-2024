import time
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

class Reindeer():
    def __init__(self, pos, facing, score, visited, turns = 0):
        self.pos = pos
        self.facing = facing
        self.score = score
        self.visited = visited
        self.loop = (self.pos in visited)
        self.turns = turns

    def __repr__(self):
        return "Reindeer(pos=%r, facing=%r, score=%r, visited=%r, loop=%r)" % (self.pos, self.facing, self.score, self.visited, self.loop)

    def move(self):
        return self.__class__(self.pos + self.facing, self.facing, self.score+1, self.visited+[self.pos])
    
    def turn_left(self):
        return self.__class__(self.pos, self.facing * (-1j), self.score+1_000, self.visited, self.turns -1)
    
    def turn_right(self):
        return self.__class__(self.pos, self.facing * 1j, self.score+1_000, self.visited, self.turns + 1)
    
class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=16, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = MazeSplitter(self.test_data).split()
        self.data = MazeSplitter(self.data).split()

    def setup(self, data, max_num_turns = 1, num_top_scores = 2_000):
        (self.width, self.height), self.walls, self.start, self.end = data
        
        self.reindeers = [Reindeer(self.start, (1), 0, [])]
        self.finished_reindeers = []
        self.max_num_turns = max_num_turns
        self.num_top_scores = num_top_scores
        self.local_min_score = {}

    def is_local_min_score(self, reindeer):
        if (reindeer.pos in self.local_min_score):
            if reindeer.turns == 0:
                if (self.local_min_score[reindeer.pos] < reindeer.score):
                    return False
            else:
                if (self.local_min_score[reindeer.pos] < (reindeer.score - 1000*self.max_num_turns)):
                    return False
        self.local_min_score[reindeer.pos] = reindeer.score
        return True

    def update_reindeers(self):
        new_reindeers = []
        for r in self.reindeers:
            new_reindeers.append(r.move())
            if (r.turns > - self.max_num_turns) and (r.turns < self.max_num_turns):
                if r.turns <= 0:
                    new_reindeers.append(r.turn_left())
                if r.turns >= 0:
                    new_reindeers.append(r.turn_right())

        valid_reindeers = list(filter(lambda r : (r.pos not in self.walls) and (not r.loop), new_reindeers))
        finished = list(filter(lambda r : (r.pos == self.end), valid_reindeers))
        self.finished_reindeers.extend(finished)
        min_score = 1e20 if len(self.finished_reindeers)==0 else min(list(map(lambda x:x.score, self.finished_reindeers)))

        not_finished = list(filter(lambda r : (r.pos != self.end) and (r.score < min_score) and self.is_local_min_score(r), valid_reindeers))
        not_finished = sorted(not_finished, key=lambda r:r.score)[:min(len(not_finished), self.num_top_scores)]
        self.reindeers = not_finished

    def print_maze(self):
        for y in range(self.height):
            string = ""
            for x in range(self.width):
                p = x + 1j * y
                if any([r.pos == p for r in self.reindeers]):
                    string += "O"
                elif p in self.walls:
                    string += "#"
                else:
                    string += "."
            print(string)
        print("\n\n")

    def part_1(self, data):
        self.setup(data)
        while len(self.reindeers)>0:
            self.update_reindeers()
            print(len(self.reindeers), len(self.finished_reindeers))
            if self.debug: 
                self.print_maze()
                time.sleep(0.1)
        return min(list(map(lambda r:r.score, self.finished_reindeers)))
    
    def part_2(self, data):
        self.setup(data)
        while len(self.reindeers)>0:
            self.update_reindeers()
            print(len(self.reindeers), len(self.finished_reindeers))
            if self.debug: 
                self.print_maze()
                time.sleep(0.1)
        min_score = min(list(map(lambda r:r.score, self.finished_reindeers)))
        best_paths = list(filter(lambda r: (r.score == min_score), self.finished_reindeers))
        all_nodes = []
        for r in best_paths:
            all_nodes.extend(r.visited)
        return len(set(all_nodes))+1