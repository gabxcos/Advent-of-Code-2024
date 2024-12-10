import argparse, importlib, datetime

_today = datetime.date.today().day

def solve(day: int = -1, part: int = -1, optimal: bool = False, skip_test: bool = False, benchmark: bool = True):
    try:
        solution = importlib.import_module(f"solutions.{'optimal' if optimal else 'naive'}.day{day:02d}").Solver(skip_test, benchmark).solve(part)
        return solution
    except:
        if not 0 < day < 26: print("Day number must be between 1 and 25")
        elif part not in [1, 2]: print("Part number must be 1 or 2")
        else: print(f"There is no available {'optimal' if optimal else 'naive'} working solution for part {part} of day {day} yet.\n")
        return None


def solve_all_until(day: int = min(_today, 25), optimal: bool = False, skip_test: bool = False, benchmark: bool = True):
    solutions = {d:[] for d in range(1, day+1)}
    for d in range(1, day+1):
        print(f"# Day {d}:")
        for p in [1,2]:
            print(f"- Part {p}:")
            solutions[d].append( solve(d, p, optimal, skip_test, benchmark) )
        print("-"*20)
    
    return solutions


def solve_all(optimal: bool = False, skip_test: bool = False, benchmark: bool = True):
    return solve_all_until(25, optimal, skip_test, benchmark)


def main():
    parser = argparse.ArgumentParser(description="Bulk runner of gabxcos' Advent of Code 2024 solutions")
    parser.add_argument("-d", "--day", dest="day", default=_today, metavar="day_number", type=int, help="Required, day number of the AoC event")
    parser.add_argument("-p", "--part", dest="part", default=1, metavar="part_number", type=int, help="Required, part number of the day of the AoC event")
    parser.add_argument("--optimal", action="store_true", help="Optional, use the intended optimal solution instead of the one I actually came up with")
    parser.add_argument("--skip-test", action="store_true", help="Optional, skipping tests")
    parser.add_argument("--no-benchmark", action="store_true", help="Optional, avoid benchmark prints")
    parser.add_argument("--run-all", action="store_true", help="Optional, runs all available days with the given options; if set, -d and -p are ignored")
    args = parser.parse_args()

    if args.run_all:
        solve_all_until(optimal=args.optimal, skip_test=args.skip_test, benchmark=not args.no_benchmark)
    else:
        if not 0 < args.day < 26:
            print("Day number must be between 1 and 25")
            exit()
        elif args.part not in [1, 2]:
            print("Part number must be 1 or 2")
            exit()
        else:
            print(f"Solving day {args.day} part {args.part}:\n")
            solve(day=args.day, part=args.part, optimal=args.optimal, skip_test=args.skip_test, benchmark=not args.no_benchmark)

if __name__=="__main__":
    main()