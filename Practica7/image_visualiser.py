from image_reader import PGMReader
from pgm_image import PGMImage

import tkinter as tk


class ImageVisualiser:
    def __init__(self, image_data: PGMImage):
        self.image_data = image_data
        self.window = tk.Tk()
        self.window.title("PGM Image Visualiser")
        self.window.geometry(
            f"{self.image_data.width}x{self.image_data.height}")
        self.canvas = tk.Canvas(
            self.window, width=self.image_data.width, height=self.image_data.height)
        self.canvas.pack()

    @staticmethod
    def greyscale_to_hex(value):
        """Convert a grayscale value (0-255) to a hex color string."""
        hex_value = f"{value:02x}"
        return f"#{hex_value}{hex_value}{hex_value}"

    def draw_image(self):
        for y in range(self.image_data.height):
            for x in range(self.image_data.width):
                colour = ImageVisualiser.greyscale_to_hex(
                    self.image_data.pixels[y][x])
                self.canvas.create_rectangle(
                    x, y, x+1, y+1, fill=colour, outline=colour
                )

    def run(self):
        self.draw_image()
        self.window.mainloop()


if __name__ == "__main__":
    reader = PGMReader('Practica7/images/brain.pgm')
    image_data = reader.read()

    visualiser = ImageVisualiser(image_data)
    visualiser.run()
