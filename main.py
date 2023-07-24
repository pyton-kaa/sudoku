from tkinter import *
from layout import *


CELL_SIZE = 50

window = Tk()
window.title("Easy Sudoku Solver")
window.minsize(width=9 * CELL_SIZE + 210, height=9 * CELL_SIZE + 10)

IMAGE = PhotoImage(file="blank1.png")

board = Board(CELL_SIZE, IMAGE)
board.draw()

solver = Solver(board)

menu = Menu(solver)
menu.create()


window.mainloop()
