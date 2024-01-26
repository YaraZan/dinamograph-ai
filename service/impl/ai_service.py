from keras.src.layers import Conv2D, MaxPooling2D, Dropout
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Dense, Flatten
from PIL import Image
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
import numpy as np
import os
import random
import shutil
from database.database import SessionLocal
from database.models import Marker
from keras.models import load_model

db = SessionLocal()

input_shape = (224, 224, 1)

def augment_image(
        image_path: str,
        output_path: str,
        rotation_angle=2
):
    original_image = Image.open(image_path)

    rotated_image = original_image.rotate(rotation_angle)

    rotated_image.save(output_path)


def balance_dataset(
        images_path='datasets/ready',
        processing_path='datasets/_train'
):
    # If training session isn't started yet, we create `datasets/_train` directory for
    # current training session
    if not os.path.exists(processing_path):
        os.makedirs(processing_path)

    # Variable to count categories' number
    category_counts = {}
    for filename in os.listdir(images_path):
        if filename.endswith(".png"):
            marker_id = int(filename.split('_')[-1].split('.')[0])
            category_counts.setdefault(marker_id, 0)
            category_counts[marker_id] += 1

    # Find the maximum count
    max_count = max(category_counts.values())

    # Copy all files from `datasets/ready` to `datasets/_train`
    for filename in os.listdir(images_path):
        source_file = os.path.join(images_path, filename)
        output_file = os.path.join(processing_path, filename)
        shutil.copy(source_file, output_file)

    # Augment random images from unbalanced categories to equal dataset categories
    for marker_id, count in category_counts.items():
        while count < max_count:
            source_files = [f for f in os.listdir(images_path) if
            int(f.split('_')[-1].split('.')[0]) == marker_id and f.endswith('.png')]

            source_file = os.path.join(images_path, random.choice(source_files))
            output_filename = os.path.join(processing_path, f'д_augmented_{count}_{marker_id}.png')

            augment_image(image_path=source_file, output_path=output_filename)
            count += 1


def preprocess_image(
        image_path: str,
        target_size=(224, 224)
):
    img = Image.open(image_path)
    img = img.resize(target_size)

    img = img.convert('L')

    img_array = image.img_to_array(img)

    img_array = np.expand_dims(img_array, axis=0)

    img_array = preprocess_input(img_array)

    return img_array


def load_data(
        processing_path='datasets/_train',
        training=False
):
    # Balance dataset if its training call
    if training:
        balance_dataset()

    # Train arrays
    x_tr = []
    y_tr = []

    # Push training data
    for filename in os.listdir(processing_path):
        x = preprocess_image(os.path.join(processing_path, filename))
        x = np.squeeze(x, axis=0)

        y = int(filename.split('_')[-1].split('.')[0])

        x_tr.append(x)
        y_tr.append(y)

    return np.array(x_tr), np.array(y_tr)


def create_new_model(
        version_name: str
):
    x_train, y_train = load_data(training=True)

    classes = sorted(list(set(y_train)))
    num_classes = len(classes)

    model = Sequential()

    # Convolutional layers
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))

    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))

    # Flatten layer to transition from convolutional layers to dense layers
    model.add(Flatten())

    # Dense layers
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))  # Optional dropout for regularization
    model.add(Dense(256, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))  # Output layer

    # Compile the model
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    # Print a summary of the model architecture
    model.summary()

    # Train the model (x_train and y_train are assumed to be your training data)
    model.fit(x_train, LabelEncoder().fit_transform(y_train), epochs=35, validation_split=0.2)

    # Save the model
    model.save(f'd_models/{version_name}.h5')


def predict(
        model_name: str,
        file_to_predict: str
):
    x_train, y_train = load_data()

    classes = sorted(list(set(y_train)))

    model = load_model(f'd_models/{model_name}.h5')

    prediction = model.predict(preprocess_image(file_to_predict))

    file_class = int(file_to_predict.split('_')[-1].split('.')[0])
    prediction_class = int(classes[np.argmax(prediction)])

    predicted_class = db.query(Marker).filter(Marker.id == prediction_class).first()
    actual_class = db.query(Marker).filter(Marker.id == file_class).first()

    print("Нейросеть думает что это: ", predicted_class.name.split('_'))
    print("На самом деле это: ", actual_class.name.split('_'))

    return { "prediction": predicted_class.name, "actual": actual_class.name }


# for f in os.listdir('datasets/_train'):
#     predict('d_v1', f'datasets/_train/{f}')