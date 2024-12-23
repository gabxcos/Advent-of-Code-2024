# My naive solutions

## Commentary

### Day 11

This is the first day that possibly gave me a real challenge - all due to `mental block`!

As you can see, the solution for part 1 is somewhat brute-force, working on the given input itself, while the part 2 solution required me to use a dictionary as a base, because otherwise the exponential growth breaks the program pretty quickly (on my M1 Mac Mini, a length of 40 blinks is already quite long!).

The optimized solution for part 2 takes half the time on 75 iterations, than part 1 on 25.

Problem is: this is a simple solution to come up with, but it took me **the whole day** to figure out for some reason! Just happy to see I wasn't the only one.

This is surely telling on how much our mental state matters, as there are no simple or hard problems, but just clear and occluded minds!

As a side note, the stress for not figuring out a rapid solution led me to some very creative approaches early in the morning!

If you run day 11 part 1 with the `--debug` flag, you'll see I even plotted the points on `matplotlib` and tried to come up with a predicted value by fitting an exponential function.

I won't tell you the final solution (just clone the repo and run it, or try coming up with your code 😜), but I will tell you how close I got with `scipy.optimize.curve_fit`: the final solution is in the 14th order of magnitude, and so is `curve_fit`'s prediction, but it misses by an error of around `10^12` (meaning, the first two digits are correct but the third differs by 1), or around 0.33% of the actual result.

Now, that means that I could try 10^12 different values (a thousand billions) and still not hit the actual result!

Considering there is a 60 seconds cooldown between attempts (assuming no other anti-spam measures), that would take around **1.9 million years**!

Just goes to show how there is no easy way out to solving these puzzles...

### Day 19

This is the first day after the first I was able to come up with an optimal solution at first try!

Luckily I already knew the optimal solution from the base problem (searching if any combination of words matches a string), and adapting it in order to keep a count of all intermediate solutions (instead of a simple True / False) was also quite easy!