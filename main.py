import os
import pickle

import Game



if __name__ == '__main__':


    game = Game.createGame()
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




