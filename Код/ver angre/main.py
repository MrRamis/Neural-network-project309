from tensorflow import keras #из tensorflow() берем keras
from keras.callbacks import ModelCheckpoint #это нужно для сохранения прогресса обучения нейронки после каждой эпохи

from tensorflow.keras import layers # это нужно для построения слоев и архитнктуры нейронки

import numpy as np # нужна для работы с векторами
import random
import io#предоставляет основные возможности Python для работы с различными типами ввода-вывода
#nltk это пакет библиотек и программ для символьной и статистической обработки естественного языка

from keras.layers import Dense, Dropout, LSTM #нужно для постройки модели нейросети

batch_size = 128
path = "te.txt"

with io.open(path, encoding="utf-8") as f:
    text = f.read().lower()
text = text.replace("\n", " ")
print("Corpus length:", len(text))

chars = sorted(list(set(text)))
print("Total chars:", len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

maxlen = 100
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print("Number of sequences:", len(sentences))

x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool_)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool_)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

#model = keras.Sequential(
    #[
        #keras.Input(shape=(maxlen, len(chars))),
        #layers.LSTM(128),
        #layers.Dense(len(chars), activation="softmax"),
    #]
#)
model = keras.Sequential()
model.add(LSTM(256, input_shape=(maxlen, len(chars)), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(128))
#model.add(Dropout(0.2))
#model.add(LSTM(64))
model.add(Dropout(0.2))
model.add(Dense(len(chars), activation="softmax"))

#optimizer = keras.optimizers.Adam(learning_rate=0.01) медленный оптимайзер

optimizer = keras.optimizers.RMSprop(learning_rate=0.005)#optimizer = keras.optimizers.SGD(momentum=0.5, nesterov=True, learning_rate=0.5)#optimizer = keras.optimizers.Adagrad(learning_rate=0.1)
model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics='accuracy')

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

epochs = 2
filepath = "model_weights_saved.hdf5"

for epoch in range(1, epochs + 1):

    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min',
                                 save_freq='epoch')
    desired_callbacks = [checkpoint]
    #подгрузка файла обученного
    model.load_weights(filepath, by_name=False, skip_mismatch=False, options=None)
    model.fit(x, y, batch_size=batch_size, epochs=1, callbacks=desired_callbacks)

    print()
    print("Generating text after epoch: %d" % epoch)

    start_index = random.randint(0, len(text) - maxlen - 1)
for diversity in [0.2, 0.5, 1.0, 1.2]:
    print("...Diversity:", diversity)

    generated = ""
    sentence = text[start_index: start_index + maxlen]
    print('...Generating with seed: "' + sentence + '"')

    for i in range(400):
        x_pred = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sentence):
            x_pred[0, t, char_indices[char]] = 1.0
        preds = model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_char = indices_char[next_index]
        sentence = sentence[1:] + next_char
        generated += next_char

    print("...Generated: ", generated)
    print()
