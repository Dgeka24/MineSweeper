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
        print("Сделайте ход! Координаты и тип хода [int] [int] [Flag/Open]")
        command = list(filter(None, input().split(' ')))
        if len(command) == 3 and command[0].isdigit() and command[1].isdigit() and command[2] in ["Flag", "Open"]:
            point = (int(command[0]), int(command[1]))
            move_type = command[2]
            if not game.isPointCorrect((point[0]-1, point[1]-1)):
                point = (None, None)
                move_type = None
                print("Некорректный ход")
        else:
            print("Некорректный ход")
    game.make_move(point, move_type)


if __name__ == '__main__':
    game = None
    while game is None:
        game = CreationCommand()
    while game.GameState:
        game.printField()
        move(game)
    game.printField()
    print("Игра завершена")
