# Advent of Code 2024

*(This repository's structure and the base classes and utils functions were heavily inspired by [nitekat1124](https://github.com/nitekat1124/advent-of-code-2024)'s, all rights reserved.
The solutions implemented in the `solutions/naive` folder I came up with without looking at other people's code.)*

My personal solutions to [Advent of Code 2024](https://adventofcode.com/2024/), implemented in Python 3.

## Solutions

![](https://img.shields.io/badge/days_completed_📅-14-blue)
![](https://img.shields.io/badge/stars_⭐-28-yellow)
![](https://img.shields.io/badge/half_stars_🌗-0-white)

For each day, a single ⭐ is listed if only the first part of the puzzle was solved, and both ⭐⭐ if both parts are solved correctly.
A 🌠 signifies that consulting external resources was required in order to solve a part (usually out of frustration for not finding a solution by myself for several hours or days).

| Day | Naive Solutions | Optimal Solutions |
|-----|:---------------:|:-----------------:|
| 01  |        ⭐⭐       |         ⭐⭐        |
| 02  |        ⭐⭐       |         --        |
| 03  |        ⭐⭐       |         --        |
| 04  |        ⭐⭐       |         --        |
| 05  |        ⭐⭐       |         --        |
| 06  |        ⭐⭐       |         --        |
| 07  |        ⭐⭐       |         --        |
| 08  |        ⭐⭐       |         --        |
| 09  |        ⭐⭐       |         --        |
| 10  |        ⭐⭐       |         --        |
| 11  |        ⭐⭐       |         --        |
| 12  |        ⭐🌠       |         --        |
| 13  |        ⭐⭐       |         --        |
| 14  |        ⭐⭐       |         --        |

### What is the difference between "naive" and "optimal" solutions?

Under the `solutions/naive` folder I list the solution I came up on the spot, while trying to solve the daily Advent of Code challenge, without any particular refactoring or optimization, just some minor cleanup.

Under the `solutions/optimal` folder I will list progressively some better and optimized solution, possibly the best among the ones I find online, if not the actually optimal ones.

Both folder have a dedicated `README.md` with some personal commentary on specific solutions where I find it interesting to document my thought process, or the credits to an optimal solution I found online.

## How to run

### Preparing the puzzles

For each day you intend to test my solutions against, you need to provide manually the puzzle inputs (see why [here](https://www.reddit.com/r/adventofcode/comments/zdz8qa/license_of_the_input_data/)).

In order to do so, the plaintext of the sample input and of your personal input need to be put respectively in two distinct files, in `inputs/test/09` and `inputs/puzzle/09` assuming you're testing just day 9 (in general, the file name is the zero-fill at two positions of a given day).

### Usage

This is the general usage helper, provided by Python's `argparse`:

```
usage: runner.py [-h] [-d day_number] [-p part_number] [--optimal] [--skip-test] [--no-elapsed] [--run-all]

Bulk runner of gabxcos' Advent of Code 2024 solutions

options:
  -h, --help            show this help message and exit
  -d day_number, --day day_number
                        Required, day number of the AoC event
  -p part_number, --part part_number
                        Required, part number of the day of the AoC event
  --optimal             Optional, use the intended optimal solution instead of the one I actually came up with
  --skip-test           Optional, skipping tests
  --no-elapsed        Optional, avoid elapsed prints
  --debug               Optional, add debug prints and computations, if available
  --run-all             Optional, runs all available days with the given options; if set, -d and -p are ignored
```

### Examples

- running for part 2 of day 9:

    ```python -m runner -d 9 -p 2```

- running all available naive solutions:

    ```python -m runner --run-all```

- running all available optimal solutions:

    ```python -m runner --optimal --run-all```

- running all available naive solutions without testing sample inputs:

    ```python -m runner --run-all --skip-test```

- running all available naive solutions without measuring elapsed time:

    ```python -m runner --run-all --no-elapsed```

- running all available naive solutions with debug computations:

    ```python -m runner --run-all --debug```