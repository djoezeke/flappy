import pygame
from xodex.objects.image import Image
from xodex.objects.objects import DrawableObject


class Score(DrawableObject):
    """Game Score"""

    def __init__(self, win_width, win_height):
        self.numbers = [
            Image("assets/images/0.png"),
            Image("assets/images/1.png"),
            Image("assets/images/2.png"),
            Image("assets/images/3.png"),
            Image("assets/images/4.png"),
            Image("assets/images/5.png"),
            Image("assets/images/6.png"),
            Image("assets/images/7.png"),
            Image("assets/images/8.png"),
            Image("assets/images/9.png"),
        ]

        self.width = win_width
        self.height = win_height

        self.y = win_height * 0.1
        self.score = 0

    def set(self, score: int) -> None:
        """Set Score"""
        self.score = score

    def reset(self) -> None:
        """Reset Score"""
        self.score = 0

    def add(self) -> None:
        """Increase Score"""
        self.score += 1
        pygame.mixer.Sound("assets/sounds/point.wav").play()

    def perform_draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        """
        Actual drawing logic. Must be implemented by subclass.

        Args:
            surface (Surface): The Pygame surface to draw on.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        score_digits: list[int] = [int(x) for x in list(str(self.score))]
        images: list[Image] = [self.numbers[digit] for digit in score_digits]
        digits_width = sum(image.rect.width for image in images)
        x_offset = (self.width - digits_width) / 2

        for image in images:
            surface.blit(image.image, (x_offset, self.y))
            x_offset += image.rect.width

    @property
    def rect(self) -> pygame.Rect:
        """rect"""
        score_digits: list[int] = [int(x) for x in list(str(self.score))]
        images: list[Image] = [self.numbers[digit] for digit in score_digits]
        w = sum(image.rect.width for image in images)
        x = (self.width - w) / 2
        h = max(image.rect.height for image in images)
        return pygame.Rect(x, self.y, w, h)
