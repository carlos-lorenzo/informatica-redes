import numpy as np

from pgm_image import PGMImage


class PGMReader:
    def __init__(self, filename):
        self.filename = filename

    def read(self) -> PGMImage:
        width = 0
        height = 0
        max_gray = 0
        pixels = np.array([])

        with open(self.filename, 'r') as f:
            # Read magic number
            magic_number = f.readline().strip()
            if magic_number != 'P2':
                raise ValueError("Not a valid PGM P2 file")

            # Read width and height
            dimensions = f.readline().strip()
            while dimensions.startswith('#'):  # Skip comments
                dimensions = f.readline().strip()
            width, height = map(int, dimensions.split())

            # Read max gray value
            max_gray_line = f.readline().strip()

            while max_gray_line.startswith('#'):  # Skip comments
                max_gray_line = f.readline().strip()
            max_gray = int(max_gray_line)

            # Read pixel data
            data = f.read()
            pixels = np.array(
                list(map(int, data.split()))
            ).reshape((height, width))

        return PGMImage(
            width=width,
            height=height,
            max_gray=max_gray,
            pixels=pixels
        )


if __name__ == "__main__":
    reader = PGMReader('Practica7/images/brain.pgm')
    image_data = reader.read()

    print(f"Width: {image_data.width}")
    print(f"Height: {image_data.height}")
    print(f"Max Gray: {image_data.max_gray}")
    print(f"Number of Pixels: {len(image_data.pixels)}")
