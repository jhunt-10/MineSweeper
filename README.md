# MineSweeper

Bot ideas:

Goal: Solely winning.

- Game start
- Find confirmed mines -> flag
- Consider when an uncovered tile is "satisfied," 
    i.e. # of neighboring flags = # of neighboring mines -> clear neighbors
- Deduction:  Ex. If an unsatisfied 1 has two uncovered neighbors, 
              and a 1 with three or more uncovered neighbors shares those two neighbors, 
              then clear all the remaining neighbors.
- No deductions to be made? -> 
      Resort to probability:
        - Odds of randomly selected neighbor being a mine.
        - How many mines are left?
        - Also consider... Will uncovering neighbor x give me confirmed mines/deduction possibilites for squares y, z, etc.?
