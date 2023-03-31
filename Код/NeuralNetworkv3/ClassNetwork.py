from tensorflow import keras
from tensorflow.keras import layers
from keras.layers import Dense, Dropout, LSTM
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import random
import numpy as np
import io


class Neyron:
    def __init__(self, count_chars, model_save, continue_text, path_text):
        self.count_chars = count_chars
        self.path_text = path_text
        self.model_save = model_save
        self.continue_text = continue_text
        with io.open(self.path_text, encoding="utf-8") as f:
            self.text = f.read().lower()
        self.text = self.text.replace("\n", " ")
        self.chars = sorted(list(set(self.text)))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))
        self.maxlen = 100
        self.Load_Model()

    def Load_Model(self):
        self.model = keras.Sequential()
        self.model.add(LSTM(256, input_shape=(self.maxlen, len(self.chars)), return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(256))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(len(self.chars), activation="softmax"))

        self.optimizer = keras.optimizers.RMSprop(
            learning_rate=0.005)
        self.model.compile(loss="categorical_crossentropy", optimizer=self.optimizer, metrics='accuracy')
        self.model.load_weights(self.model_save, by_name=False, skip_mismatch=False, options=None)

    def sample(self, preds, temperature=1.0):
        preds = np.asarray(preds).astype("float64")
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    def Set_text(self):
        start_index = random.randint(0, len(self.text) - self.maxlen - 1)
        generated = ""
        if(self.continue_text !=""):
            sentence = self.text[start_index: start_index + self.maxlen]
        else:
            sentence = self.continue_text[start_index: start_index + self.maxlen]

        for i in range(self.count_chars):
            x_pred = np.zeros((1, self.maxlen, len(self.chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, self.char_indices[char]] = 1.0
            preds = self.model.predict(x_pred, verbose=0)[0]
            next_index = self.sample(preds, 1.4)
            next_char = self.indices_char[next_index]
            sentence = sentence[1:] + next_char
            generated += next_char

        return generated