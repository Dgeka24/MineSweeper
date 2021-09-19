import os
import pickle

import Game



if __name__ == '__main__':


    game = Game.createGame()

    #file = open("last_save.pckl", "ab")
    print(os.getcwd())
    game.printField()
    #game = Game.Game()
    #pickle.dump(game, file)




