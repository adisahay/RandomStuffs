import sys
import random

MINE = -1

class Board:
    def __init__(self, size, mines):
        self.size = size
        end = size * size - 1
        self.board = [[0 for i in range(size)] for i in range(size)]
        self.ui = [[False for i in range(size)] for i in range(size)]

        count = 0
        self.mineLocs = []
        while count < mines:
            rnd = random.randint(0, end)
            row = rnd // size
            col = rnd % size

            if self.board[row][col] == MINE:
                continue

            self.board[row][col] = MINE
            self.mineLocs.append((row, col))
            count += 1

        for i, j in self.mineLocs:
            self.__setMarkers(i, j)

    def __setMarkers(self, row, col):
        self.__setMark(row - 1, col)
        self.__setMark(row - 1, col + 1)
        self.__setMark(row - 1, col - 1)
        self.__setMark(row, col - 1)
        self.__setMark(row, col + 1)
        self.__setMark(row + 1, col - 1)
        self.__setMark(row + 1, col)
        self.__setMark(row + 1, col + 1)

    def __setMark(self, row, col):
        if row < 0 or row >= self.size or col < 0 or col >= self.size or self.board[row][col] == MINE:
            return

        self.board[row][col] += 1

    def displayUI(self):
        print("   ", end = "")
        for i in range(self.size):
            print(chr(ord("A") + i), end = "  ")
        print("")

        for i in range(self.size):
            for j in range(self.size):
                if j is 0:
                    print(chr(ord("A") + i), end = " ")
                if self.ui[i][j]:
                    if self.board[i][j] == 0:
                        print("[ ]", end = "")
                    elif self.board[i][j] == MINE:
                        print("[*]", end = "")
                    else:
                        print("[" + str(self.board[i][j]) + "]", end = "")
                else:
                    print("[+]", end = "")
            print("")

    def reveal(self, row, col):
        if row >= 0 and row < self.size and col >= 0 and col < self.size and self.ui[row][col] is False:
            self.ui[row][col] = True
            if self.board[row][col] == 0:
                self.reveal(row - 1, col - 1)
                self.reveal(row - 1, col)
                self.reveal(row - 1, col + 1)
                self.reveal(row, col - 1)
                self.reveal(row, col + 1)
                self.reveal(row + 1, col - 1)
                self.reveal(row + 1, col)
                self.reveal(row + 1, col + 1)


class Game:
    def __init__(self, size, mines):
        if size > 25:
            print("Only size upto 25x25 supported")
            sys.exit()
        if size * size <= mines:
            print("No. of mines must be less than the size of the board")
            sys.exit()

        self.board = Board(size, mines)

    def click(self, cell):
        if cell[0] >= "A" and cell[0] <= "Z" and cell[1] >= "A" and cell[1] <= "Z":
            row = ord(cell[0]) - ord("A")
            col = ord(cell[1]) - ord("A")
            return self.board.reveal(row, col)

    def prompt(self):
        return

    def showBoard(self):
        self.board.displayUI()

import sys
import subprocess as sp

game = Game(int(sys.argv[1]), int(sys.argv[2]))
while True:
    sp.call("clear", shell = True)
    game.showBoard()
    print("\nEnter the cell position (e.g. 'AD' for row - A, col - D), or type 'exit':")
    pos = input()
    if pos == "exit":
        break
    game.click(pos)
