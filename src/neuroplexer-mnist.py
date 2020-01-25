# With 5 epochs achieved an accuarcy of 98.13%
# With 10 epochs it achieves an accuracy of 98.27%
# With 2 epochs it achieves an accuarcy of 97.52%
from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
import numpy as np

mnist = tf.keras.datasets.mnist

(data_train, label_train), (data_test, label_test) = mnist.load_data()

data_train, data_test = data_train / 255.0, data_test / 255.0

# print(label_train[:100])

# For now, 100 is the True label and 25 the false label
label_train_array = [[] for _ in range(10)]
label_test_array = [[] for _ in range(10)]

for i in range(10):
    # The training data labels
    temp_label = label_train.copy()
    temp_label[temp_label != i] = 25
    temp_label[temp_label == i] = 100

    temp_label[temp_label == 25] = 0
    temp_label[temp_label == 100] = 1

    label_train_array[i] = temp_label.copy()

    # The testing data labels
    temp_label = label_test.copy()
    temp_label[temp_label != i] = 25
    temp_label[temp_label == i] = 100

    temp_label[temp_label == 25] = 0
    temp_label[temp_label == 100] = 1

    label_test_array[i] = temp_label.copy()
    print(temp_label[:25])
# print(len(label_train_array))



# Standard format of the Neural Network for all the digits
standard_model = [tf.keras.layers.Flatten(input_shape=(28,28)),
                  tf.keras.layers.Dense(128, activation='relu'),
                  tf.keras.layers.Dropout(0.2),
                  tf.keras.layers.Dense(2, activation='softmax')]


def create_model():
    model = tf.keras.models.Sequential([tf.keras.layers.Flatten(input_shape=(28,28)),
                                        tf.keras.layers.Dense(128, activation='relu'),
                                        tf.keras.layers.Dropout(0.2),
                                        tf.keras.layers.Dense(2, activation='softmax')])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

print(label_test_array[2][:25])
print(label_test[:25])
all_digit_models = [[] for _ in range(10)]
for j in range(10):
    all_digit_models[j] = create_model()
    all_digit_models[j].fit(data_train, label_train_array[j], epochs=1)
    print("\n\n\nCurrently on Digit: ", j, "\n\n\n")

predictions_of_all_models = [[] for _ in range(10)]
for k in range(10):
    all_digit_models[k].evaluate(data_test, label_test_array[k], verbose=2)
    predictions_of_all_models[k] = all_digit_models[k].predict(data_test)

digit_guessed = []
for digit_index in range(len(label_test)):
    highest_correct = 0
    index_of_the_highest = 0
    for index in range(10):
        temp = predictions_of_all_models[index][digit_index][1]
        if highest_correct <= temp:
            highest_correct = temp
            index_of_the_highest = index
    digit_guessed.append(index_of_the_highest)

total_right = 0
for compare in range(len(label_test)):
    if digit_guessed[compare] == label_test[compare]:
        total_right += 1

print("Accuarcy: ", total_right / len(label_test))

# For further improvements, I should feed the predictions into their own neural network
print(predictions_of_all_models[:][0].shape)
