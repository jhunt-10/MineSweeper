"""
@ author James Hunt and Ethan Oullette

First created: 8/2/22

Last Modified: 8/7/22

This Module houses the gui for Mine Sweeper game.

Ethan is so bot :/

"""
import random
from tkinter import Tk, Frame, Label, StringVar
import numpy as np
from PIL import Image, ImageTk
#from model import Grid, Square
from threading import Thread
from collections import deque
import datetime
import time


SIZE = 20    # fixed size of grid

NUM_MINES = 70

TEXT_COLOR = "#000000"
COVERED_COLOR = "#00FF00"
UNCOVERED_COLOR = "#FFFFFF"
FLAG_COLOR = "#FF0000"
ZERO_COLOR = "#CCCCCC"
FLAG_PATH = "flag.jpeg"
BOMB_PATHS = ["bombc3.png", "bomb2.png", "bomb1.png"]
GREEN1 = "#20B718"
GREEN2 = "#28E41E"
MENU_COLOR = "#134B00"
TAN1 = "#C3BA8C"
TAN2 = "#DFD59F"
HIGHLIGHT_GREEN = "#68FF60"
HIGHLIGHT_TAN = "#F4E9AF"
DARK_TEXT = "#3B448C"
LIGHT_TEXT = "#6E7CEE"
SQUARE_SIZE = 9
WINDOW_SIZE = 900
MINE_COLORS = ["#0A48FB", "#34781C", "#CA0000",
               "#8A09DD", "#7D0000", "#09EFE3", "#000000", "#888888"]


