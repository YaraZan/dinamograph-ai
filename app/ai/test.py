import os

import numpy as np
from keras.models import load_model
from ai import preprocess_image
from ai import classes

model = load_model('d_models/d_v1.h5')

first_to_predict = 'datasets/_train' + '/' + os.listdir('datasets/_train')[1]

prediction = model.predict(preprocess_image(first_to_predict))

print("Predicted Class:", classes[np.argmax(prediction)])
print("Actual Class:", int(os.listdir('datasets/_train')[1].split('_')[-1].split('.')[0]))

print(prediction)
print(classes)