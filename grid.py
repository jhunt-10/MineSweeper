import random
import numpy as np


class Square():

    def __init__(self, mine, x, y):
        self.mine = mine    # initializes the mine value for the square 0-9
        self.x = x
        self.y = y
        self.covered = True
        self.flag = False

    def __str__(self):
        return f"{self.mine}, ({self.x}, {self.y})"

    def flagger(self, flag):
        self.flag = flag


class Grid():
    """Grid class

    Produces numerical grid in memory with numpy

    Strictly numerical representation of the grid"""

    def __init__(self, size, num_mines):
        self.num_mines = num_mines
        self.size = size
        self.mines = np.ndarray((2, num_mines), dtype=np.dtype(int))
        self.placed = set()
        self.total_flags = 0
        # initialize the grid, a SIZE by SIZE 2-d array. The grid should be indexed self.grid[y][x] -> some Square instance at point (x,y)
        self.grid = np.ndarray((size, size), dtype=np.dtype(object))
        for row in np.nditer(np.arange(size)):  # iterate through each row
            # iterate through each column
            for col in np.nditer(np.arange(size)):

                # at each iteration (each square), check if the point is not a mine
                #   # counter for # of neighbors that are mines
                # check each neighbor that has one of 3 different changes in y value
                # exit the loop if the change for x and y is both 0 (the current square)

                # when finsihed looking at all 8 neighbors, add a reference in the 2-d array to a new Square instance with the discovered prope
                self.grid[row.item()][col.item()] = Square(
                    0, col.item(), row.item())

        # creates mines at random
        x_change = np.asarray([-1, 1, 0])
        y_change = np.asarray([-1, 1, 0])
        for i in np.nditer(np.arange(num_mines)):
            rand_x = random.randint(0, size-1)  # gives mine a random x value
            rand_y = random.randint(0, size-1)  # gives mine a random y value
            # in the 2-d array self.mines, the array at row 0 will hold the x-values for each mine
            self.mines[0][i] = rand_x
            # the array at row 1 will hold the y-values for each mine, the mines are indexed 0 through NUM_MINES - 1
            self.mines[1][i] = rand_y
            # so to acces the x and y value of a mine at a given index, this point is (self.mines[0][index], self.mines[1][index])

            # checks to make sure the randomly generated x and y have not already been given to a mine, not likely but possible
            while (self.mines[0][i], self.mines[1][i]) in self.placed:
                # if the point was given already, create new random x and y values
                rand_x = random.randint(0, size-1)
                rand_y = random.randint(0, size-1)
                self.mines[0][i] = rand_x
                self.mines[1][i] = rand_y

            # add a tuple of length 2, representing the point of the mine on the grid, to a set called self.placed
            self.placed.add((self.mines[0][i], self.mines[1][i]))
            # add a Square instance of the mine to the grid at its respective x and y
            self.grid[self.mines[1][i]][self.mines[0][i]] = Square(
                9, self.mines[0][i], self.mines[1][i])
            for x_val in np.nditer(x_change):
                for y_val in np.nditer(y_change):
                    if x_val == 0 and y_val == 0:
                        break
                    try:
                        neighbor = self.grid[self.mines[1]
                                             [i] + y_val][self.mines[0][i] + x_val]
                    except:
                        continue
                    else:
                        if self.mines[1][i] + y_val < 0 or self.mines[0][i] + x_val < 0:
                            continue
                        elif neighbor.mine != 9:
                            neighbor.mine += 1

    def get_square(self, x, y):
        """Method to return square at given x and y"""
        return self.grid[y][x]
