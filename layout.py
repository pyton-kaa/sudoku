from tkinter import *
from tkinter import messagebox
from engine import *

dfont = ("Arial", 22, "normal")
fgrey = "#444444"
bgrey = "#DDDDDD"
fblue = "#0000DD"
bblue = "#DDDDFF"
fred = "#DD0000"
bred = "#FFDDDD"
fgreen = "#00DD00"
bgreen = "#DDFFDD"
fyellow = "#777700"
byellow = "#FFFFBB"


class Cell(Button):
    def __init__(self, size, row, col, image):
        super().__init__()
        self.size = size
        self.value = 0
        self.x = size * col + 8
        self.y = size * row + 8
        self.image = image

    def create(self):
        self.configure(
            image=self.image,
            text="",
            font=dfont,
            compound="c",
            bd=0,
            width=self.size - 9,
            height=self.size - 9,
            bg=bgrey,
            fg=fgrey,
            command=self.change_value,
        )
        self.place(x=self.x, y=self.y)

    def set_value(self, value):
        self.value = value
        if value == 0:
            self.configure(text="", bg=bgrey, fg=fgrey)
        else:
            self.configure(text=f"{value}", bg="white", fg="black")

    def choose_value(self, win, value):
        self.set_value(value)
        win.destroy()

    def change_value(self):
        self.configure(bg=bblue, fg=fblue)
        choice = Toplevel()
        choice.title("Choose the value for the selected cell")
        # val = IntVar(choice)
        valuebuttons = []
        for i in range(9):
            valuebuttons.append(
                Button(
                    choice,
                    text=f"{i+1}",
                    width=3,
                    command=lambda i=i: self.choose_value(choice, i + 1),
                    font=dfont,
                )
            )
        emptybutton = Button(
            choice,
            text="Empty cell",
            width=14,
            command=lambda: self.choose_value(choice, 0),
            font=("Arial", 18, "normal"),
        )
        for i in range(9):
            valuebuttons[i].grid(row=i // 3, column=i % 3, padx=5, pady=5)
        emptybutton.grid(row=3, column=0, columnspan=3, padx=5, pady=5)


class Board:
    def __init__(self, size, image):
        self.canvas = Canvas(height=9 * size + 10, width=9 * size + 10)
        buttons = {}
        for row in range(9):
            for col in range(9):
                cell = Cell(size, row, col, image)
                buttons[(row, col)] = cell
        self.buttons = buttons
        self.size = size

    def draw(self):
        for i in range(10):
            wd = 1
            if i % 3 == 0:
                wd = 2
            self.canvas.create_line(
                5, i * self.size + 5, 9 * self.size + 5, i * self.size + 5, width=wd
            )
            self.canvas.create_line(
                i * self.size + 5, 9 * self.size + 5, i * self.size + 5, 5, width=wd
            )
        self.canvas.place(x=0, y=0)

        for row in range(9):
            for col in range(9):
                cell = self.buttons[(row, col)]
                cell.create()

    def show_conflicts(self):
        self.restore_colors()
        fcolors = [
            "#FF0000",
            "#00FF00",
            "#0000FF",
            "#BB6600",
            "#BB0066",
            "#66BB00",
            "#00BB66",
            "#0066BB",
            "#6600BB",
        ]
        bcolors = [
            "#FFCCCC",
            "#CCFFCC",
            "#CCCCFF",
            "#FFDDBB",
            "#FFBBDD",
            "#DDFFBB",
            "#BBFFDD",
            "#BBDDFF",
            "#DDBBFF",
        ]
        puzzle = get_values(self)
        conflicts = check(puzzle)
        for pair in conflicts:
            v = self.buttons[pair].value
            self.buttons[pair].configure(fg=fcolors[v - 1], bg=bcolors[v - 1])
        if len(conflicts) == 0:
            messagebox.showinfo(
                "No conflicts found", "There are no direct conflicts in your puzzle."
            )

    def color_witnesses(self, row, col, x):
        for pair in relatives(row, col):
            if self.buttons[pair].value == x:
                self.buttons[pair].configure(bg=bred, fg=fred)

    def color_witnesses2(self, row, col, domain, v):
        present = 0
        for pair in domain:
            if pair == (row, col):
                continue
            elif self.buttons[pair].value == v:
                present = 1
                self.buttons[pair].config(fg=fred, bg=bred)
                break

    def color_witnesses3(self, row, col, domain, v):
        for cell in domain:
            if cell == (row, col):
                continue
            if self.buttons[cell]["bg"] in [bred, bgreen]:
                continue
            else:
                present = 0
                for pair in rows[cell[0]]:
                    if pair == (row, col):
                        continue
                    elif self.buttons[pair].value == v:
                        witness = pair
                        present = 1
                        break
                if present == 1:
                    for pair in rows[cell[0]]:
                        self.buttons[pair].config(fg=fred, bg=bred)
                    self.buttons[witness].config(fg=fgreen, bg=bgreen)
                else:
                    for pair in cols[cell[1]]:
                        if pair == (row, col):
                            continue
                        elif self.buttons[pair].value == v:
                            witness = pair
                            present = 1
                            break
                    if present == 1:
                        for pair in cols[cell[1]]:
                            self.buttons[pair].config(fg=fred, bg=bred)
                        self.buttons[witness].config(fg=fgreen, bg=bgreen)
                    else:
                        for pair in squares[(cell[0] // 3, cell[1] // 3)]:
                            if pair == (row, col):
                                continue
                            elif self.buttons[pair].value == v:
                                witness = pair
                                present = 1
                                break
                        if present == 1:
                            for pair in squares[(cell[0] // 3, cell[1] // 3)]:
                                self.buttons[pair].config(fg=fred, bg=bred)
                            self.buttons[witness].config(fg=fgreen, bg=bgreen)

    def restore_colors(self):
        for row in range(9):
            for col in range(9):
                x = self.buttons[(row, col)].value
                if x == 0:
                    fcolor = fgrey
                    bcolor = bgrey
                else:
                    fcolor = "black"
                    bcolor = "white"
                self.buttons[(row, col)].configure(fg=fcolor, bg=bcolor)

    def clear(self):
        for button in self.buttons.values():
            button.set_value(0)


def infobox():
    box = Toplevel(pady=10, padx=10)
    info1 = Label(box, text="Click a cell to set its value.", pady=5)
    info2 = Label(
        box,
        text="Click 'Check for conflicts' to search for straightforward contradictions.",
        pady=5,
    )
    info3 = Label(
        box,
        text="Click 'Reset cell colors' to make all empty cells grey and all cells with values white.",
        pady=5,
    )
    info4 = Label(
        box,
        text="Click 'Clear all cells' to remove the values, leaving the cells empty.",
        pady=5,
    )
    info5 = Label(
        box,
        text="Check the 'Show steps' box if you wish to see the steps of solution.",
        pady=5,
    )
    info6 = Label(
        box, text="Click 'Solve' to see the solution (with or without steps).", pady=5
    )
    ok = Button(box, text="Close", command=lambda: box.destroy(), pady=5, width=30)
    info1.pack()
    info2.pack()
    info3.pack()
    info4.pack()
    info5.pack()
    info6.pack()
    ok.pack()


class Menu(Frame):
    def __init__(self, solver):
        super().__init__()
        self.readme = Button(self, text="Readme", command=infobox, pady=10, width=20)
        self.solver = solver
        self.solvebutton = Button(
            self, text="Solve", command=self.solve, pady=10, width=20
        )
        self.steps = BooleanVar(self, False)
        self.showsteps = Checkbutton(
            self,
            text="Show steps",
            variable=self.steps,
            onvalue=True,
            offvalue=False,
            pady=10,
        )
        self.clearbutton = Button(
            self,
            text="Clear all cells",
            command=self.solver.board.clear,
            pady=10,
            width=20,
        )
        self.size = solver.board.size
        self.checker = Button(
            self,
            text="Check for conflicts",
            pady=10,
            width=20,
            command=self.solver.board.show_conflicts,
        )
        self.cells = None
        self.next = None
        self.final = None
        self.colors = Button(
            self,
            text="Reset cell colors",
            command=self.solver.board.restore_colors,
            pady=10,
            width=20,
        )

    def create(self):
        self.configure(width=150, pady=10)
        self.place(x=9 * self.size + 30, y=0)
        self.readme.pack(pady=10)
        self.checker.pack(pady=10)
        self.colors.pack(pady=10)
        self.clearbutton.pack(pady=10)
        self.showsteps.pack()
        self.solvebutton.pack(pady=5)

    def show_solution(self):
        self.solver.changed2 = 1
        while self.solver.changed2:
            self.solver.changed1 = 1
            while self.solver.changed1:
                self.solver.iterate1()
                self.update1()
                if self.solver.conflict == 1:
                    break
            self.solver.iterate2()
            self.update2()
            if self.solver.conflict == 1:
                break
        if self.solver.conflict == 1:
            self.solver.board.show_conflicts()
            messagebox.showwarning(
                title="Conflict",
                message="When solving the puzzle, I found a conflict.\nThere is no solution. Please change some values.",
            )
            self.solver.conflict = 0
        else:
            self.finish()

    def solve(self):
        if self.next is None:
            pass
        elif self.next.winfo_exists():
            self.next.destroy()
            self.final.destroy()
        self.cells = get_values(self.solver.board)[0]
        self.solver.puzzle = get_values(self.solver.board)
        if self.steps.get():
            self.solver.changed = 1
            self.next = Button(
                self,
                text="Next step",
                fg=fgreen,
                bg=bgreen,
                width=20,
                command=self.iterate,
            )
            self.final = Button(
                self,
                text="Show final solution",
                fg=fblue,
                bg=bblue,
                width=20,
                command=self.show_solution,
            )
            self.next.pack(pady=5)
            self.final.pack(pady=5)
        else:
            self.show_solution()

    def finish(self):
        nonzero = 1
        for button in self.solver.board.buttons.values():
            nonzero *= button.value
        if nonzero == 0:
            warn = Toplevel()
            warn.title("I can't figure out next step!")
            sorry1 = Label(warn, text="It seems that this puzzle is not easy.", pady=5)
            sorry2 = Label(
                warn,
                text="It is possible that it does not have a unique solution.",
                pady=5,
            )
            sorry3 = Label(
                warn,
                text="If there is a unique solution, finding it would require making some additional assumptions.",
                pady=5,
            )
            buttonframe = Frame(warn)
            cont = Button(
                buttonframe,
                text="Continue with current values",
                width=40,
                command=lambda: self.keep(warn),
            )
            rest = Button(
                buttonframe,
                text="Restore my values",
                width=40,
                command=lambda: self.restore(warn),
            )
            cont.pack(side="left")
            rest.pack()
            sorry1.pack()
            sorry2.pack()
            sorry3.pack()
            buttonframe.pack()
            if self.next is None:
                pass
            elif self.next.winfo_exists():
                self.next.destroy()
                self.final.destroy()
                self.solvebutton.config(state=ACTIVE)
                self.showsteps.config(state=ACTIVE)
                for button in self.solver.board.buttons.values():
                    button.config(state=ACTIVE)
        else:
            for button in self.solver.board.buttons.values():
                button.configure(fg=fgreen, bg=bgreen)

    def update1(self):
        if self.solver.changed1 == 1 or self.solver.changed2 == 1:
            row = self.solver.last_row
            col = self.solver.last_col
            v = self.solver.puzzle[0][row][col]
            if self.steps.get():
                l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                l.remove(v)
                self.solver.board.restore_colors()
                for pair in relatives(row, col):
                    self.solver.board.buttons[pair].configure(bg=byellow, fg=fyellow)
                self.solver.board.buttons[(row, col)].configure(fg=fblue, bg=bblue)
                for x in l:
                    self.solver.board.color_witnesses(row, col, x)
                self.solver.board.buttons[(row, col)].set_value(v)
                self.solver.board.buttons[(row, col)].config(bg=bblue, fg=fblue)
            else:
                self.solver.board.buttons[(row, col)].set_value(v)

    def update2(self):
        if self.solver.changed2 == 1:
            row = self.solver.last_row
            col = self.solver.last_col
            value = self.solver.puzzle[0][row][col]
            if self.steps.get():
                self.solver.board.restore_colors()
                l = []
                for pair in self.solver.domain:
                    self.solver.board.buttons[pair].config(fg=fblue, bg=bblue)
                    v = self.solver.board.buttons[pair].value
                    if v != 0:
                        l.append(v)
                # self.solver.board.color_witnesses2(row, col, self.solver.domain, v)
                self.solver.board.color_witnesses3(row, col, self.solver.domain, value)
                self.solver.board.buttons[(row, col)].set_value(v)
                self.solver.board.buttons[(row, col)].config(bg=bblue, fg=fblue)
            else:
                self.solver.board.buttons[(row, col)].set_value(value)

    def iterate(self):
        self.solvebutton.config(state=DISABLED)
        self.showsteps.config(state=DISABLED)
        for button in self.solver.board.buttons.values():
            button.config(state=DISABLED)
        self.solver.changed1 = 2
        while self.solver.changed1 == 2:
            self.solver.iterate1()
        if self.solver.changed1 == 0:
            self.solver.iterate2()
        self.update1()
        self.update2()
        if self.solver.changed1 == 0 and self.solver.changed2 == 0:
            self.finish()
        elif self.solver.conflict == 1:
            self.solver.board.show_conflicts()
            messagebox.showwarning(
                title="Conflict",
                message="When solving the puzzle, I found a conflict.\nThere is no solution. Please change some values.",
            )
            self.solver.conflict = 0
            self.solvebutton.config(state=ACTIVE)
            self.solvebutton.config(state=ACTIVE)
            for button in self.solver.board.buttons.values():
                button.config(state=ACTIVE)
            self.next.destroy()
            self.final.destroy()

    def keep(self, warn):
        for button in self.solver.board.buttons.values():
            if button.value == 0:
                fgcolor = fgrey
                bgcolor = bgrey
            else:
                fgcolor = "black"
                bgcolor = "white"
            button.configure(fg=fgcolor, bg=bgcolor)
        warn.destroy()

    def restore(self, warn):
        for row in range(9):
            for col in range(9):
                self.solver.board.buttons[(row, col)].set_value(self.cells[row][col])
        warn.destroy()
