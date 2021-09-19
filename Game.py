import random
import time
import os
import pickle


def createGame():
    path_to_save = os.path.join(os.getcwd(), "last_save.pckl")
    print(path_to_save)
    if os.path.exists(path_to_save):
        print("Game was loaded")
        file = open(path_to_save, 'rb')
        game = pickle.load(file)
    else:
        print("No saved games")
        game = Game.Game()
        file = open("last_save.pckl", "wb")
        pickle.dump(game, file)
        print("New game was created")
    return game


class Game:
    CONST_MineValue = -1
    CONST_MineSymbol = '*'
    CONST_ShadowSymbol = '#'

    def __init__(self, n: int = 5, m: int = 5, mines: int = 5):
        # добавить проверку значений
        #random.seed(0)
        seed = int(time.time())
        print("CURRENT SEED ", seed)
        random.seed(seed)
        self.amount_of_rows = n
        self.amount_of_columns = m
        self.amount_of_mines = mines
        self.field = []
        self.player_field = []
        self.GenerateField()
        self.printField()

    def printField(self):
        for row in self.field:
            for cell in row:
                print(cell, end="")
            print()

        print()
        for row in self.player_field:
            for cell in row:
                print(cell, end="")
            print()

    def GenerateField(self):
        n = self.amount_of_rows
        m = self.amount_of_columns
        mines = self.amount_of_mines
        self.player_field = [[Game.CONST_ShadowSymbol for j in range(m)] for i in range(n)]
        self.field = [[0 for j in range(m)] for i in range(n)]
        free_poses = set([(i, j) for j in range(m) for i in range(n)])
        amount_of_mines = 0
        help_field = [[0 for j in range(m)] for i in range(n)]

        while amount_of_mines < mines:
            (x, y) = (random.sample(free_poses, k=1))[0]
            help_field[x][y] -= 1
            if help_field[x][y] < 0:
                free_poses.remove((x,y))
                amount_of_mines += 1
                help_field[x][y] -= 10000
                self.field[x][y] = Game.CONST_MineSymbol
                for (i, j) in self.PossibleNeighbours((x, y)):
                    help_field[i][j] += 1
        for (x,y) in free_poses:
            self.field[x][y] = self.countMines((x, y))

    def countMines(self, point: tuple):
        counter = 0
        for (i,j) in self.PossibleNeighbours(point):
            if self.field[i][j] == Game.CONST_MineSymbol:
                counter += 1
        return counter

    def isPointCorrect(self, point: tuple) -> bool:
        n = self.amount_of_rows
        m = self.amount_of_columns
        (x, y) = point
        if x < 0 or y < 0 or x >= n or y >= m:
            return False
        return True

    def PossibleNeighbours(self, point: tuple) -> list:
        n = self.amount_of_rows
        m = self.amount_of_columns
        (x, y) = point
        return [
            (new_x, new_y)
            for new_x in range(x - 1, x + 2) for new_y in range(y-1, y+2)
            if abs(new_x - x) + abs(new_y - y) != 0 and self.isPointCorrect((new_x, new_y))
        ]

