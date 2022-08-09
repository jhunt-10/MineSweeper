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
BOMB_PATH = "bomb.jpeg"
GREEN1 = "#20B718"
GREEN2 = "#28E41E"
TAN1 = "#C3BA8C"
TAN2 = "#DFD59F"
HIGHLIGHT_GREEN = "#68FF60"
HIGHLIGHT_TAN = "#F4E9AF"
SQUARE_SIZE = 14
WINDOW_SIZE = 900
MINE_COLORS = ["#0A48FB", "#1DD300", "#CA0000",
               "#8A09DD", "#7D0000", "#09EFE3", "#000000", "#888888"]


class MineSweeperGUI(Tk):
    """Mine Sweeper GUI class

    inhereits tkinter

    responsible for displaying the game

    house visual representation of the grid"""

    class Tile(Frame):
        """Tile class

        inherits Tk.Frame

        Each square is a frame with several other custom values including, mine which descirbes if the square is a mine
        or how many it touches, covered which describes if the mine value is revealed or not, and flag which describes if the square
        has been flagged."""

        def __init__(self, master, size, x, y, flag_image, square, dif_num):
            if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
                color = GREEN1
                ucolor = TAN1
            else:
                color = GREEN2
                ucolor = TAN2
            super().__init__(master, width=size, height=size, bg=color,
                             highlightbackground=TEXT_COLOR, highlightthickness=0)  # intitializes normal Tk.Frame Object with the desired parameters
            # grids the square on the window (essentially makes it appear in the window, not to be confused with self.master.grid, the 2-d array storing each Square)
            self.grid(column=x, row=y)
            # prevents the size of the square from changing based on the size of the text inside it
            self.grid_propagate(False)
            self.covered_color = color
            self.uncovered_color = ucolor

            self.square = square
            self.x = x
            self.y = y
            if self.square.mine == 9:   # if the Square is a mine, have it show * instead of a number to represent a mine
                self.label = Label(
                    self, image=master.bomb_image)  # TODO add functionality to change bomb image size based on difficluty, do this not here though, just change master.bomb_image
                self.label.configure(bg="#0000FF")
            elif self.square.mine == 0:
                self.label = Label(self, bg=self.uncovered_color)
            else:   # if teh Square is not a mine have it show the number of mines it touches
                self.label = Label(
                    self, text=str(self.square.mine), fg=MINE_COLORS[self.square.mine-1], bg=self.uncovered_color, font=("Helvetica bold", 15*(3-dif_num)))
            # Label object to display the FLAG_IMAGE when right clicked
            self.flag_label = Label(self, image=flag_image)

            # event handler to handle the Button-1 event which is a noormal click on the square. THis calles the function self.click()
            self.bind("<Button-1>", lambda event: self.click())
            # event handler to show flag on right click
            self.bind("<Button-2>", lambda event: self.right_click())

            self.bind("<Enter>", lambda event: self.highlight())

            self.bind("<Leave>", lambda event: self.leave())

        def click(self):
            """Method to handle the click event on the Square

            """
            if self.square.flag:
                pass
            elif self.square.covered:
                if self.square.flag:
                    self.flag_label.grid_forget()
                self.configure(bg=self.uncovered_color)

                if self.square.mine != 9 and self.square.mine != 0:
                    Frame(self, width=4, bg=self.uncovered_color).grid(
                        row=1, column=0)
                self.label.grid(sticky="nsew", row=0, column=1)
                self.square.covered = False
                if self.square.mine == 9:
                    self.master.explosion()
                elif self.square.mine == 0:
                    self.master.zeros(self)

        def highlight(self):
            if self.square.covered and not self.square.flag:
                self.configure(bg=HIGHLIGHT_GREEN)
            elif not self.square.covered and self.square.mine != 0:
                self.configure(bg=HIGHLIGHT_TAN)
                for child in self.winfo_children():
                    child.configure(bg=HIGHLIGHT_TAN)

        def leave(self):
            if self.square.covered and not self.square.flag:
                self.configure(bg=self.covered_color)
            elif not self.square.covered and self.square.mine != 0:
                self.configure(bg=self.uncovered_color)
                for child in self.winfo_children():
                    child.configure(bg=self.uncovered_color)

        def right_click(self):
            """Method to update the flag value of a Square"""
            if self.square.covered:    # prevents flagging the square if uncovered
                if self.square.flag:
                    self.configure(bg=self.covered_color)
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
                self.configure(bg=self.uncovered_color)
                if self.square.mine != 9 and self.square.mine != 0:
                    Frame(self, width=4).grid(row=1, column=0)
                self.label.grid(sticky="nsew", row=0, column=1)
                self.square.covered = False

    def __init__(self):
        super().__init__()  # inititalizes all instances values for a typical TK root window

        self.flag_image = ImageTk.PhotoImage(Image.open(FLAG_PATH))
        self.bomb_image = ImageTk.PhotoImage(Image.open(BOMB_PATH))

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
        def click(num, dif_num):
            # create new grid with num size and at least num * 2 mines
            self.play(num, dif_num)
        big_frame = Frame(self, width=WINDOW_SIZE, height=WINDOW_SIZE,
                          padx=WINDOW_SIZE/5, pady=WINDOW_SIZE/5)
        big_frame.grid()
        big_frame.grid_propagate(False)
        difficulties = ["Easy", "Medium", "Hard", 15, 30, 45]
        for dif in range(3):
            difficulty_frame = Frame(
                big_frame, width=150, height=100, highlightbackground="#00FF00", highlightthickness=2, bg="white")
            difficulty_label = Label(
                difficulty_frame, text=difficulties[dif], fg="black", bg="white", font=("Helevetica", 25))
            dif_number = difficulties[dif+3]
            difficulty_label.grid()

            difficulty_frame.grid(column=dif, padx=20, row=0)
            difficulty_frame.grid_propagate(False)
            difficulty_frame.bind("<Enter>", lambda event,
                                  obj=difficulty_frame: self.highlight(obj))
            difficulty_frame.bind("<Leave>", lambda event,
                                  obj=difficulty_frame: self.leave(obj))
            difficulty_frame.bind("<Button-1>", lambda event,
                                  num=dif_number, dif_num=dif: click(num, dif_num))

    def play(self, num, dif_number):
        for child in self.winfo_children():
            child.destroy()
        self.grid = Grid(num, num*3*(dif_number+1))
        self.tiles = np.ndarray((num, num), dtype=np.dtype(object))
        for row in range(num):
            for col in range(num):
                self.tiles[row][col] = self.Tile(
                    self, SQUARE_SIZE*(3-dif_number), col, row, self.flag_image, self.grid.grid[row][col], dif_number)
                self.tiles[row][col].grid(row=row, column=col)

    def explosion(self):
        """Method to uncover every mine in the grid if one mine is clicked on."""
        for i in range(self.grid.num_mines):  # iterate through the total number of mines

            # get the x value for the mine at the given iteration
            x_val = self.grid.mines[0][i]
            # get the y value for the same mine
            y_val = self.grid.mines[1][i]

            # uncover the square at the given x and y values
            self.tiles[y_val][x_val].uncover()

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
