import numpy as np

from pgm_image import PGMImage

# Parent class


class Transformer:
    def transform(self, image: PGMImage) -> PGMImage:
        raise NotImplementedError(
            "Transform method must be implemented by subclasses")


class InvertTransformer(Transformer):
    def transform(self, image: PGMImage) -> PGMImage:
        inverted_pixels = image.max_gray - image.pixels
        return PGMImage(
            width=image.width,
            height=image.height,
            max_gray=image.max_gray,
            pixels=inverted_pixels
        )


class ThresholdTransformer(Transformer):
    def __init__(self, threshold: int):
        self.threshold = threshold

    def transform(self, image: PGMImage) -> PGMImage:
        thresholded_pixels = (image.pixels >= self.threshold) * image.max_gray
        return PGMImage(
            width=image.width,
            height=image.height,
            max_gray=image.max_gray,
            pixels=thresholded_pixels
        )


class BrightnessTransformer(Transformer):
    def __init__(self, brightness_change: int):
        self.brightness_change = brightness_change

    def transform(self, image: PGMImage) -> PGMImage:
        brightened_pixels = image.pixels + self.brightness_change
        brightened_pixels = brightened_pixels.clip(0, image.max_gray)
        return PGMImage(
            width=image.width,
            height=image.height,
            max_gray=image.max_gray,
            pixels=brightened_pixels
        )


class TransposeTransformer(Transformer):
    def transform(self, image: PGMImage) -> PGMImage:
        transposed_pixels = image.pixels.T
        return PGMImage(
            width=image.height,
            height=image.width,
            max_gray=image.max_gray,
            pixels=transposed_pixels
        )


class MirrorTransformer(Transformer):
    def transform(self, image: PGMImage) -> PGMImage:
        mirrored_pixels = np.fliplr(image.pixels)
        return PGMImage(
            width=image.width,
            height=image.height,
            max_gray=image.max_gray,
            pixels=mirrored_pixels
        )
