from xodex.scenes import Scene


class GameScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _generate_objects_(self):
        Floor = self.object.Floor
        Flappy = self.object.Flappy
        Background = self.object.Background

        yield Background()
        yield Floor()
        yield Flappy()
