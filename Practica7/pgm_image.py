import numpy as np

from dataclasses import dataclass, field


@dataclass
class PGMImage:
    width: int
    height: int
    min_gray: int = field(init=False, default=0)
    max_gray: int
    pixels: np.ndarray = field(default_factory=lambda: np.array([]))

    def __post_init__(self):
        if self.pixels.shape != (self.height, self.width):
            raise ValueError(
                "Pixel data does not match specified width and height")
