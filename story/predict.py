import pickle
import numpy as np
from googletrans import Translator

def predict(postingan):
    translator = Translator()
    dt1 = translator.translate(postingan)
    kata = dt1.text

    with open('model_web', 'rb') as f:
        lr1 = pickle.load(f)

    with open('model_web2', 'rb') as f:
        lr = pickle.load(f)

    posting = [kata]
    posting1 = np.array(posting)
    test = lr1.transform(posting1)

    hasil = lr.predict_proba(test)
    persen = (hasil[0][1])*100
    return int(round(persen,2))