import numpy as np

cpdef Set_text(deferences, sentence, indices_char, chars, maxlen, count_chars, text_seed, text, model):
    text_seed = clear_text(text).split()
    generated = ""
    for i in range(count_chars):
        x_pred = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sentence):
            x_pred[0, t, self.char_indices[char]] = 1.0
        preds = model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds, deferences)
        next_char = indices_char[next_index]
        sentence = sentence[1:] + next_char
        generated += next_char
    return generated

def clear_text(result):
    characters = '\''
    result = re.sub(characters, '', result).lower()
    clear = result.split()
    result = " ".join(clear)
    return result

def sample(self, preds, temperature=1.0):
    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)