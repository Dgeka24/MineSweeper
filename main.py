import os
import pickle

import Game




if __name__ == '__main__':

    print("Создать новую игру или загрузить старую? [new/load] [name] (латинские буквы и цифры без пробелов)")



    game = Game.createGame("new_game1")
    #game = Game.loadGame(game_name = "new_game1")
    if game == None:
        exit()
    GameState = True
    while GameState:
        game.printField()
        string = input().split(' ')
        x = int(string[0])
        y = int(string[1])
        symbol = string[2]
        GameState = GameState and game.make_move((x,y), symbol)

    #file = open("last_save.pckl", "ab")
    print(os.getcwd())
    #game.printField()
    #game = Game.Game()
    #pickle.dump(game, file)




