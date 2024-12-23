# My optimal solutions

## Commentary

### Day 1

Nothing to say, pretty easy puzzle to start, my solution was already quite optimal with little to no rework.

### Day 19

Searching if a combination of words matches a string can be done in `O(N * k)`, where here `N = number of towels` and `k = length of word`. This is already a pretty fast solution! It takes half a second on my Mac mini M1.

The second part can be achieved with a simple modification, keeping the same complexity: the first part is actually faster because for any of the `k` positions it stops as soon as it finds a single viable solution, and continues with the next place. Instead, here we don't want to skip and for each position we actually want to keep count of all possible words, multiplied by the previous number of possibilities.

i.e. if we have the towel design `helloworld`, and let's say there are two ways to get to `hel` (`h` + `el`, `he` + `l`), then when we find we can add another `l` to get `hell`, we will actually count it twice (once for every solution for the sentence before this second `l`).

This achieves similarly lightning fast results, around 0.6 secs on my machine.