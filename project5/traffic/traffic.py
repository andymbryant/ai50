import cv2
import numpy as np
import os
import sys
from tensorflow.keras import layers, models
import tensorflow as tf
from PIL import Image
import pathlib
import datetime
from sklearn.model_selection import train_test_split

EPOCHS = 16
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4

# Set seed to ensure consistent results
# Use numpy to set seed for tensorflow then set seed in tensorflow as well
np.random.seed(123)
tf.random.set_seed(456)

def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []
    root_dir = os.path.join(data_dir)
    # use os module to walk through root directory
    for subdir, dirs, files in os.walk(root_dir):
        # loop through files
        for file in files:
            filepath = os.path.join(subdir, file)
            extension = pathlib.Path(filepath).suffix
            # only work with ppm files
            if extension == '.ppm':
                # read in images and resize them according to project specs
                img = cv2.imread(filepath)
                res = cv2.resize(img, dsize=(IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_CUBIC)
                # ensure images are represented as arrays
                data = np.asarray(res, dtype="float64")
                images.append(data)
                # avoid using root data directory
                if subdir != 'data':
                    # get subdir in a platform-agnostic way
                    head, sep, cat = subdir.partition(os.sep)
                    cat_int = int(cat)
                    labels.append(cat_int)
    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # Initialize model
    model = models.Sequential()
    # Add three convolutional layers with max pooling added
    # Use relu activation for optimal training for image classification - see readme for more info
    model.add(layers.Conv2D(30, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(60, (2, 2), activation='relu'))
    model.add(layers.MaxPooling2D((1, 1)))
    model.add(layers.Conv2D(120, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    # Flatten to make shape of input to final dense layers match expected output of compile
    model.add(layers.Flatten())
    model.add(layers.Dense(NUM_CATEGORIES * 3, activation='relu'))
    # Optimal dropout rate
    model.add(layers.Dropout(0.50))
    model.add(layers.Dense(NUM_CATEGORIES))
    model.compile(optimizer='adam', rate=0.0001, loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True), metrics=['accuracy', 'mse'])
    model.summary()
    return model


if __name__ == "__main__":
    main()
