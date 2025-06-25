import pygame
from pygame.event import Event
from xodex.scenes import BlurScene, SceneManager


class OverScene(BlurScene):
    def __init__(self, blur_surface, score, **kwargs):
        super().__init__(
            blur_surface, blur_count=2, blur_duration=3, on_blur_complete=None, **kwargs
        )
        self.score = score

    def _generate_objects_(self):
        Image = self.object.Image
        Score = self.object.Score

        score = Score(self.width, self.height)
        score.set(self.score)

        message = Image(
            "assets/images/gameover.png",
            (int((self.width - 184) // 2), int(self.height * 0.5)),
        )

        yield message
        yield score

    def handle_scene(self, event: Event, *args, **kwargs) -> None:
        """
        Handle an event for all objects in the scene.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.gotomain()
        super().handle_scene(event, *args, **kwargs)

    def gotomain(self):
        """gotomain"""
        pygame.mixer.Sound("assets/sounds/wing.wav").play()
        SceneManager().reset("MainScene")

    def on_first_enter(self, *args, **kwargs):
        pygame.mixer.Sound("assets/sounds/swoosh.wav").play()
