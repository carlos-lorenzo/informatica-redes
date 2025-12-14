from image_reader import PGMReader
from image_visualiser import ImageVisualiser
from image_transformer import InvertTransformer, ThresholdTransformer, BrightnessTransformer, TransposeTransformer, MirrorTransformer


if __name__ == "__main__":
    reader = PGMReader('Practica7/images/brain.pgm')
    image_data = reader.read()

    # Invert Transformation
    invert_transformer = InvertTransformer()
    inverted_image = invert_transformer.transform(image_data)
    print("Inverted Image - Max Gray:", inverted_image.max_gray)

    # Threshold Transformation
    threshold_transformer = ThresholdTransformer(threshold=128)
    thresholded_image = threshold_transformer.transform(image_data)
    print("Thresholded Image - Max Gray:", thresholded_image.max_gray)

    # Brightness Transformation
    brightness_transformer = BrightnessTransformer(brightness_change=50)
    brightened_image = brightness_transformer.transform(image_data)
    print("Brightened Image - Max Gray:", brightened_image.max_gray)

    transpose_transformer = TransposeTransformer()
    transposed_image = transpose_transformer.transform(image_data)

    mirror_transformer = MirrorTransformer()
    mirrored_image = mirror_transformer.transform(image_data)

    visualiser = ImageVisualiser(mirrored_image)
    visualiser.run()
