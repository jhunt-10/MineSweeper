"""
@ author James Hunt and Ethan Oullette

First created: 8/2/22

Last Modified: 8/7/22

This Module houses the gui for Mine Sweeper game.

Ethan is so bot :/

"""
import random
from tkinter import Tk, Frame, Label
import numpy as np
from PIL import Image, ImageTk
from grid import Grid, Square


SIZE = 20    # fixed size of grid

NUM_MINES = 70

TEXT_COLOR = "#000000"
COVERED_COLOR = "#00FF00"
UNCOVERED_COLOR = "#FFFFFF"
FLAG_COLOR = "#FF0000"
ZERO_COLOR = "#CCCCCC"
FLAG_PATH = "flag.jpeg"
SQUARE_SIZE = 25
WINDOW_SIZE = SIZE * SQUARE_SIZE * 2
MINE_COLORS = []


class MineSweeperGUI(Tk):
    """Mine Sweeper GUI class

    inhereits tkinter

    responsible for displaying the game"""

    class Tile(Frame):
        """Tile class

        inherits Tk.Frame

        Each square is a frame with several other custom values including, mine which descirbes if the square is a mine
        or how many it touches, covered which describes if the mine value is revealed or not, and flag which describes if the square
        has been flagged."""

        def __init__(self, master, size, x, y, flag_image, square):
            super().__init__(master, width=size, height=size, bg=COVERED_COLOR,
                             highlightbackground=TEXT_COLOR, highlightthickness=1)  # intitializes normal Tk.Frame Object with the desired parameters
            # grids the square on the window (essentially makes it appear in the window, not to be confused with self.master.grid, the 2-d array storing each Square)
            self.grid(column=x, row=y, padx=1, pady=1)
            # prevents the size of the square from changing based on the size of the text inside it
            self.grid_propagate(False)

            self.square = square
            self.x = x
            self.y = y
            if self.square.mine == 9:   # if the Square is a mine, have it show * instead of a number to represent a mine
                self.label = Label(
                    self, text="*", fg=TEXT_COLOR, bg="white", font=("Helvetica bold", ))
                self.configure(bg="#0000FF")
            elif self.square.mine == 0:
                self.label = Label(self, bg="#CCCCCC")
            else:   # if teh Square is not a mine have it show the number of mines it touches
                self.label = Label(
                    self, text=str(self.square.mine), fg=TEXT_COLOR, bg="white")
            # Label object to display the FLAG_IMAGE when right clicked
            self.flag_label = Label(self, image=flag_image)

            # event handler to handle the Button-1 event which is a noormal click on the square. THis calles the function self.click()
            self.bind("<Button-1>", lambda event: self.click())
            # event handler to show flag on right click
            self.bind("<Button-2>", lambda event: self.right_click())

        def click(self):
            """Method to handle the click event on the Square

            """
            if self.square.flag:
                pass
            elif self.square.covered:
                if self.square.flag:
                    self.flag_label.grid_forget()
                if self.square.mine == 0:
                    self.configure(bg=ZERO_COLOR)
                else:
                    self.configure(bg=UNCOVERED_COLOR)
                self.label.grid(sticky="nsew")
                self.square.covered = False
                if self.square.mine == 9:
                    self.master.explosion()
                elif self.square.mine == 0:
                    self.master.zeros(self)

        def right_click(self):
            """Method to update the flag value of a Square"""
            if self.square.covered:    # prevents flagging the square if uncovered
                if self.square.flag:
                    self.configure(bg=COVERED_COLOR)
                    self.square.flag = False
                else:
                    self.configure(bg=FLAG_COLOR)
                    self.square.flag = True

            # TODO create animation to nicely add a flag to the square or remove the flag
        def uncover(self):
            """Method to reveal the value of the square when clicked"""
            if self.square.covered:
                if self.square.flag:
                    self.flag_label.grid_forget()
                if self.square.mine == 0:
                    self.configure(bg=ZERO_COLOR)
                else:
                    self.configure(bg=UNCOVERED_COLOR)
                self.label.grid(sticky="nsew")
                self.square.covered = False

    def __init__(self):
        super().__init__()  # inititalizes all instances values for a typical TK root window

        self.flag_image = ImageTk.PhotoImage(Image.open(FLAG_PATH))

        self.title("Mine Sweeper")  # sets the title of the window
        # constrains the size of the window
        self.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")
        # create 2-d array to represnet the x and y values of each mine
        self.grid = None
        self.tiles = None
        self.start()

    def highlight(self, obj):
        for child in obj.winfo_children():
            child.configure(bg="#00FF00", fg="white")
        obj.configure(bg="#00FF00", highlightbackground="#013f28")

    def leave(self, obj):
        for child in obj.winfo_children():
            child.configure(bg="#FFFFFF", fg="black")
        obj.configure(bg="#FFFFFF", highlightbackground="#00FF00")

    def start(self):
        def click(num):
            # create new grid with num size and at least num * 2 mines
            self.play(num)
        big_frame = Frame(self, width=WINDOW_SIZE, height=WINDOW_SIZE,
                          padx=WINDOW_SIZE/4, pady=WINDOW_SIZE/4)
        big_frame.grid()
        big_frame.grid_propagate(False)
        difficulties = ["Easy", "Medium", "Hard", 14, 25, 40]
        for dif in range(3):
            difficulty_frame = Frame(
                big_frame, width=200, height=100, highlightbackground="#00FF00", highlightthickness=2, bg="white")
            difficulty_label = Label(
                difficulty_frame, text=difficulties[dif], fg="black", bg="white", font=("Helevetica", 25))
            dif_number = difficulties[dif+3]
            difficulty_label.grid()

            difficulty_frame.grid(column=dif, padx=20)
            difficulty_frame.grid_propagate(False)
            difficulty_frame.bind("<Enter>", lambda event,
                                  obj=difficulty_frame: self.highlight(obj))
            difficulty_frame.bind("<Leave>", lambda event,
                                  obj=difficulty_frame: self.leave(obj))
            difficulty_frame.bind("<Button-1>", lambda event,
                                  num=dif_number: click(num))

    def play(self, num):
        for child in self.winfo_children():
            child.destroy()
        self.grid = Grid(num, num*3)
        self.tiles = np.ndarray((num, num), dtype=np.dtype(object))
        for row in range(num):
            for col in range(num):
                self.tiles[row][col] = self.Tile(
                    self, SQUARE_SIZE, col, row, self.flag_image, self.grid.grid[row][col])
                self.tiles[row][col].grid(row=row, column=col)

    def explosion(self):
        """Method to uncover every mine in the grid if one mine is clicked on."""
        """for i in range(NUM_MINES):  # iterate through the total number of mines
            # get the x value for the mine at the given iteration
            x_val = self.mines[0][i]
            y_val = self.mines[1][i]    # get the y value for the same mine
            # uncover the square at the given x and y values
            self.grid[y_val][x_val].click()
        """
        # TODO Add animation to this method so that the mines are uncover in a cool, explosive manner

    def zeros(self, square):
        """Method to uncover the neighboring squares that are zeros when a zero is clicked"""
        visited = set()
        x_change = [-1, 1, 0]
        y_change = [-1, 1, 0]

        def bfs(node):
            if node in visited:
                return
            for row in y_change:
                for col in x_change:
                    try:
                        # make sure node is in grid
                        neighbor = self.tiles[node.y + row][node.x+col]
                    except:
                        pass
                    else:
                        if node.y + row < 0 or node.x + col < 0:
                            pass
                        elif neighbor.square.mine == 0:
                            neighbor.uncover()
                            visited.add(node)
                            bfs(neighbor.square)
                        elif neighbor.square.mine != 9:
                            neighbor.uncover()

        bfs(square.square)
