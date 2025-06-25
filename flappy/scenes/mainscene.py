import pygame
from pygame.event import Event
from xodex.scenes import Scene, SceneManager


class MainScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        img = self.object.Image

    def _generate_objects_(self):
        Image = self.object.Image
        Floor = self.object.Floor
        Flappy = self.object.Flappy
        Background = self.object.Background

        message = Image(
            "assets/images/message.png",
            (int((self.width - 184) // 2), int(self.height * 0.12)),
        )

        yield Background()
        yield Floor()
        yield Flappy()
        yield message

    def handle_scene(self, event: Event, *args, **kwargs) -> None:
        """
        Handle an event for all objects in the scene.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.enter()
        super().handle_scene(event, *args, **kwargs)

    def update_scene(self, deltatime: float, *args, **kwargs) -> None:
        """
        Update all objects in the scene, unless paused.

        Args:
            deltatime (float): Time since last update (ms).
        """
        super().update_scene(deltatime, *args, **kwargs)

    def enter(self):
        """enter"""
        pygame.mixer.Sound("assets/sounds/wing.wav").play()
        SceneManager().reset("GameScene")
