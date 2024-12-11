from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class MatrixSplitter(BaseLinesSplitter):
    def split(self):
        return [list(l) for l in self.lines]
    
class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=8, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = MatrixSplitter(self.test_data).split()
        self.data = MatrixSplitter(self.data).split()

    def setup(self, data):
        self.lines = data
        self.antennas = {}

        self.width = len(self.lines[0])
        self.height = len(self.lines)

        for y in range(self.height):
            for x in range(self.width):
                val = self.lines[y][x]
                if val != ".":
                    if val in self.antennas:
                        self.antennas[val].append((x, y))
                    else:
                        self.antennas[val] = [(x,y)]

    
    def get_antinodes(self, nodeA, nodeB, just_one = True):
    
        x_a, y_a = nodeA
        x_b, y_b = nodeB
        vec_x = x_a - x_b
        vec_y = y_a - y_b

        repeat = 1 if just_one else min(self.width, self.height)

        ants = []
        # First side
        for i in range(repeat):
            ant_x = x_a + vec_x * (i+1)
            ant_y = y_a + vec_y * (i+1)
            if (0 <= ant_x < self.width) and (0 <= ant_y < self.height):
                ants.append((ant_x, ant_y))
            else:
                break

        # Other side
        for i in range(repeat):
            ant_x = x_b - vec_x * (i+1)
            ant_y = y_b - vec_y * (i+1)
            if (0 <= ant_x < self.width) and (0 <= ant_y < self.height):
                ants.append((ant_x, ant_y))
            else:
                break
    
        return ants

    def is_valid_node(self, node):
        x,y = node
        if (0 <= x < self.width) and (0 <= y < self.height):
            return True
        return False

    def part_1(self, data):
        self.setup(data)

        antinodes = []
        for _,nodes in self.antennas.items():
            for nodeA in nodes:
                for nodeB in nodes:
                    if nodeA!=nodeB:
                        antinodes.extend(self.get_antinodes(nodeA, nodeB))
        antinodes = list(set(antinodes))
        return len(antinodes)
    
    def part_2(self, data):
        self.setup(data)

        antinodes = []
        for _,nodes in self.antennas.items():
            for nodeA in nodes:
                for nodeB in nodes:
                    if nodeA!=nodeB:
                        antinodes.extend(self.get_antinodes(nodeA, nodeB, False))
                    else:
                        antinodes.append(nodeA)
        antinodes = list(set(antinodes))
        return len(antinodes)