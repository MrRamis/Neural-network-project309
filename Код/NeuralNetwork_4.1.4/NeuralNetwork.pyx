from tensorflow import keras
from keras.layers import Dense, Dropout, LSTM
from functools import cache, lru_cache
import os
import random
import numpy as np
import io
import re
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class Neyron:
    @cache
    def __init__(self, count_chars, model_save, continue_text, path_text):
        self.count_chars = count_chars
        self.path_text = path_text
        self.model_save = model_save
        with io.open(self.path_text, encoding="utf-8") as f:
            self.text = f.read().lower()
        self.text = self.text.replace("\n", " ")
        self.continue_text = continue_text
        self.chars = sorted(list(set(self.text)))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))
        if continue_text == "":
            self.sentence = self.clear_text(self.Seed_Text())
            self.maxlen = len(self.sentence)
        elif continue_text != "":
            self.sentence = self.clear_text(continue_text)
            self.maxlen = len(continue_text)

    @cache
    def Load_Model(self):
        self.model = keras.Sequential()
        self.model.add(LSTM(256, input_shape=(self.maxlen, len(self.chars)), return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(256))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(len(self.chars), activation="softmax"))

        self.optimizer = keras.optimizers.RMSprop(
            learning_rate=0.005)
        self.model.load_weights(self.model_save, by_name=False, skip_mismatch=False, options=None)
        self.model.compile(loss="categorical_crossentropy", optimizer=self.optimizer, metrics='accuracy')

    @cache
    def clear_text(self, result):
        characters = '\''
        result = re.sub(characters, '', result).lower()
        cdef list clear = result.split()
        result = " ".join(clear)
        return result

    def sample(self, preds, temperature=1.0):
        preds = np.asarray(preds).astype("float64")
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    @cache
    def Set_text(self, deferences):
        cdef float defe = deferences
        self.model.load_weights(self.model_save, by_name=False, skip_mismatch=False, options=None)
        self.text_seed = self.clear_text(self.text).split()
        generated = ""
        for i in range(self.count_chars):
            x_pred = np.zeros((1, self.maxlen, len(self.chars)))
            for t, char in enumerate(self.sentence):
                x_pred[0, t, self.char_indices[char]] = 1.0
            preds = self.model.predict(x_pred, verbose=0)[0]
            next_index = self.sample(preds, defe)
            next_char = self.indices_char[next_index]
            self.sentence = self.sentence[1:] + next_char
            generated += next_char

        return generated

    @cache
    def Seed_Text(self):
        cdef list seed_text = self.clear_text(self.text).split()
        new_text = " "
        cdef list generated = []
        cdef int start_position = random.randint(0, len(seed_text) - 17)
        for i in range(0, 17):
            generated.append(seed_text[start_position + i])
        new_text = " ".join(generated)
        return new_text


