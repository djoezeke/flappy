import random
from enum import IntEnum

import pygame
from pygame.event import Event

from xodex.game.sounds import Sounds
from xodex.objects.animator import Animator
from xodex.objects.objects import DrawableObject, EventfulObject, LogicalObject


def clamp(n: float, minn: float, maxn: float) -> float:
    """Clamp a number between two values."""
    return max(min(maxn, n), minn)


class PlayerMode(IntEnum):
    """Enumeration for Flappy's movement modes."""

    SHM = 1
    NORMAL = 2
    CRASH = 3


class Bird(Animator):
    """
    Bird class handles the animated sprite for the player character.

    Args:
        x (int): Initial x position.
        y (int): Initial y position.
    """

    def __init__(self, x=50, y=256):
        bird_sprites = [
            [
                "assets/images/bluebird-downflap.png",
                "assets/images/bluebird-midflap.png",
                "assets/images/bluebird-upflap.png",
            ],
            [
                "assets/images/yellowbird-downflap.png",
                "assets/images/yellowbird-midflap.png",
                "assets/images/yellowbird-upflap.png",
            ],
            [
                "assets/images/redbird-downflap.png",
                "assets/images/redbird-midflap.png",
                "assets/images/redbird-upflap.png",
            ],
        ]
        super().__init__(
            random.choice(bird_sprites),
            frame_duration=100,
            loop=True,
            pingpong=False,
            reverse=False,
            on_finish=None,
            pos=(x, y),
        )


class Flappy(DrawableObject, EventfulObject, LogicalObject):
    """
    Flappy is the main player character, handling movement, flapping, and collision.

    Args:
        x (int): Initial x position.
        y (int): Initial y position.
        floor: Floor object for collision.
        pipes: List of pipe objects for collision.
    """

    def __init__(self, win_width, win_height):
        x = int(win_width * 0.2)
        y = int((win_height - 24) / 2)
        self.flappy = Bird(x, y)

        self.min_y = -2 * self.flappy.rect.height
        self.max_y = (win_height * 0.79) - self.flappy.rect.height * 0.75

        self.crash_entity = None
        self.crashed = False
        self.set_mode(PlayerMode.SHM)

    def set_mode(self, mode: PlayerMode) -> None:
        """
        Set the current movement mode for Flappy.

        Args:
            mode (PlayerMode): The mode to set.
        """
        self.mode = mode
        if mode == PlayerMode.NORMAL:
            self.reset_vals_normal()
            Sounds().play("wing")
        elif mode == PlayerMode.SHM:
            self.reset_vals_shm()
        elif mode == PlayerMode.CRASH:
            Sounds().play("hit")
            if self.crash_entity == "pipe":
                Sounds().play("die")
            self.reset_vals_crash()

    def reset_vals_crash(self) -> None:
        self.acc_y = 2
        self.vel_y = 7
        self.max_vel_y = 15
        self.vel_rot = -8

    def reset_vals_normal(self) -> None:
        """Reset physics values for normal gameplay."""
        self.vel_y = -9
        self.max_vel_y = 10
        self.min_vel_y = -8
        self.acc_y = 1
        self.rot = 80
        self.vel_rot = -3
        self.rot_min = -90
        self.rot_max = 20
        self.flap_acc = -9
        self.flapped = False

    def reset_vals_shm(self) -> None:
        """Reset physics values for simple harmonic motion (idle)."""
        self.vel_y = 1
        self.max_vel_y = 4
        self.min_vel_y = -4
        self.acc_y = 0.5

        self.rot = 0
        self.vel_rot = 0
        self.rot_min = 0
        self.rot_max = 0

        self.flap_acc = 0
        self.flapped = False

    def flap(self) -> None:
        """
        Make the bird flap if possible.
        Only works if not in CRASH mode and not at the top of the screen.
        """
        if self.mode == PlayerMode.CRASH:
            return
        if self.flappy.rect.y > self.min_y:
            self.vel_y = self.flap_acc
            self.flapped = True
            # Instantly rotate up on flap
            self.rot = self.rot_max
            Sounds().play("wing")

    def tick_normal(self) -> None:
        """Update position and rotation for normal gameplay mode."""
        if self.vel_y < self.max_vel_y and not self.flapped:
            self.vel_y += self.acc_y
        if self.flapped:
            self.flapped = False

        self.flappy.rect.y = clamp(
            self.flappy.rect.y + self.vel_y, self.min_y, self.max_y
        )

        # Rotate up on flap, then smoothly rotate down as falling
        if self.vel_y < 0:
            self.rot = self.rot_max
        else:
            self.rotate()

    def rotate(self) -> None:
        """Rotate smoothly"""
        self.rot += self.vel_rot
        if self.rot < self.rot_min:
            self.rot = self.rot_min
        elif self.rot > self.rot_max:
            self.rot = self.rot_max

    def tick_crash(self) -> None:
        """Update position and rotation for crash mode."""
        if self.min_y <= self.flappy.rect.y <= self.max_y:
            self.flappy.rect.y = clamp(
                self.flappy.rect.y + self.vel_y, self.min_y, self.max_y
            )
            # Rotate only when it's a pipe crash and bird is still falling
            if self.crash_entity != "floor":
                self.rotate()

        # player velocity change
        if self.vel_y < self.max_vel_y:
            self.vel_y += self.acc_y

    def tick_shm(self) -> None:
        """Update position for idle (SHM) mode."""
        if self.vel_y >= self.max_vel_y or self.vel_y <= self.min_vel_y:
            self.acc_y *= -1
        self.vel_y += self.acc_y
        self.flappy.rect.y += self.vel_y

    def collided(self, floor, pipes) -> bool:
        """
        Check for collision with the floor or pipes.

        Returns:
            bool: True if collision detected, else False.
        """

        # Floor collision
        if self.collide(floor.rect):
            self.crashed = True
            self.crash_entity = "floor"
            return True

        # Pipes collision
        for pipe in pipes.upper:
            if self.collide(pipe.rect):
                self.crashed = True
                self.crash_entity = "pipe"
                return True

        for pipe in pipes.lower:
            if self.collide(pipe.rect):
                self.crashed = True
                self.crash_entity = "pipe"
                return True

        return False

    def collide(self, other) -> bool:
        """collide"""
        return self.flappy.rect.colliderect(other)

    def crossed(self, pipe) -> bool:
        """crossed"""
        return pipe.rect.x <= self.flappy.rect.x < pipe.rect.x - pipe.vel_x

    def perform_draw(self, surface, *args, **kwargs):
        """
        Draw Flappy on the given surface.

        Args:
            surface: Pygame surface.
        """

        image = self.flappy.get_image()
        rotated_image = pygame.transform.rotate(image.image, self.rot)
        rotated_rect = rotated_image.get_rect(center=self.flappy.rect.center)
        surface.blit(rotated_image, rotated_rect)

    def handle_event(self, event: Event, *args, **kwargs) -> None:
        """
        Handle an event for Flappy.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        self.flappy.handle_event(event, *args, **kwargs)

    def perform_update(self, deltatime: float, *args, **kwargs) -> None:
        """
        Update Flappy's state.

        Args:
            deltatime (float): Time since last update in seconds.
        """

        if self.mode == PlayerMode.SHM:
            self.tick_shm()
        elif self.mode == PlayerMode.NORMAL:
            self.tick_normal()
        elif self.mode == PlayerMode.CRASH:
            self.tick_crash()

        self.flappy.perform_update(deltatime, *args, **kwargs)
