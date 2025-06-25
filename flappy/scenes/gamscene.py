import pygame
from pygame.event import Event
from xodex.scenes import Scene, SceneManager


class GameScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Pipes = self.object.Pipes
        Floor = self.object.Floor
        Score = self.object.Score
        Flappy = self.object.Flappy
        self.floor = Floor(self.width)
        self.score = Score(self.width, self.height)
        self.pipes = Pipes(self.width, self.height)
        self.flappy = Flappy(self.width, self.height)

    def _generate_objects_(self):
        Background = self.object.Background

        self.flappy.set_mode(2)  # normal mode

        yield Background()
        yield self.floor
        yield self.pipes
        yield self.score
        yield self.flappy

    def gameover(self):
        """entergame"""
        pygame.mixer.Sound("assets/sounds/die.wav").play()
        SceneManager().append("OverScene", self.screen, self.score.score)

    def is_tap_event(self, event) -> bool:
        """
        Determine if the event is a flap/tap event.

        Args:
            event: Pygame event.

        Returns:
            bool: True if event is a tap/flap.
        """
        m_left, _, _ = pygame.mouse.get_pressed()
        space_or_up = event.type == pygame.KEYDOWN and (
            event.key == pygame.K_SPACE or event.key == pygame.K_UP
        )
        screen_tap = event.type == pygame.FINGERDOWN
        return m_left or space_or_up or screen_tap

    def handle_scene(self, event: Event, *args, **kwargs) -> None:
        """
        Handle an event for all objects in the scene.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if self.is_tap_event(event):
            self.flappy.flap()
        super().handle_scene(event, *args, **kwargs)

    def update_scene(self, deltatime: float, *args, **kwargs) -> None:
        """
        Update all objects in the scene, unless paused.

        Args:
            deltatime (float): Time since last update (ms).
        """

        if self.flappy.collided(self.floor, self.pipes):
            self.gameover()

        for i, pipe in enumerate(self.pipes.upper):
            if self.flappy.crossed(pipe):
                self.score.add()
        super().update_scene(deltatime, *args, **kwargs)
