"""FLAPPY project Main Game Loop"""

from xodex.game.game import Game

from . import objects
from . import scenes


if __name__ == "__main__":
    game = Game("flappy")
    game.main_loop()
