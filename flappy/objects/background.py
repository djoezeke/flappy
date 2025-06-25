import random
from xodex.objects.image import Image


class Background(Image):
    """Game Background"""

    def __init__(self):
        backgrounds = [
            "assets/images/background-day.png",
            "assets/images/background-night.png",
        ]
        super().__init__(random.choice(backgrounds), (0, 0))