class MineSweeperGUI(Tk):
    """Mine Sweeper GUI class

    inhereits tkinter

    responsible for displaying the game

    house visual representation of the grid"""

    def __init__(self, driver):
        super().__init__()  # inititalizes all instances values for a typical TK root window

        # assign driver for instance of the gui
        self.driver = driver

        self.flag_image = ImageTk.PhotoImage(Image.open(FLAG_PATH))
        self.bomb_image = None

        self.title("Mine Sweeper")  # sets the title of the window
        # constrains the size of the window
        self.geometry(f"{WINDOW_SIZE+400}x{WINDOW_SIZE}")
        # creates body variable which is initialized to a Frame that wil be parent to the everything in the main window
        self.body = Frame(self, bg=MENU_COLOR)
        self.body.grid()

        # establishes variable grid_frame which at some point will be assigned a Frame object that will be the parent object to each tile in the grid
        self.grid_frame = None
        self.flag_place = 0
        self.start_page()

    def highlight_button(self, obj):
        """View method to change the background color of a button (highlight it) when entered"""
        for child in obj.winfo_children():
            child.configure(bg=TAN2, fg=LIGHT_TEXT)
        obj.configure(bg=TAN2, highlightbackground=TAN1)

    def unhighlight_button(self, obj):
        """View method to change the background color of a button (unhighlight it) when left"""
        for child in obj.winfo_children():
            child.configure(bg=TAN1, fg=DARK_TEXT)
        obj.configure(bg=TAN1, highlightbackground=TAN2)

    def start_page(self):
        """View method to display all tkinter objects for the start up"""
        # destroys any previous tkinter objects/ widgets that existed in the body
        for child in self.body.winfo_children():
            child.destroy()

        # creates Frame object that will be the parent to every
        self.grid_frame = Frame(self.body, bg=MENU_COLOR)

        self.grid_frame.grid()

        # creates background of green checkered squares
        for row in range(6):
            for col in range(6):
                if (col + row) % 2 == 0:
                    color = GREEN1
                else:
                    color = GREEN2
                Frame(self.grid_frame, width=170, height=170, bg=color).grid(
                    row=row, column=col)

        difficulties = ["EASY", "MEDIUM", "HARD", 200, 352, 550]
        # difficulty label for each button to display and positions to place the button frames on the background

        # iterates thru the 3 different difficulties, 0 thru 2
        for dif in range(3):
            # creates a frame to display the varying difficulties
            holder = Frame(self.grid_frame, bg=TAN1, highlightbackground=TAN2,
                           highlightthickness=4, relief="ridge")

            # creates a label to display the text for each difficulty
            difficulty_label = Label(
                holder, text=difficulties[dif], fg=DARK_TEXT, bg=TAN1, font=("Poppins bold", 38))

            # shows the label
            difficulty_label.grid(column=1, padx=10, pady=15)

            # grids the frame with the lowest difficulty being leftmost and highest rightmost
            holder.place(x=difficulties[dif+3], y=400)

            # events that changes the color of the frame when the mouse enters
            # because these next 2 events do not effect the model, they call functions in the view
            # the contros for these are strictly related to the view so there is no need to call a function outside of the view
            holder.bind("<Enter>", lambda event,
                        obj=holder: self.highlight_button(obj))
            holder.bind("<Leave>", lambda event,
                        obj=holder: self.unhighlight_button(obj))

            # event that handles click on one of three difficulty buttons
            # this event effects both the model and the view
            # the model should be initialized after this event and a new page in the view called play should be displayed
            # because the event requires driving multiple facets of the program, function of the driver is called-
            holder.bind("<Button-1>", lambda event,
                        dif_num=dif: self.driver.play(dif_num))

            for child in holder.winfo_children():
                binds = list(child.bindtags())
                binds.insert(1, holder)
                child.bindtags(tuple(binds))

        print("got here")

    def play_screen(self):
        self.menu_frame = Frame(self.body, height=900,
                                width=200, bg=MENU_COLOR)
        self.menu_frame.grid(column=1)
        print("end of play screen")

    """
    def update_flags(self, increment):
        self.flag_place += increment
        self.flags.set(str(self.flag_place))

    def change_time(self, time):
        self.timer_view.set(str(time))

    def display_board(self, grid):
        pass
        # iterates through grid
        # displays Tile tkinter object at each iteration

    def play(self, num, dif_number):
        # cpu clocker to test speed of initialization
        start_time = time.perf_counter_ns()
        for child in self.winfo_children():
            child.destroy()     # destory every part of the view from the start screen
        # sets the bomb image depending on square size
        self.bomb_image = ImageTk.PhotoImage(
            Image.open(BOMB_PATHS[dif_number]))
        self.size = num
        self.body = Frame(self, bg=MENU_COLOR)
        self.grid_frame = Frame(self.body, bg=MENU_COLOR)
        self.flags = StringVar(self)

        self.timer_view = StringVar(self)
        self.timer_view.set(0.0)
        self.menu_frame = Frame(
            self.body, bg=MENU_COLOR, width=200, height=900)
        self.flags_label = Label(
            self.menu_frame, text="Flags Placed:",  font=("Poppins", 23), fg=LIGHT_TEXT, bg=MENU_COLOR)
        self.flags_number = Label(
            self.menu_frame,  font=("Poppins", 23), fg=LIGHT_TEXT, textvariable=self.flags, bg=MENU_COLOR)
        self.tiemr_view_label = Label(self.menu_frame,  font=(
            "Poppins", 23), fg=LIGHT_TEXT, textvariable=self.timer_view, bg=MENU_COLOR)
        self.flags_label.grid(pady=20)
        self.flags_number.grid(column=1, padx=10, pady=20)
        self.body.grid()
        self.grid_frame.grid(column=0, row=0, sticky="nw")
        self.menu_frame.grid(column=1, row=0)
        self.menu_frame.grid_propagate(False)
        if dif_number == 0:
            self.sq_size = 50
        else:
            self.sq_size = SQUARE_SIZE*(
                3-dif_number) + 10

        for row in range(num):
            for col in range(num):
                if dif_number == 0:
                    dif_number = -2
                self.tiles[row][col] = self.Tile(
                    self.grid_frame, self.sq_size, col, row, self.flag_image, self.grid.grid[row][col], dif_number)
                self.tiles[row][col].grid(row=row, column=col)

        print("time since epoch", (time.perf_counter_ns() - start_time)/1000000000)

    def explosion(self, mines):
        if len(mines) == 0:
            self.update()
            return
        # add unbinding feature so you cannot click on anything when this is running
        # iterate through the total number of mines
        for i in mines:
            # get the x value for the mine at the given iteration
            x_val = self.grid.mines[0][i]
            # get the y value for the same mine
            y_val = self.grid.mines[1][i]
            self.tiles[y_val][x_val].uncover()
            self.tiles[y_val][x_val]
            self.update()

            self.after(150)
        return

        # TODO Add animation to this method so that the mines are uncover in a cool, explosive manner

    def zeros(self, square):
        visited = set()
        x_change = [-1, 1, 0]
        y_change = [-1, 1, 0]
        queue = deque()
        queue.append(square.square)
        while len(queue) > 0:
            node = queue.pop()
            self.tiles[node.y][node.x].uncover()
            self.update()
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
                            visited.add(node)
                            if neighbor.square not in visited:
                                queue.append(neighbor.square)
                        elif neighbor.square.mine != 9:
                            neighbor.uncover()
            self.after(9)"""


