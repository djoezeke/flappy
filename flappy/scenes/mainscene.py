import pygame
from pygame.event import Event
from xodex.scenes import Scene, SceneManager


class MainScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _generate_objects_(self):
        Bird = self.object.Bird
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
        yield Bird(120, 120)
        yield Flappy(120, int(self.height * 0.65), None, None)
        yield message

    def handle_scene(self, event: Event, *args, **kwargs) -> None:
        """
        Handle an event for all objects in the scene.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.entergame()
        super().handle_scene(event, *args, **kwargs)

    def entergame(self):
        """entergame"""
        pygame.mixer.Sound("assets/sounds/wing.wav").play()
        SceneManager().reset("GameScene")
