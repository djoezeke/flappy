"""
Objects Registration for FLAPPY project.

Register your custom game objects here using the @register decorator.

Example:

Registering Object On Creation.

    ```python
    from xodex.objects.manager import register
    from xodex.objects import LogicalObject, DrawableObject, EventfulObject

    # Register a button object with default name (class name)
    @register
    class Button(LogicalObject, DrawableObject, EventfulObject):
        ...

    # Register a text object with a custom name
    @register(name="text")
    class Text(DrawableObject, EventfulObject):
        ...
    ```

Registering Existing Objects.

    ```python
    from xodex.objects.manager import register
    from .text import Text

    # Register a text object with default name (class name)
    register(Text)

    # Register a text object with a custom name
    register(Text,name="text")
    ```

How it works:
- The @register decorator adds your object class to the global registry.
- You can then instantiate or reference these objects by name in your scenes or game logic.
- Use multiple inheritance to combine logic, drawing, and event features as needed.

See the Xodex documentation for more advanced usage and patterns.
"""

from xodex.objects.manager import register

# Register your flappy Objects here.

from .background import Background
from .flappy import Flappy, Bird
from .floor import Floor
from .score import Score
from .pipes import Pipes

register(Background, name="Background")
register(Flappy, name="Flappy")
register(Floor, name="Floor")
register(Score, name="Score")
register(Pipes, name="Pipes")
register(Bird, name="Bird")
