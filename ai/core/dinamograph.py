from typing import List, Any

import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.src.layers import Conv2D, MaxPooling2D, Dropout
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.models import load_model

from ai.helpers.data_helper import DataHelper
from ai.helpers.image_helper import ImageHelper

"""
*   Dinamograph-AI v1.0
*
*   Copyright (C) 2024 Potemkin Yaroslav
*
"""

# ImageHelper instance
image_helper = ImageHelper()

# DataHelper instance
data_helper = DataHelper()


def create_model(
        model_name: str,
        input_shape: tuple = (224, 224, 1),
):
    model = Sequential()

    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))

    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))

    model.add(Flatten())

    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(1, activation='softmax'))

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'],
    )

    model.save(f'ai/versions/{model_name}.h5')


def train(model_name: str, epochs: int = 35):
    x, y = data_helper.load_data()

    model = load_model(f'ai/versions/{model_name}.h5')

    model.fit(x, LabelEncoder().fit_transform(y), epochs=epochs, validation_split=0.2)

    model.save(f'ai/versions/{model_name}.h5')

    return sorted(list(set(y)))


def predict(model_name: str, image_bytes: bytes):
    model = load_model(f'ai/versions/{model_name}.h5')

    prediction = model.predict(image_helper.preprocess_image(image_bytes=image_bytes))

    return np.argmax(prediction)
