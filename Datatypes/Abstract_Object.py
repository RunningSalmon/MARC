import numpy as np

class AbstractObject:
    Position_X: int
    Position_Y: int
    Shape = np.ndarray
    Colour = int

    def __init__(self, position: tuple[int, int], shape: np.ndarray, colour: int):
        self.Position_X = position[0]
        self.Position_Y = position[1]
        self.Shape = shape
        if colour not in set(range(10)):
            raise ValueError(f"Colour {colour} is not a valid colour")
        self.Colour = colour
