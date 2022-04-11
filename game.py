import tkinter as tk
import colors
import random


class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.matrix = None
        self.score = None
        self.scoreLabel = None
        self.cells = None
        self.grid()
        self.master.title("2048 with AI")

        self.mainGrid = tk.Frame(
            self, bg=colors.GRID_COLOR, bd=3, width=600, height=600
        )
        self.mainGrid.grid(pady=(100, 0))
        self.createGUI()
        self.startGame()

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

        self.mainloop()  # display main GUI until user will manually close it

    # ------------------------------------------------------------------------------------------------------------------
    def createGUI(self):
        # create grid
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cellFrame = tk.Frame(
                    self.mainGrid, bg=colors.EMPTY_CELL_COLOR, width=150, height=150
                )
                cellFrame.grid(row=i, column=j, padx=5, pady=5)
                cellNumber = tk.Label(self.mainGrid, bg=colors.EMPTY_CELL_COLOR)
                cellNumber.grid(row=i, column=j)
                cell_data = {"frame": cellFrame, "number": cellNumber}

                row.append(cell_data)
            self.cells.append(row)

        # Score header for GUI
        scoreFrame = tk.Frame(self)
        scoreFrame.place(relx=0.5, y=45, anchor="center")
        tk.Label(scoreFrame, text="Score", font=colors.SCORE_LABEL_FONT).grid(row=0)

        self.scoreLabel = tk.Label(scoreFrame, text="0", font=colors.SCORE_FONT)
        self.scoreLabel.grid(row=1)

    # ------------------------------------------------------------------------------------------------------------------
    def startGame(self):
        self.matrix = [[0] * 4 for _ in range(4)]

        # random fill 2 with numbers - matrix is empty
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=colors.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=colors.CELL_COLORS[2],
            fg=colors.CELL_NUMBER_COLORS[2],
            font=colors.CELL_NUMBER_FONTS[2],
            text="2"
        )

        # fill with random position 2 if the matrix isn't empty
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=colors.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=colors.CELL_COLORS[2],
            fg=colors.CELL_NUMBER_COLORS[2],
            font=colors.CELL_NUMBER_FONTS[2],
            text="2"
        )
        self.score = 0

    # ------------------------------------------------------------------------------------------------------------------
    # Manipulation methods to use in arrow functions
    def stack(self):
        newMatrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fillPos = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    newMatrix[i][fillPos] = self.matrix[i][j]
                    fillPos += 1
        self.matrix = newMatrix

    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]

    def reverse(self):
        newMatrix = []
        for i in range(4):
            newMatrix.append([])
            for j in range(4):
                newMatrix[i].append(self.matrix[i][3 - j])
        self.matrix = newMatrix

    def transpose(self):
        newMatrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                newMatrix[i][j] = self.matrix[j][i]
        self.matrix = newMatrix

    # ------------------------------------------------------------------------------------------------------------------
    # Add a new 2 or 4 tile randomly to an empty cell
    def addNewTile(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while (self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = random.choice([2, 4])

    # ------------------------------------------------------------------------------------------------------------------
    # Update the GUI to match the matrix
    def updateGUI(self):
        for i in range(4):
            for j in range(4):
                cellValue = self.matrix[i][j]
                if cellValue == 0:
                    self.cells[i][j]["frame"].configure(bg=colors.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=colors.EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=colors.CELL_COLORS[cellValue])
                    self.cells[i][j]["number"].configure(
                        bg=colors.CELL_COLORS[cellValue],
                        fg=colors.CELL_NUMBER_COLORS[cellValue],
                        font=colors.CELL_NUMBER_FONTS[cellValue],
                        text=str(cellValue))
        self.scoreLabel.configure(text=self.score)
        self.update_idletasks()

    # ------------------------------------------------------------------------------------------------------------------
    # Arrow-Press Functions
    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.addNewTile()
        self.updateGUI()
        self.gameOver()

    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.addNewTile()
        self.updateGUI()
        self.gameOver()

    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.addNewTile()
        self.updateGUI()
        self.gameOver()

    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.addNewTile()
        self.updateGUI()
        self.gameOver()

    # ------------------------------------------------------------------------------------------------------------------
    # Check if any horizontal moves are possible
    def horizontalMoveExists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False

    # Check if any vertical moves are possible
    def verticalMoveExists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    # ------------------------------------------------------------------------------------------------------------------
    # Check if Game is Over - no possible moves
    def gameOver(self):
        if any(2048 in row for row in self.matrix):
            gameOverFrame = tk.Frame(self.mainGrid, borderwidth=2)
            gameOverFrame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                gameOverFrame,
                text="You win!",
                bg=colors.WINNER_BG,
                fg=colors.GAME_OVER_FONT_COLOR,
                font=colors.GAME_OVER_FONT).pack()
        elif not any(0 in row for row in
                     self.matrix) and not self.horizontalMoveExists() and not self.verticalMoveExists():
            gameOverFrame = tk.Frame(self.mainGrid, borderwidth=2)
            gameOverFrame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                gameOverFrame,
                text="Game over!",
                bg=colors.LOSER_BG,
                fg=colors.GAME_OVER_FONT_COLOR,
                font=colors.GAME_OVER_FONT).pack()
