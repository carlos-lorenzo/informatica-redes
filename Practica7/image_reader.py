class PGMReader:
    def __init__(self, filename):
        self.filename = filename
        self.width = 0
        self.height = 0
        self.max_gray = 0
        self.min_gray = 0
        self.pixels = []

    def read(self):

        with open(self.filename, 'r') as f:
            # Read magic number
            magic_number = f.readline().strip()
            if magic_number != 'P2':
                raise ValueError("Not a valid PGM P2 file")

            # Read width and height
            dimensions = f.readline().strip()
            while dimensions.startswith('#'):  # Skip comments
                dimensions = f.readline().strip()
            self.width, self.height = map(int, dimensions.split())

            # Read max gray value
            max_gray_line = f.readline().strip()

            while max_gray_line.startswith('#'):  # Skip comments
                max_gray_line = f.readline().strip()
            self.max_gray = int(max_gray_line)
            self.min_gray = 0

            # Read pixel data

            data = f.read()
            self.pixels = list(
                map(int, data.split())
            )

    def get_image_data(self):
        return {
            'width': self.width,
            'height': self.height,
            'max_gray': self.max_gray,
            'pixels': self.pixels
        }


if __name__ == "__main__":
    reader = PGMReader('Practica7/images/brain.pgm')
    reader.read()
    image_data = reader.get_image_data()
    print(f"Width: {image_data['width']}")
    print(f"Height: {image_data['height']}")
    print(f"Max Gray: {image_data['max_gray']}")
    print(f"Number of Pixels: {len(image_data['pixels'])}")
