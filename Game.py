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
    #создать для field отдельный класс
    CONST_MineSymbol = '*'
    CONST_ShadowSymbol = '#'
    CONST_FlagSymbol = "F"

    def __init__(self, n: int = 5, m: int = 5, mines: int = 5):
        # добавить проверку значений
        #random.seed(0)
        seed = int(time.time())
        print("CURRENT SEED ", seed)
        random.seed(seed)
        self.amount_of_rows = n
        self.amount_of_columns = m
        self.amount_of_mines = mines
        self.amount_of_shadows = n*m
        self.amount_of_flags = 0
        self.GameState = True
        self.field = []
        self.player_field = []
        self.GenerateField()
        self.printField()

    def flag_cell(self, point: tuple) -> bool:
        (x,y) = point
        if self.player_field[x][y] in "0123456789":
            return False
        if self.player_field[x][y] != Game.CONST_FlagSymbol:
            self.player_field[x][y] = Game.CONST_FlagSymbol
        else:
            self.player_field[x][y] = Game.CONST_ShadowSymbol
        return True

    def open_cell(self, point: tuple) -> bool:
        (x,y) = point
        if self.player_field[x][y] == self.field[x][y]:
            return True
        self.player_field[x][y] = self.field[x][y]
        if self.player_field[x][y] == Game.CONST_MineSymbol:
            return False
        if self.player_field[x][y] == 0:
            self.open_zero_cell(point)
        return True

    def open_zero_cell(self, point : tuple):
        (x,y) = point
        for new_point in self.PossibleNeighbours(point):
            self.open_cell(new_point)

    def make_move(self, point: tuple, move_type: str) -> bool:
        point = (point[0] - 1, point[1] - 1)
        (x,y) = point
        if move_type == "F":
            if not self.flag_cell(point):
                print("Incorrect cell for flagging")
        elif move_type == "O":
            if not self.open_cell(point):
                print("Game Over")
                return False
                #add endgame
        #сохранить новое состояние
        return True

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


class Field:
    def __init__(self):
        seed = int(time.time())
        print("CURRENT SEED ", seed)
        random.seed(seed)
        self.amount_of_rows
        self.amount_of_columns
        self.field = []
