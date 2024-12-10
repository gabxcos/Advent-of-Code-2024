from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class MatrixSplitter(BaseLinesSplitter):
    def split(self):
        return [list(l) for l in self.lines]
    
class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, benchmark: bool = True):
        super().__init__(day=6, raw=True, skip_test=skip_test, benchmark=benchmark)
        self.test_data = MatrixSplitter(self.test_data).split()
        self.data = MatrixSplitter(self.data).split()

    def setup(self, data):
        self.lines = data

        self.width = len(self.lines[0])
        self.height = len(self.lines)

        self.obstacle_pos = []
        self.og_guard_pos = None

        for x in range(self.width):
            for y in range(self.height):
                if self.lines[y][x] == "#":
                    self.obstacle_pos.append((x, y))
                elif self.lines[y][x] == "^":
                    self.og_guard_pos = (x, y)

        self.directions = [
            (0, -1), # up
            (1, 0), # right
            (0, 1), # down
            (-1, 0) # left
        ]


    def count_visited(self):
        dir_i = 0
        curr_dir = self.directions[dir_i]

        guard_pos = self.og_guard_pos
        while (0 <= guard_pos[0] < self.width) and (0 <= guard_pos[1] < self.height):
            g_x, g_y = guard_pos
            self.lines[g_y][g_x] = "X"
            
            checking = True
            while checking:
                new_pos = (g_x + curr_dir[0], g_y + curr_dir[1])
                new_x, new_y = new_pos
                if (0 <= new_x < self.width) and (0 <= new_y < self.height):
                    if self.lines[new_y][new_x] == "#":
                        dir_i = (dir_i+1)%4
                        curr_dir = self.directions[dir_i]
                    else:
                        checking = False
                else:
                    checking = False
            guard_pos = new_pos

        new_lines = ["".join(l) for l in self.lines]
        grid = "\n".join(new_lines)
        return grid.count("X")

    
    def test_if_loop(self, new_obstacle_pos):
        # Initialize problem
        guard_pos = (self.og_guard_pos[0], self.og_guard_pos[1])
        dir_i = 0
        curr_dir = self.directions[dir_i]

        is_loop = False
        is_starting = True
        moves = 0
        while (0 <= guard_pos[0] < self.width) and (0 <= guard_pos[1] < self.height):
            g_x, g_y = guard_pos
            
            checking = True
            while checking:
                new_pos = (g_x + curr_dir[0], g_y + curr_dir[1])
                new_x, new_y = new_pos
                if (0 <= new_x < self.width) and (0 <= new_y < self.height):
                    if (self.lines[new_y][new_x] == "#") or ( (new_x==new_obstacle_pos[0]) and (new_y==new_obstacle_pos[1])):
                        dir_i = (dir_i+1)%4
                        curr_dir = self.directions[dir_i]
                    else:
                        checking = False
                else:
                    checking = False

            new_x, new_y = new_pos
            if (
                (new_x==self.og_guard_pos[0]) and (new_y==self.og_guard_pos[1]) and (dir_i == 0)
            ) or (
                (g_x==self.og_guard_pos[0]) and (g_y==self.og_guard_pos[1]) and (dir_i == 0) and (not is_starting)
            ) or (
                moves > (self.width * self.height)
            ):
                is_loop = True
                break

            guard_pos = new_pos
            is_starting = False
            moves += 1
        
        return is_loop

    def part_1(self, data):
        self.setup(data)
        return self.count_visited()
    
    def part_2(self, data):
        self.setup(data)

        counter = 0
        for x in range(self.width):
            for y in range(self.height):
                if (
                    (self.og_guard_pos[0]==x) and (self.og_guard_pos[1]==y)
                ) or (
                    self.lines[y][x] == "#"
                ):
                    continue

                if self.test_if_loop((x, y)): counter += 1

        return counter