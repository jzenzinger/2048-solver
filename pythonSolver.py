from tkinter import *
from tkinter import messagebox
import random
import colors

# ----------------------------------------------------------------------------------------------------------------------
class GameBoard:
    bg_color = {
        "2": "#fcefe6",
        "4": "#f2e8cb",
        "8": "#f5b682",
        "16": "#f29446",
        "32": "#ff775c",
        "64": "#e64c2e",
        "128": "#ede291",
        "256": "#fce130",
        "512": "#ffdb4a",
        "1024": "#f0b922",
        "2048": "#fad74d"
    }
    color = {
        "2": "#695c57",
        "4": "#695c57",
        "8": "#ffffff",
        "16": "#ffffff",
        "32": "#ffffff",
        "64": "#ffffff",
        "128": "#ffffff",
        "256": "#ffffff",
        "512": "#ffffff",
        "1024": "#ffffff",
        "2048": "#ffffff"
    }

    def __init__(self):
        self.n = 4
        self.window = Tk()
        self.window.title('Solver 2048')
        self.gameArea = Frame(self.window, bg=colors.EMPTY_CELL_COLOR)
        self.board = []
        self.gridCell = [[0] * 4 for i in range(4)]
        self.compress = False
        self.merge = False
        self.moved = False
        self.score = 0

        for i in range(4):
            rows = []
            for j in range(4):
                l = Label(self.gameArea, text='', bg='azure4', font=('arial', 22, 'bold'), width=4, height=2)
                l.grid(row=i, column=j, padx=7, pady=7)

                rows.append(l)
            self.board.append(rows)
        self.gameArea.grid()

    # ------------------------------------------------------------------------------------------------------------------
    # Methods for manipulation with grid
    def reverse(self):
        for ind in range(4):
            i = 0
            j = 3
            while i < j:
                self.gridCell[ind][i], self.gridCell[ind][j] = self.gridCell[ind][j], self.gridCell[ind][i]
                i += 1
                j -= 1

    def transpose(self):
        self.gridCell = [list(t) for t in zip(*self.gridCell)]

    def compressGrid(self):
        self.compress = False
        temp = [[0] * 4 for i in range(4)]
        for i in range(4):
            cnt = 0
            for j in range(4):
                if self.gridCell[i][j] != 0:
                    temp[i][cnt] = self.gridCell[i][j]
                    if cnt != j:
                        self.compress = True
                    cnt += 1
        self.gridCell = temp

    def mergeGrid(self):
        self.merge = False
        for i in range(4):
            for j in range(4 - 1):
                if self.gridCell[i][j] == self.gridCell[i][j + 1] and self.gridCell[i][j] != 0:
                    self.gridCell[i][j] *= 2
                    self.gridCell[i][j + 1] = 0
                    self.score += self.gridCell[i][j]
                    self.merge = True

    def random_cell(self):
        cells = []
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j] == 0:
                    cells.append((i, j))
        curr = random.choice(cells)
        i = curr[0]
        j = curr[1]
        self.gridCell[i][j] = 2

    def can_merge(self):
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] == self.gridCell[i][j + 1]:
                    return True

        for i in range(3):
            for j in range(4):
                if self.gridCell[i + 1][j] == self.gridCell[i][j]:
                    return True
        return False

    # ------------------------------------------------------------------------------------------------------------------
    # Methods for paint grid with bg and colors
    def paintGrid(self):
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j] == 0:
                    self.board[i][j].config(text='', bg='azure4')
                else:
                    self.board[i][j].config(text=str(self.gridCell[i][j]),
                                            bg=self.bg_color.get(str(self.gridCell[i][j])),
                                            fg=self.color.get(str(self.gridCell[i][j])))


# ----------------------------------------------------------------------------------------------------------------------
# Class for main game
class Game:
    def __init__(self, gameBoard):
        self.board = gameBoard
        self.end = False
        self.won = False
        self.score = 0
        self.highestNumber = 0

    def strategy(self):
        key = randomkey()
        self.link_keys(key)
        self.board.window.after(2, self.strategy)

    def start(self):
        self.board.random_cell()
        self.board.random_cell()
        self.board.paintGrid()
        self.board.window.after(2, self.strategy)
        self.board.window.mainloop()

    def link_keys(self, key):
        if self.end or self.won:
            return
        self.board.compress = False
        self.board.merge = False
        self.board.moved = False

        pressedKey = key

        if pressedKey == 'Up':
            self.board.transpose()
            self.board.compressGrid()
            self.board.mergeGrid()
            self.board.moved = self.board.compress or self.board.merge
            self.board.compressGrid()
            self.board.transpose()

        elif pressedKey == 'Down':
            self.board.transpose()
            self.board.reverse()
            self.board.compressGrid()
            self.board.mergeGrid()
            self.board.moved = self.board.compress or self.board.merge
            self.board.compressGrid()
            self.board.reverse()
            self.board.transpose()

        elif pressedKey == 'Left':
            self.board.compressGrid()
            self.board.mergeGrid()
            self.board.moved = self.board.compress or self.board.merge
            self.board.compressGrid()

        elif pressedKey == 'Right':
            self.board.reverse()
            self.board.compressGrid()
            self.board.mergeGrid()
            self.board.moved = self.board.compress or self.board.merge
            self.board.compressGrid()
            self.board.reverse()
        else:
            pass

        self.board.paintGrid()

        flag = 0
        for i in range(4):
            for j in range(4):
                if self.board.gridCell[i][j] == 2048:
                    flag = 1
                    break

        if flag == 1:  # found 2048
            self.won = True
            messagebox.showinfo('2048', message='You Won!')
            return

        for i in range(4):
            for j in range(4):
                if self.board.gridCell[i][j] == 0:
                    flag = 1
                    break

        if not (flag or self.board.can_merge()):
            self.end = True
            messagebox.showinfo('2048', message='Game Over!\nSorry, you will close this window too many times '
                                                'ff:)\n\nAnd again.')

        if self.board.moved:
            self.board.random_cell()

        if self.end or self.won:
            matrix = self.board.gridCell
            cells = []
            for i in matrix:
                for j in i:
                    cells.append(j)
            cells.sort()
            self.highestNumber = cells[-1]
            self.score = self.board.score
            self.board.window.quit()
            self.board.window.destroy()

            return

        self.board.paintGrid()


# ----------------------------------------------------------------------------------------------------------------------
# Random Key Generator for returning a random key choice
def randomkey():
    keys = ["Up", "Down", "Left", "Right"]
    chooseKey = random.choice(keys)
    return chooseKey


# ----------------------------------------------------------------------------------------------------------------------
# Class for statistics and their printing on console through game playing, if user wants to play it by AI
class Stats:
    def __init__(self, iteration):
        self.iteration = iteration
        self.stats = []
        self.play30()

    def play30(self):
        for i in range(self.iteration):
            game = Game(GameBoard())
            game.start()
            self.stats.append([game.highestNumber, game.score])

    def getStats(self):
        print("Stats:\n")
        print("-----------------------------")
        print("#\tHighest\t\tScore\tW/L")
        j = 1
        w = 0
        l = 0
        for i in self.stats:
            if i[0] >= 2048:
                print(j, ".\t", i[0], "\t\t", i[1], "\tW")
                w += 1
            else:
                print(j, ".\t", i[0], "\t\t", i[1], "\tL")
                l += 1
            j += 1
        print("-----------------------------")
        print(f"\n\nRandom strategy ->\t\tWin: {w} Lost: {l}")
