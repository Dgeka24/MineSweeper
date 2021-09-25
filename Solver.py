import Game

CONST_NUMBERS_LIST = [1, 2, 3, 4, 5, 6, 7, 8, 9]
obvious_moves = dict()


def isPointCorrect(field: list, point: tuple) -> bool:
    n = len(field)
    m = len(field[0])
    (x, y) = point
    if x < 0 or y < 0 or x >= n or y >= m:
        return False
    return True


def PossibleNeighbours(field: list, point: tuple) -> list:
    (x, y) = point
    return [
        (new_x, new_y)
        for new_x in range(x - 1, x + 2) for new_y in range(y - 1, y + 2)
        if abs(new_x - x) + abs(new_y - y) != 0 and isPointCorrect(field, (new_x, new_y))
    ]


def FindObvious(field: list) -> tuple:
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] in CONST_NUMBERS_LIST:
                number_of_flags = 0
                number_of_shadows = 0
                for (x,y) in PossibleNeighbours(field, (i,j)):
                    if field[x][y] == Game.Game.CONST_ShadowSymbol:
                        number_of_shadows += 1
                    elif field[x][y] == Game.Game.CONST_FlagSymbol:
                        number_of_flags += 1
                if number_of_flags == field[i][j] and number_of_shadows > 0:
                    for (x, y) in PossibleNeighbours(field, (i, j)):
                        if field[x][y] == Game.Game.CONST_ShadowSymbol:
                            obvious_moves[(x,y)] = 'Open'
                elif number_of_shadows == field[i][j] - number_of_flags and number_of_shadows > 0:
                    for (x, y) in PossibleNeighbours(field, (i, j)):
                        if field[x][y] == Game.Game.CONST_ShadowSymbol:
                            obvious_moves[(x,y)] = 'Flag'


def RecommendMove(field: list):
    if len(obvious_moves) > 0:
        return obvious_moves.popitem()
    FindObvious(field)
    if len(obvious_moves) > 0:
        return obvious_moves.popitem()
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == "#":
                return ((i,j), "Open")
    return None
