import io
import os
import random
import shutil
from typing import List, Any

from PIL import Image
from matplotlib import pyplot as plt
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
import numpy as np

from constants.constants import Constants
from ai.helpers.image_helper import ImageHelper

# ImageHelper instance
image_helper = ImageHelper()

# Constants instance
constants = Constants()


class DataHelper:
    """
        Helper class for manipulation with data.

        Includes:
            - balance_dataset: Balance dataset for training
            - load_data: Loads preprocessed data for training

    """
    @staticmethod
    def balance_dataset(
            images_path: str = constants.STORAGE_DATASETS_READY,
            training_path: str = constants.STORAGE_DATASETS_TRAIN
    ):
        """
        Balances dataset if there's a difference between categories count

            Parameters:
                images_path (str): Path to the marked images dataset
                training_path (str): Path to the training directory (created in training process)
        """
        if not os.path.exists(training_path):
            os.makedirs(training_path)

        category_counts = {}
        for filename in os.listdir(images_path):
            if filename.endswith(".png"):
                marker_id = int(filename.split('_')[-1].split('.')[0])
                category_counts.setdefault(marker_id, 0)
                category_counts[marker_id] += 1

        max_count = max(category_counts.values())

        for filename in os.listdir(images_path):
            source_file = os.path.join(images_path, filename)
            output_file = os.path.join(training_path, filename)
            shutil.copy(source_file, output_file)

        for marker_id, count in category_counts.items():
            while count < max_count:
                source_files = [f for f in os.listdir(images_path) if
                                int(f.split('_')[-1].split('.')[0]) == marker_id and f.endswith('.png')]

                source_file = os.path.join(images_path, random.choice(source_files))
                output_filename = os.path.join(training_path, f'д_augmented_{count}_{marker_id}.png')

                image_helper.augment_image(image_path=source_file, output_path=output_filename)
                count += 1

    @staticmethod
    def create_graph(
            x_values: List[Any],
            y_values: List[Any],
            output_filename: str,
            is_colorful: bool = True
    ):
        """
        Creates a plot, based on given data and saves it.

        Parameters:
            x_values (str): Dinamogramm's x values
            y_values (str): Dinamogramm's y values
            output_filename (str): Filename to save
            is_colorful (bool): Boolean variable to indicate in what color save image
        """
        if is_colorful:
            plt.plot(x_values, y_values, marker='o', linestyle='-', color='green', label='graph')
            plt.title('Динамограмма')
            plt.xlabel('Длина')
            plt.ylabel('Нагрузка')
            plt.legend()
            plt.savefig(output_filename, format='png', dpi=300, bbox_inches='tight')
            plt.close()
        else:
            fig, ax = plt.subplots(figsize=(8, 6), facecolor='white')
            ax.plot(x_values, y_values, marker='o', linestyle='-', color='black', markersize=1)
            ax.set_facecolor('white')

            ax.set_title('')
            ax.set_xlabel('')
            ax.set_ylabel('')

            for spine in ax.spines.values():
                spine.set_visible(False)

            ax.set_xticks([])
            ax.set_yticks([])

            fig.savefig(output_filename, format='png', dpi=300, bbox_inches='tight', pad_inches=0.1)
            plt.close()

    @staticmethod
    def create_image_bytes_from_raw(x_values: List, y_values: List):
        """
        Creates a black and white version of the plot and returns the bytes of the created image.

        Parameters:
            x_values (str): Dinamogramm's x values
            y_values (str): Dinamogramm's y values

        Returns:
            bytes: Bytes of the created image
        """
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='white')
        ax.plot(x_values, y_values, marker='o', linestyle='-', color='black', markersize=1)
        ax.set_facecolor('white')

        ax.set_title('')
        ax.set_xlabel('')
        ax.set_ylabel('')

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.set_xticks([])
        ax.set_yticks([])

        image_bytes_io = io.BytesIO()
        fig.savefig(image_bytes_io, format='png', dpi=300, bbox_inches='tight', pad_inches=0.1)
        # plt.show()
        plt.close()

        return image_bytes_io.getvalue()

    def load_data(
            self,
            processing_path: str = constants.STORAGE_DATASETS_TRAIN,
    ):
        """
        Load training data from datasets folder

            Parameters:
                processing_path (str): Path to training process folder
        """
        self.balance_dataset()

        x_tr = []
        y_tr = []

        for filename in os.listdir(processing_path):
            x = image_helper.preprocess_image(is_local=True, image_path=os.path.join(processing_path, filename))
            x = np.squeeze(x, axis=0)

            y = int(filename.split('_')[-1].split('.')[0])

            x_tr.append(x)
            y_tr.append(y)

        return np.array(x_tr), np.array(y_tr)
