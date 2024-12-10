# Advent of Code 2024

*(This repository's structure and the base classes and utils functions were heavily inspired by [nitekat1124](https://github.com/nitekat1124/advent-of-code-2024)'s, all rights reserved.
The solutions implemented in the `solutions/naive` folder I came up with without looking at other people's code.)*

My personal solutions to [Advent of Code 2024](https://adventofcode.com/2024/), implemented in Python 3.

## Solutions

![](https://img.shields.io/badge/days_📅-9-blue)
![](https://img.shields.io/badge/stars_⭐-18-yellow)
![](https://img.shields.io/badge/half_stars_🌗-0-white)

For each day, a single ⭐ is listed if only the first part of the puzzle was solved, and both ⭐⭐ if both parts are solved correctly.

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

### What is the difference between "naive" and "optimal" solutions?

Under the `solutions/naive` folder I list the solution I came up on the spot, while trying to solve the daily Advent of Code challenge, without any particular refactoring or optimization, just some minor cleanup.

Under the `solutions/optimal` folder I will list progressively some better and optimized solution, possibly the best among the ones I find online, if not the actually optimal ones.

Both folder have a dedicated `README.md` with some personal commentary on specific solutions where I find it interesting to document my thought process, or the credits to an optimal solution I found online.

## How to run

```
usage: runner.py [-h] [-d day_number] [-p part_number] [--optimal] [--skip-test] [--no-benchmark] [--run-all]

Bulk runner of gabxcos' Advent of Code 2024 solutions

options:
  -h, --help            show this help message and exit
  -d day_number, --day day_number
                        Required, day number of the AoC event
  -p part_number, --part part_number
                        Required, part number of the day of the AoC event
  --optimal             Optional, use the intended optimal solution instead of the one I actually came up with
  --skip-test           Optional, skipping tests
  --no-benchmark        Optional, avoid benchmark prints
  --run-all             Optional, runs all available days with the given options; if set, -d and -p are ignored
```