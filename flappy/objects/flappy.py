import random
from enum import Enum
import pygame
from pygame.event import Event
from xodex.objects.animator import Animator


def clamp(n: float, minn: float, maxn: float) -> float:
    """Clamps a number between two values"""
    return max(min(maxn, n), minn)


class PlayerMode(Enum):
    SHM = "SHM"
    NORMAL = "NORMAL"
    CRASH = "CRASH"


class Flappy(Animator):
    def __init__(
        self,
        frame_duration=100,
        loop=True,
        pingpong=False,
        reverse=False,
        on_finish=None,
        **kwargs
    ):

        flappy = [
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
            random.choice(flappy),
            frame_duration,
            loop,
            pingpong,
            reverse,
            on_finish,
            pos=(50, 256),
            **kwargs,
        )

        self.min_y = -2 * 512
        self.max_y = int(512 * 0.79) - int(512 * 0.75)

        self.set_mode(PlayerMode.SHM)

    def set_mode(self, mode: PlayerMode) -> None:
        self.mode = mode

        if mode == PlayerMode.NORMAL:
            self.reset_vals_normal()
            # self.config.sounds.wing.play()
        elif mode == PlayerMode.SHM:
            self.reset_vals_shm()

    def reset_vals_normal(self) -> None:
        self.vel_y = -9  # player's velocity along Y axis
        self.max_vel_y = 10  # max vel along Y, max descend speed
        self.min_vel_y = -8  # min vel along Y, max ascend speed
        self.acc_y = 1  # players downward acceleration

        self.rot = 80  # player's current rotation
        self.vel_rot = -3  # player's rotation speed
        self.rot_min = -90  # player's min rotation angle
        self.rot_max = 20  # player's max rotation angle

        self.flap_acc = -9  # players speed on flapping
        self.flapped = False  # True when player flaps

    def reset_vals_shm(self) -> None:
        self.vel_y = 1  # player's velocity along Y axis
        self.max_vel_y = 4  # max vel along Y, max descend speed
        self.min_vel_y = -4  # min vel along Y, max ascend speed
        self.acc_y = 0.5  # players downward acceleration

        self.rot = 0  # player's current rotation
        self.vel_rot = 0  # player's rotation speed
        self.rot_min = 0  # player's min rotation angle
        self.rot_max = 0  # player's max rotation angle

        self.flap_acc = 0  # players speed on flapping
        self.flapped = False  # True when player flaps

    def tick_shm(self) -> None:
        if self.vel_y >= self.max_vel_y or self.vel_y <= self.min_vel_y:
            self.acc_y *= -1
        self.vel_y += self.acc_y
        self._img_pos[1] += self.vel_y

    def tick_normal(self) -> None:
        if self.vel_y < self.max_vel_y and not self.flapped:
            self.vel_y += self.acc_y
        if self.flapped:
            self.flapped = False

        self._img_pos[1] = clamp(self._img_pos[1] + self.vel_y, self.min_y, self.max_y)
        # self.rotate()

    def perform_draw(self, surface, *args, **kwargs):

        # if self.mode == PlayerMode.SHM:
        #     self.tick_shm()
        # elif self.mode == PlayerMode.NORMAL:
        #     self.tick_normal()

        super().perform_draw(surface, *args, **kwargs)

    def handle_event(self, event: Event, *args, **kwargs) -> None:
        """
        Handle an event for flappy in the scene.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        # if event.type == pygame.MOUSEBUTTONDOWN:
        # self.flap()
        super().handle_event(event, *args, **kwargs)

    def flap(self) -> None:
        if self._img_pos[1] > self.min_y:
            self.vel_y = self.flap_acc
            self.flapped = True
            self.rot = 80
            pygame.mixer.Sound("assets/sounds/wing.wav").play()

    def rotate(self) -> None:
        self.rot = clamp(self.rot + self.vel_rot, self.rot_min, self.rot_max)
