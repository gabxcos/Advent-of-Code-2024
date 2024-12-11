from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from math import exp


class OneLineIntSplitter(BaseLinesSplitter):
    def split(self):
        return [int(el) for el in self.lines[0].split(" ") if el!=""]

class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=11, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = OneLineIntSplitter(self.test_data).split()
        self.data = OneLineIntSplitter(self.data).split()


    @staticmethod
    def blink(line):
        new_line = []
        for num in line:
            if num==0:
                new_line.append(1)
            elif (len(str(num))%2) == 0:
                mid_point = len(str(num))//2
                n_a = int(str(num)[:mid_point])
                n_b = int(str(num)[mid_point:])
                new_line.extend([n_a, n_b])
            else:
                new_line.append(num * 2024)
        return new_line
    
    @staticmethod
    def dict_blink(d):
        new_d = {}
        for num in d:
            new_num = []
            if num==0:
                new_num.append(1)
            elif (len(str(num))%2) == 0:
                mid_point = len(str(num))//2
                n_a = int(str(num)[:mid_point])
                n_b = int(str(num)[mid_point:])
                new_num.extend([n_a, n_b])
            else:
                new_num.append(num * 2024)

            for n in new_num:
                if n in new_d:
                    new_d[n] += d[num]
                else:
                    new_d[n] = d[num]

        return new_d


    def part_1(self, data):
        l_x = [0]
        l_y = [len(data)]
        for i in range(1, 26):
            data = Solver.blink(data)
            l_x.append(i)
            l_y.append(len(data))

        if self.debug:
            # Test 1: Do some experimentations for exponential curve fitting
            x = np.array(l_x)#.reshape((-1, 1))
            y = np.array(l_y)

            res = np.polyfit(x, np.log(y), 1, w=np.sqrt(y))
            res_opt = curve_fit(lambda t,a,b: a*np.exp(b*t),  x,  y, p0=(exp(res[1]), res[0]))
            print(res_opt[0][0], res_opt[0][1])

            y_test_scipy = np.array([res_opt[0][0] * exp(res_opt[0][1] * _x) for _x in l_x])
            
            x = x.reshape((-1, 1))
            plt.title("Matplotlib demo") 
            plt.xlabel("x axis caption") 
            plt.ylabel("y axis caption") 
            plt.plot(x,y)
            plt.plot(x,y_test_scipy) 
            plt.show()

            print("Estimate for 75: ", res_opt[0][0] * exp(res_opt[0][1] * 75), "\n")

            # Test 2: Searching for a function for invariants
            print("Testing first 25 iterations for invariant 0:")
            inv_data = [0]
            inv_l_x = [0]
            inv_l_y = [len(inv_data)]
            print(f"{inv_l_x[0]}: {inv_l_y[0]} --> {inv_data}")
            for i in range(1, 26):
                inv_data = Solver.blink(inv_data)
                inv_l_x.append(i)
                inv_l_y.append(len(inv_data))
                if i < 11:
                    print(f"{inv_l_x[i]}: {inv_l_y[i]} --> {inv_data}")
            print(inv_l_y)

        return l_y[25]
    
    def part_2(self, data):
        d = { k : data.count(k) for k in list(set(data))}

        for _ in range(75):
            d = Solver.dict_blink(d)
        
        return sum(list(d.values()))
    