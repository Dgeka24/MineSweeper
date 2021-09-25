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
                elif number_of_shadows == field[i][j] and number_of_shadows > 0:
                    for (x, y) in PossibleNeighbours(field, (i, j)):
                        if field[x][y] == Game.Game.CONST_ShadowSymbol:
                            obvious_moves[(x,y)] = 'Flag'


def CheckSquare(field: list, i: int, j: int, step_rows: int, step_columns: int):
    Square = field[i:i+step_rows]
    for i in len(Square):
        Square[i] = Square[i][j:j+step_columns]
    poses_of_shadows = dict()
    shadows_as_mines = dict()
    amount_of_shadows = 0
    amount_of_numbers = 0
    for x in range(len(Square)):
        for y in range(len(Square[x])):
            if Square[x][y] == Game.Game.CONST_ShadowSymbol:
                poses_of_shadows[amount_of_shadows] = (x,y)
                amount_of_shadows += 1
            elif Square[x][y] in CONST_NUMBERS_LIST:
                amount_of_numbers += 1
    if amount_of_numbers == 0 or amount_of_shadows == 0:
        return None
    Border = (1 << amount_of_shadows)
    for mask in range(Border):
        for byte_num in range(amount_of_shadows):
            (x,y) = poses_of_shadows[byte_num]
            if ((1<<byte_num) & mask) == 1:
                Square[x][y] = Game.Game.CONST_MineSymbol
            else:
                Square[x][y] = Game.Game.CONST_ShadowSymbol







def CheckingGrids(field: list):
    step_rows = min(4, len(field))
    step_columns = min(4, len(field[0]))
    for i in range(len(field)-step_rows+1):
        for j in range(len(field[i])-step_columns+1):
            move = CheckSquare(field, i, j, step_rows, step_columns)
            if not (move is None):
                return move
    return None


def RecommendMove(field: list):
    if len(obvious_moves) > 0:
        return obvious_moves.popitem()
    FindObvious(field)
    if len(obvious_moves) > 0:
        return obvious_moves.popitem()


