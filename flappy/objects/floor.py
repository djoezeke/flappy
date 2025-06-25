from xodex.objects.image import Image


class Floor(Image):
    """Game Fooor"""

    def __init__(self, win_width):
        super().__init__("assets/images/base.png", pos=(0, int(512 * 0.79)))
        self.vel_x = 4
        self.x_extra = self._img_rect.width - win_width

    def perform_draw(self, surface, *args, **kwargs):
        self._img_rect.x = -((-self._img_rect.x + self.vel_x) % self.x_extra)
        return super().perform_draw(surface, *args, **kwargs)

    @property
    def rect(self):
        return self._img_rect
