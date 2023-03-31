from keras.callbacks import ModelCheckpoint
from tensorflow import keras
from keras.layers import Dense, Dropout, LSTM
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import io



batch_size = 128
path = "sherlock.txt"

with io.open(path, encoding="utf-8") as f:
    text = f.read().lower()
text = text.replace("\n", " ")
print("Corpus length:", len(text))

chars = sorted(list(set(text)))
print("Total chars:", len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

maxlen = 60
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i : i + maxlen])
    next_chars.append(text[i + maxlen])
print("Number of sequences:", len(sentences))

x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool_)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool_)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1


filepath = "model_weights_saved.hdf5"

model = keras.Sequential()
model.add(LSTM(256, input_shape=(maxlen, len(chars)), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(len(chars), activation="softmax"))
optimizer = keras.optimizers.RMSprop(learning_rate=0.005)
model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])



def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


epochs = 100


for epoch in range(1, epochs+1):
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min',
                                 save_freq='epoch')
    desired_callbacks = [checkpoint]
    model.load_weights(filepath, by_name=False, skip_mismatch=False, options=None)
    model.fit(x, y, batch_size=batch_size, epochs=1, callbacks=desired_callbacks)





