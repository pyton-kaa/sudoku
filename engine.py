from tkinter import *


numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
rows = []
cols = []
squares = {}
for r in range(9):
    rows.append([])
    for c in range(9):
        rows[r].append((r, c))
for c in range(9):
    cols.append([])
    for r in range(9):
        cols[c].append((r, c))
for x in range(3):
    for y in range(3):
        square = []
        for r in range(3):
            for c in range(3):
                square.append((3 * x + r, 3 * y + c))
        squares[(x, y)] = square


def relatives(row, col):
    list = []
    for r in range(9):
        if r == row:
            continue
        else:
            list.append((r, col))
    for c in range(9):
        if c == col:
            continue
        else:
            list.append((row, c))
    for r in [3 * (row // 3), 3 * (row // 3) + 1, 3 * (row // 3) + 2]:
        for c in [3 * (col // 3), 3 * (col // 3) + 1, 3 * (col // 3) + 2]:
            if r == row:
                continue
            elif c == col:
                continue
            else:
                list.append((r, c))
    return list


def get_values(board):
    cells = []
    nonzero_cells = []
    for row in range(9):
        cells.append([])
        for col in range(9):
            v = board.buttons[(row, col)].value
            cells[row].append(v)
            if v != 0:
                nonzero_cells.append((row, col))
    puzzle = [cells, nonzero_cells]
    return puzzle


def check(puzzle):
    conflicts = []
    for coords in puzzle[1]:
        for pair in relatives(coords[0], coords[1]):
            if puzzle[0][pair[0]][pair[1]] == puzzle[0][coords[0]][coords[1]]:
                conflicts.append(pair)
    return conflicts


class Solver:
    def __init__(self, board):
        self.puzzle = None
        self.board = board
        self.changed1 = 1
        self.changed2 = 0
        self.conflict = 0
        self.last_row = 0
        self.last_col = 0
        self.domain = None

    def iterate1(self):
        self.changed1 = 0
        for row in range(9):
            for col in range(9):
                if (row, col) in self.puzzle[1]:
                    continue
                else:
                    if self.puzzle[0][row][col] == 0:
                        self.puzzle[0][row][col] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                        self.changed1 = 2
                    elif self.puzzle[0][row][col] in range(1, 10):
                        continue
                    else:
                        for pair in relatives(row, col):
                            val = self.puzzle[0][pair[0]][pair[1]]
                            if val in self.puzzle[0][row][col]:
                                self.puzzle[0][row][col].remove(val)
                        if len(self.puzzle[0][row][col]) == 1:
                            self.puzzle[0][row][col] = self.puzzle[0][row][col][0]
                            self.puzzle[1].append((row, col))
                            self.changed1 = 1
                            self.last_row = row
                            self.last_col = col
                            break
            if self.changed1 == 1:
                break
        if len(check(self.puzzle)) > 0:
            self.conflict = 1

    def count_values(self, domain):
        appearance = {}
        for value in range(1, 10):
            count = 0
            places = [0]
            for pair in domain:
                l = self.puzzle[0][pair[0]][pair[1]]
                if l in range(10):
                    continue
                elif value in l:
                    count += 1
                    places.append(pair)
            places[0] = count
            appearance[value] = places
        return appearance

    def catch_single(self):
        for row in rows:
            appearance = self.count_values(row)
            for value in range(1, 10):
                if appearance[value][0] == 1:
                    self.domain = row
                    return [appearance[value][1], value]

        for col in cols:
            appearance = self.count_values(col)
            for value in range(1, 10):
                if appearance[value][0] == 1:
                    self.domain = col
                    return [appearance[value][1], value]

        for square in squares.values():
            appearance = self.count_values(square)
            for value in range(1, 10):
                if appearance[value][0] == 1:
                    self.domain = square
                    return [appearance[value][1], value]
        return []

    def iterate2(self):
        self.changed2 = 0
        item = self.catch_single()
        if len(item) > 1:
            self.puzzle[0][item[0][0]][item[0][1]] = item[1]
            self.puzzle[1].append(item[0])
            self.last_row = item[0][0]
            self.last_col = item[0][1]
            self.changed2 = 1
            self.changed1 = 1
            if len(check(self.puzzle)) > 0:
                self.conflict = 1


def choose_value(win, buttons, r, c, value):
    buttons[(r, c)].value = value
    if value in range(1, 10):
        fgcolor = "black"
        bgcolor = "white"
    else:
        bgcolor = "#EEEEEE"
        fgcolor = "#444444"
    buttons[(r, c)].configure(text=f"{value}", fg=fgcolor, bg=bgcolor)
    win.destroy()


def change_value(buttons, r, c):
    buttons[(r, c)].configure(bg="#DDDDFF", fg="#4444FF")
    choice = Toplevel()
    choice.title("Choose the value for the selected cell")
    val = IntVar(choice)
    choices = []
    for i in range(10):
        choices.append(Radiobutton(choice, text=f"{i}", value=i, variable=val))
    for button in choices:
        button.pack()
    ok = Button(
        choice,
        text="OK",
        command=lambda: choose_value(choice, buttons, r, c, val.get()),
    )
    ok.pack()


commands = {}
for row in range(9):
    for col in range(9):

        def ch(win, buttons, value):
            buttons[(row, col)].value = value
            if value in range(1, 10):
                fgcolor = "black"
                bgcolor = "white"
            else:
                bgcolor = "#EEEEEE"
                fgcolor = "#444444"
            buttons[(row, col)].configure(text=f"{value}", fg=fgcolor, bg=bgcolor)
            win.destroy()

        def fun(buttons):
            buttons[(row, col)].configure(bg="#DDDDFF", fg="#4444FF")
            choice = Toplevel()
            choice.title("Choose the value for the selected cell")
            val = IntVar(choice)
            choices = []
            for i in range(10):
                choices.append(Radiobutton(choice, text=f"{i}", value=i, variable=val))
            for button in choices:
                button.pack()
            ok = Button(
                choice, text="OK", command=lambda: ch(choice, buttons, val.get())
            )
            ok.pack()

        commands[(row, col)] = fun
