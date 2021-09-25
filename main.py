import Game
import Solver

def CheckName(name: str) -> bool:
    if len(name) > 10:
        return False
    return name.isalnum()


def ArgumentsOfCreation() -> tuple:
    print("Введите размеры поля и количество мин [int] [int] [int] (размеры не должны превышать 50)")
    command = list(filter(None, input().split(' ')))
    if len(command) != 3:
        print("Неверный формат ввода")
        return None, None, None
    for x in command:
        if not x.isdigit():
            print("Неверный формат ввода")
            return None, None, None
    rows = int(command[0])
    columns = int(command[1])
    mines = int(command[2])
    if rows > 50 or rows < 0 or columns > 50 or columns < 0 or mines > rows*columns or mines < 0:
        print("Некорректное поле")
        return None, None, None
    return rows, columns, mines



def CreationCommand() -> Game.Game:
    print("Создать новую игру или загрузить старую? [new/load] [name] (имя латинские буквы и цифры без пробелов, длина не более 10 символов)")
    command = input()
    parsed = list(filter(None, command.split(' ')))
    if len(parsed) != 2:
        print("Неправильный формат ввода")
        return None
    if parsed[0] not in ["new", "load"]:
        print("Неправильный формат ввода")
        return None
    if not CheckName(parsed[1]):
        print("Неправильный формат ввода")
        return None
    if parsed[0] == "new":
        rows = None
        columns = None
        mines = None
        while rows is None:
            (rows, columns, mines) = ArgumentsOfCreation()
        return Game.NewGame(rows, columns, mines, parsed[1])
    else:
        return Game.LoadGame(parsed[1])


def move(game: Game.Game):
    point = (None, None)
    move_type = None
    while point[0] is None:
        print("Сделайте ход! Координаты и тип хода [int] [int] [Flag/Open/Recommend/Solve]")
        command = list(filter(None, input().split(' ')))
        if len(command) == 1 and command[0] in ["Recommend", "Solve"]:
            point = (1, 1)
            move_type = command[0]
        elif len(command) == 3 and command[0].isdigit() and command[1].isdigit() and command[2] in ["Flag", "Open", "Recommend", "Solve"]:
            point = (int(command[0]), int(command[1]))
            move_type = command[2]
            if not game.isPointCorrect((point[0]-1, point[1]-1)):
                point = (None, None)
                move_type = None
                print("Некорректный ход")
        else:
            print("Некорректный ход")
    if move_type in ["Flag", "Open"]:
        game.make_move(point, move_type)
    elif move_type == "Recommend":
        move = Solver.RecommendMove(game.player_field)
        move = ((move[0][0]+1, move[0][1]+1), move[1])
        if not (move is None):
            print("Рекомендуемый ход: ", move)
        else:
            print("Нет рекомендуемого хода")
    else:
        while game.GameState:
            move = Solver.RecommendMove(game.player_field)
            if move is None:
                for i in range(game.amount_of_rows):
                    for j in range(game.amount_of_columns):
                        if game.player_field[i][j] == game.CONST_FlagSymbol:
                            game.make_move((i+1,j+1), "Flag")
            else:
                move = ((move[0][0] + 1, move[0][1] + 1), move[1])
                print("Ход ", move)
                game.make_move(move[0], move[1])


if __name__ == '__main__':
    game = None
    while game is None:
        game = CreationCommand()
    while game.GameState:
        game.printField()
        move(game)

    game.printField()
    print("Игра завершена")
