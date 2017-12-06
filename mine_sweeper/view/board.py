import datetime
import time
from tkinter import *
from tkinter.messagebox import *
from mine_sweeper.controller.game_board import GameBoard
from mine_sweeper.view.colors import colors
from mine_sweeper.model.node import Node


class Board:
    def __init__(self, master, size, game_board: GameBoard, controller):
        # Initialize the UI
        self.master = master
        self.size = size
        self.game_board = game_board
        # --test
        self.first_click = True
        self.controller = controller(self.game_board)
        frame = Frame(master)
        # Make the window responsive
        frame.grid(row=0, column=0, sticky=N + S + E + W)

        Grid.rowconfigure(master, 0, weight=1)
        Grid.rowconfigure(frame, 0, minsize=60, weight=1)
        Grid.columnconfigure(master, 0, weight=1)

        # Initialize the core variables
        self.flags = 0  # The number of flags
        self.boxes = []  # A list that contain all of the boxes
        self.mines = round((self.size[0] * self.size[1]) * (10/64))  # The number of mines, Identified by the game size

        # Initialize the timer label
        self.timerLBL = Label(frame, font=("Helvetica", 16))
        self.timerLBL.grid(column=0, row=0, sticky=N + S + E + W, columnspan=int(self.size[1] / 2))

        # Initialize the timer and update it every second
        self.start_time = time.time()
        self.update_timer()

        # Initialize the flag-mines label
        self.minesLBL = Label(frame, font=("Helvetica", 16),
                              text="Mines left: " + str(self.flags) + "/" + str(self.mines))
        self.minesLBL.grid(column=int(self.size[1] / 2), row=0, sticky=N + S + E + W, columnspan=int(self.size[1] / 2))

        # get graph nodes
        print(game_board.get_graph_nodes_as_list())
        # Create boxes upon the game size
        for x in range(self.size[0]):
            Grid.columnconfigure(frame, x, weight=1)
            for y in range(self.size[1]):
                i = len(self.boxes)
                Grid.rowconfigure(frame, y + 1, weight=1)
                self.boxes.append({
                    "button": Button(frame, font='TkDefaultFont 20 bold', text=" ", bg="darkgrey"),
                    "isFlagged": False
                })
                # Lay the boxes on the board
                self.boxes[i]['button'].grid(row=x + 1, column=y, sticky=N + S + E + W)
                self.boxes[i]['button'].bind('<Button-1>', self.lclick_wrapper(x, y))
                self.boxes[i]['button'].bind('<Button-3>', self.rclick_wrapper(x, y))

        # Bot function
        # self.left_click([(0, 0), (7, 7)])

    def lclick_wrapper(self, x, y):

        return lambda Button: self.lclick_handler(x, y)

    def rclick_wrapper(self, x, y):

        return lambda Button: self.rclick_handler(x, y)

    def lclick_handler(self, x, y):

        if self.first_click:
            self.first_click = False
            self.game_board.set_mines(self.game_board.get_graph_nodes_as_list()[x][y])

        value = self.game_board.get_graph_nodes_as_list()[x][y]

        print(value)
        self.game_board.discover(value)
        nodes = self.game_board.get_graph_nodes_as_list()

        for r in nodes:
            for c in r:
                print(c.__str__(), end=" | ")
            print("\n")

        # TODO belal
        changed_nodes = self.game_board.discover(value)

        if value.node_data.mine:
            pos = value.node_data.pos
            index = pos[0] * self.size[0] + pos[1]
            self.boxes[index]['button'].configure(text="*", fg="red", bg="lightgrey")
            self.gameover()
        elif value.node_data.weight >= 0:
            for changed_node in changed_nodes:
                pos = changed_node.node_data.pos
                weight = changed_node.node_data.weight
                if weight == 0:
                    weight = ' '
                index = pos[0] * self.size[0] + pos[1]
                self.boxes[index]['button'].configure(text=weight, bg="lightgrey", fg=colors[weight])
                self.boxes[index]['button'].unbind('<Button-1>')

    # Right click mouse handler
    def rclick_handler(self, x, y):
        index = x * self.size[0] + y
        # If this box not lift clicked, mark it as a flag
        if not self.boxes[index]['isFlagged']:
            self.boxes[index]['button'].configure(text="F")
            self.boxes[index]['isFlagged'] = True
            self.boxes[index]['button'].unbind('<Button-1>')
            self.flags += 1
        # If this box id flagged, unflag
        elif self.boxes[index]['isFlagged']:
            self.boxes[index]['button'].configure(text=" ")
            self.boxes[index]['isFlagged'] = False
            self.boxes[index]['button'].bind('<Button-1>', self.lclick_wrapper(x, y))
            self.flags -= 1

        # Update the flags count
        self.minesLBL.configure(text="Mines left: " + str(self.flags) + "/" + str(self.mines))


    def update_timer(self):
        timer = time.time() - self.start_time
        timerstr = datetime.datetime.fromtimestamp(timer).strftime('%M:%S')
        self.timerLBL.configure(text="Time: " + timerstr)
        self.master.after(1000, self.update_timer)

    # Show the player that he lose!
    def gameover(self):
        showinfo("Game Over", "You Lose!")
        answer = askquestion("Play again?", "Do you want to play again?")
        if answer == "yes":
            self.__init__(self.master, self.size, self.game_board, self.controller.__class__)
        else:
            self.master.destroy()

    # Show the player that he won!
    def victory(self):
        showinfo("Victory!", "You Win!")
        answer = askquestion("Play again?", "Do you want to play again?")
        if answer == "yes":
            self.__init__(self.master, self.size, self.game_board, self.controller.__class__)
        else:
            self.master.destroy()

    # Bot function
    def left_click(self, pos):

        for p in pos:
            self.lclick_handler(p[0], p[1])
