import pygame
from pygame.event import Event
from xodex.scenes import Scene, SceneManager


class GameScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _generate_objects_(self):
        Pipes = self.object.Pipes
        Floor = self.object.Floor
        Flappy = self.object.Flappy
        Background = self.object.Background

        floor = Floor()
        pipes = Pipes()
        flappy = Flappy(50, 256, floor, pipes)
        flappy.set_mode(2)  # normal mode

        yield Background()
        yield floor
        yield pipes
        yield flappy

    def gameover(self):
        """entergame"""
        pygame.mixer.Sound("assets/sounds/wing.wav").play()
        SceneManager().append("OverScene", self.screen)
