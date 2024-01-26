import io

from PIL import Image
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
import numpy as np


class ImageHelper:
    """
        Helper class for manipulation with images.

        Used internally to handle image manipulation operations.
    """
    @staticmethod
    def augment_image(
            image_path: str,
            output_path: str,
            rotation_angle=2
    ):
        """
        Augment an image from unbalanced category

            Parameters:
                image_path (str): Path to the image
                output_path (str): Path to the output image
                rotation_angle (int): Rotation angle in degrees
        """
        original_image = Image.open(image_path)

        rotated_image = original_image.rotate(rotation_angle)

        rotated_image.save(output_path)

    @staticmethod
    def preprocess_image(
            image_path: str = None,
            is_local: bool = False,
            image_bytes: bytes = None,
            target_size=(224, 224)
    ):
        """
        Preprocess the image before training or prediction

            Parameters:
                image_bytes (bytes, optional): Bytes representation of the image.
                image_path (str, optional): Path to the image.
                is_local (bool, optional): Whether the image is local or uploaded.
                target_size (tuple(int, int): Target size of image. Defaults to (224, 224).

        """
        if is_local:
            img = Image.open(image_path)
        else:
            img = Image.open(io.BytesIO(image_bytes))

        img = img.resize(target_size)
        img = img.convert('L')

        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        return img_array
