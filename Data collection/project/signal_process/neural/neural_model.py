# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 18:12:33 2019

@author: umesh
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import pickle

from sklearn.model_selection import train_test_split


import keras
from keras.models import Sequential
from keras.layers import Dense

from sklearn.metrics import confusion_matrix

dataset = pd.read_csv('A:\\CC\\Final\\training_data_modified.csv')

X = dataset.iloc[:, 0:3].values
Y = dataset.iloc[:, 3].values

print(X.shape)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2)

classifier = Sequential()


classifier.add(Dense(output_dim = 6, init = 'uniform', activation = 'relu', input_dim = 3))
# Adding the second hidden layer
classifier.add(Dense(output_dim = 6, init = 'uniform', activation = 'relu'))
# Adding the output layer
classifier.add(Dense(output_dim = 1, init = 'uniform', activation = 'sigmoid'))

classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

classifier.fit(X_train, y_train, batch_size = 5, nb_epoch = 200)


pickle.dump(classifier, open("neural_model", 'wb'))



y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)

single_val = np.asarray(X_test[0]).reshape(1,3)

print(single_val.shape)
cm = confusion_matrix(y_test, y_pred)

classifier.save("classifier.sav")