class Tile(Frame):
    """Tile class

    inherits Tk.Frame

    Each square is a frame with several other custom values including, mine which descirbes if the square is a mine
    or how many it touches, covered which describes if the mine value is revealed or not, and flag which describes if the square
    has been flagged."""

    def __init__(self, master, size, x, y, driver):
        # intitializes normal Tk.Frame Object with the size x size dimensions
        super().__init__(master, width=size, height=size)

        self.driver = driver

        self.x = x
        self.y = y

        # event handler to handle the Button-1 event which is a noormal click on the square. THis calles the function self.click()
        self.bind("<Button-1>", lambda event, x=self.x,
                  y=self.y: self.driver.square_click(x, y))
        # event handler to show flag on right click
        self.bind("<Button-2>", lambda event, x=self.x,
                  y=self.y: self.driver.square_right_click(x, y))

        self.bind("<Enter>", lambda event, x=self.x,
                  y=self.y: self.driver.square_highlight(x, y))

        self.bind("<Leave>", lambda event, x=self.x,
                  y=self.y: self.driver.square_unhighlight(x, y))

    def set_bg_color(self, bg_color):
        """Method to change the background color of the square, set ot parameter bg_color"""
        self.configure(bg=bg_color)

        for child in self.winfo_children():
            child.configure(bg=bg_color)

    def uncover_safe(self, value, text_color, bg_color, text_size):
        """Method to uncover a safe square
        Takes parameters value, which is number to display, bg_color which is the color to display, text_size, and text_color"""
        Frame(self, width=4, height=4, bg=bg_color).grid(
            row=1, column=0)   # grids a positioning frame so the label is centered
        Label(
            self, text=str(value), fg=text_color, bg=bg_color, font=("Helvetica bold", text_size)).grid(column=1, row=0)

        # updates binds so that if a child of the tile is clicked it calls the handler for the tile itself
        for child in self.winfo_children():
            binds = list(child.bindtags())
            binds.insert(1, self)
            child.bindtags(tuple(binds))

    def uncover_zero(self, bg_color):
        """Method to uncover a square that is not touching any mines
        Configures the background color of the square to the parameter bg_color"""
        self.configure(bg=bg_color)

    def uncover_mine(self, mine_image, bg_color):
        """Method to uncover a square that is a mine
        Displays the image mine_image, with background bg_color"""
        Label(self, image=mine_image, bg=bg_color).grid()


# likely will not need this click function but keeping the code here to reference for creating function in model.py

    """def click(self):
        if self.square.flag:
            pass
        elif self.square.covered:
            self.configure(bg=self.uncovered_color)

            if self.square.mine != 9 and self.square.mine != 0:
                Frame(self, width=4, height=10,  bg=self.uncovered_color).grid(
                    row=1, column=0)
            self.label.grid(sticky="nsew", row=0, column=1)
            self.square.covered = False
            if self.square.mine == 9:
                self.master.master.master.explosion(
                    list(range(self.master.master.master.grid.num_mines)))
            elif self.square.mine == 0:
                self.master.master.master.zeros(self)
        elif self.square.mine > 0:
            # part of click that handles a click on an uncovered tile
            # looks at each neighbor to that tile and tallies the total number of flagged neighbors
            # if the total number of flagged neighbors is equal to the mine number of the tile the each neighbor of the tile is revelead
            x_change = [-1, 1, 0]
            y_change = [-1, 1, 0]
            neighbors = []
            flags = 0
            for row in y_change:
                for col in x_change:
                    if col == 0 and row == 0:
                        break
                    try:
                        # make sure node is in grid
                        neighbor = self.master.master.master.tiles[self.y +
                                                                   row][self.x+col]
                    except:
                        # index error caught, do nothing
                        pass
                    else:
                        if self.y + row < 0 or self.x + col < 0:
                            pass
                        elif neighbor.square.flag:
                            flags += 1
                        else:
                            neighbors.append(neighbor)
            if flags == self.square.mine:
                for neigh in neighbors:
                    if neigh.square.covered:
                        neigh.reveal()"""


# likely will delete all of these methods but keeping them for reference for model.py

    """

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
        self.square
        if self.square.covered:    # prevents flagging the square if uncovered
            if self.square.flag:
                self.configure(bg=self.covered_color)
                self.square.flagger(False)
                self.master.master.master.grid.total_flags -= 1
                self.master.master.master.update_flags(-1)
            else:
                self.configure(bg=FLAG_COLOR)
                self.square.flagger(True)
                self.master.master.master.grid.total_flags += 1
                self.master.master.master.update_flags(1)

        # TODO create animation to nicely add a flag to the square or remove the flag

    def reveal(self):
        self.configure(bg=self.uncovered_color)
        if self.square.mine != 9 and self.square.mine != 0:
            Frame(self, width=4, height=self.size/6).grid(row=1, column=0)
        elif self.square.mine == 9:
            self.master.master.master.explosion(
                list(range(self.master.master.master.grid.num_mines)))
        elif self.square.mine == 0:
            self.master.master.master.zeros(self)
        self.label.grid(sticky="nsew", row=0, column=1)
        self.square.covered = False

    def uncover(self):
        if self.square.covered:
            if self.square.flag:
                self.flag_label.grid_forget()
            self.configure(bg=self.uncovered_color)
            if self.square.mine != 9 and self.square.mine != 0:
                Frame(self, width=4, height=self.size /
                      6).grid(row=1, column=0)
            self.label.grid(sticky="nsew", row=0, column=1)
            self.square.covered = False

    """
