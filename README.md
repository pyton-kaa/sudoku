# sudoku
An application solving easy and medium sudoku puzzles

## What does it do?
The application opens an empty 9x9 board. When you click any cell, you can set its value (1-9 or empty).

On the right side of the board there are several buttons. You can view an instruction, restore colors, check for conflicts or solve the puzzle.

### Conflicts
The 'Check for conflicts' button finds only direct conflicts: two cells with the same value in the same row, column or square.

### Solving
You can solve puzzles that do not require making assumptions. For example, easy- and medium-level puzzles from sudoku.com website are resolved.

If you check the 'Show steps' checkbox, you can view step-by-step solution. After clicking 'Next step', a new value shows up, highlited in blue. An explanation of this choice is highlited in red. It is either *related* (in terms of sudoku) cells with all other values, or other cells in the same row/column/square, *related* to some cell that has the same value.

If you started viewing the step-by-step solution, you can jump to the final solution using the 'Show final solution' button.

## What did I learn?
* Creating GUI with Tkinter
* Applying actions on the click of a button
* Adjusting layout (colours, fonts, sizes)
* Translating a practical puzzle-solving method to a precise algorithm
