from functools import reduce
import operator
import matplotlib.pyplot as plt
from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class RobotSplitter(BaseLinesSplitter):
    @staticmethod
    def get_position(string):
        xy = [int(el) for el in string.split("=")[1].split(" ")[0].split(",")]
        return xy[0] + 1j * xy[1]

    staticmethod
    def get_velocity(string):
        xy = [int(el) for el in string.split("=")[2].split(",")]
        return xy[0] + 1j * xy[1]
    
    def split(self):
        return [(RobotSplitter.get_position(line), RobotSplitter.get_velocity(line)) for line in self.lines]

    
class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=14, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = RobotSplitter(self.test_data).split()
        self.data = RobotSplitter(self.data).split()

    def setup(self, data):
        self.robots = data
        # Test size
        if len(self.robots) < 100:
            self.width = 11
            self.height = 7
            self.stem_size = 20 # placebo, won't find
        else:
            self.width = 101
            self.height = 103
            self.stem_size = 20

    def move_n_sec(self, n):
        new_robots = []
        for r in self.robots:
            p, v = r
            new_p = p + n * v
            new_x = new_p.real % self.width
            new_y = new_p.imag % self.height
            new_robots.append( ( new_x + 1j * new_y, v) )
        self.robots = new_robots


    def get_quadrants(self):
        q1 = [r for r in self.robots if (r[0].real < (self.width // 2)) and (r[0].imag < (self.height // 2))]
        q2 = [r for r in self.robots if (r[0].real < (self.width // 2)) and (r[0].imag > (self.height // 2))]
        q3 = [r for r in self.robots if (r[0].real > (self.width // 2)) and (r[0].imag < (self.height // 2))]
        q4 = [r for r in self.robots if (r[0].real > (self.width // 2)) and (r[0].imag > (self.height // 2))]
        self.quadrants = q1, q2, q3, q4
        return self.quadrants
    
    def get_score(self):
        return reduce(operator.mul, [len(q) for q in self.quadrants], 1)
    
    def get_robot_coords(self):
        pos_arr = [r[0] for r in self.robots]
        x = [p.real for p in pos_arr]
        y = [p.imag for p in pos_arr]
        return x, y
    
    def has_stem(self, x, y):
        x_counts = [x.count(el) for el in set(x)]
        y_counts = [y.count(el) for el in set(y)]
        return min([max(x_counts), max(y_counts)]) >= self.stem_size
    
    @staticmethod
    def plot_robots(x, y):
        fig=plt.figure()
        ax=fig.add_axes([0,0,1,1])
        ax.scatter(x, y, color='r')
        plt.show()

    def part_1(self, data):
        self.setup(data)
        self.move_n_sec(100)
        self.get_quadrants()
        return self.get_score()
    
    def part_2(self, data):
        self.setup(data)
        steps = 0
        while steps < 10_000:
            self.move_n_sec(1)
            steps += 1
            x, y = self.get_robot_coords()
            if self.has_stem(x, y):
                if self.debug:
                    print(steps)
                    Solver.plot_robots(x, y)
                    plt.pause(1)
                    plt.close()
                break
        return steps