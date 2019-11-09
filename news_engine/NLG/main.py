# -*- coding: utf-8 -*-
"""
@Author    : wfs2010
@Email     : 1337581543@qq.com
@License   : Copyright(C), KEDACOM
@Time      : 2019/11/2 下午11:47
@File      : main.py
@Version   : 1.0
@Desciption:  
"""

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.utils import np_utils


def create_model(x,y,z):
    model = Sequential()
    model.add(LSTM(400, input_shape=(x,y), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(400,return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(400))
    model.add(Dropout(0.2))
    model.add(Dense(z, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model

def train():
    text = (open("./toge_all.txt").read())
    characters = sorted(list(set(text)))
    n_to_char = {n: char for n, char in enumerate(characters)}
    char_to_n = {char: n for n, char in enumerate(characters)}
    X = []
    Y = []
    length = len(text)
    seq_length = 100
    for i in range(0, length - seq_length, 1):
        sequence = text[i:i + seq_length]
        label = text[i + seq_length]
        X.append([char_to_n[char] for char in sequence])
        Y.append(char_to_n[label])
    X_modified = np.reshape(X, (len(X), seq_length, 1))
    X_modified = X_modified / float(len(characters))
    Y_modified = np_utils.to_categorical(Y)
    model = create_model(X_modified.shape[1], X_modified.shape[2],Y_modified.shape[1])
    model.fit(X_modified, Y_modified, epochs=1, batch_size=30)
    model.save_weights('./text_generator_400_0.2_400_0.2_400_0.2_100.h5')


def create_text():
    text = (open("./toge_all.txt").read())
    characters = sorted(list(set(text)))
    n_to_char = {n: char for n, char in enumerate(characters)}
    char_to_n = {char: n for n, char in enumerate(characters)}
    X = []
    Y = []
    length = len(text)
    seq_length = 100
    for i in range(0, length - seq_length, 1):
        sequence = text[i:i + seq_length]
        label = text[i + seq_length]
        X.append([char_to_n[char] for char in sequence])
        Y.append(char_to_n[label])
    string_mapped = X[19]
    print(string_mapped)
    full_string = [n_to_char[value] for value in string_mapped]
    X_modified = np.reshape(X, (len(X), seq_length, 1))
    X_modified = X_modified / float(len(characters))
    Y_modified = np_utils.to_categorical(Y)
    model = create_model(X_modified.shape[1], X_modified.shape[2],Y_modified.shape[1])
    model.load_weights('./text_generator_400_0.2_400_0.2_400_0.2_100.h5')
    # generating characters
    for i in range(80):
        x = np.reshape(string_mapped, (1, len(string_mapped), 1))
        x = x / float(len(characters))
        pred_index = np.argmax(model.predict(x, verbose=0))
        seq = [n_to_char[value] for value in string_mapped]
        full_string.append(n_to_char[pred_index])
        string_mapped.append(pred_index)
        string_mapped = string_mapped[1:len(string_mapped)]
    # combining text
    txt = ""
    for char in full_string:
        txt = txt + char
    print(txt)
if __name__=="__main__":
    create_text()