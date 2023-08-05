from __future__ import with_statement
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
import pickle as pkl
import gzip
import re
import os
import json
import keras
import scipy as sp
from keras.layers import *
from keras.models import Sequential
import wordbatch
from wordbatch.extractors import WordSeq
import random
import threading
from keras.models import load_model

non_alphas = re.compile('[^A-Za-z\'-]+')
trash_re= [re.compile("<[^>]*>"), re.compile("[^a-z0-9' -]+"), re.compile(" [.0-9'-]+ "),
           re.compile("[-']{2,}"),re.compile(" '"),re.compile("  +")]

def normalize_text(text):
    text= text.lower()
    for x in trash_re:
        while x.search(text) != None:  text = x.sub(" ", text)
    return non_alphas.sub(' ', text).strip()

class BatchData(object):
    def __init__(self):
        self.texts= None
        self.labels= None

class WordseqRegressor():
    def __init__(self, pickle_model="", datadir=None):
        self.maxlen = 200
        self.n_words = 20000
        self.wb= wordbatch.WordBatch(normalize_text, n_words=self.n_words,
                                             extractor=(WordSeq, {"seq_maxlen": self.maxlen}))
        self.model = Sequential()
        self.model.add(Embedding(self.n_words,
                            100,
                            input_length=self.maxlen))

        self.model.add(Conv1D(activation="relu", padding="same", strides=1, filters=64, kernel_size=3))
        self.model.add(Dropout(0.5)) #0.343497256609
        self.model.add(BatchNormalization())
        self.model.add(GlobalMaxPooling1D())
        self.model.add(Dense(1))
        self.model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_squared_error'])
        if datadir == None:
            self.model= load_model(pickle_model)
            self.wb= pkl.load(gzip.open(pickle_model + ".wb", 'rb'))
        else: self.train(datadir, pickle_model)

    def transform_batch(self, texts, batch_data):
        batch_data.texts= self.wb.transform(texts)

    def train(self, datadir, pickle_model=""):
        texts= []
        labels= []
        training_data = os.listdir(datadir)
        rcount= 0
        texts2= []
        batchsize= 100000

        batch_data = BatchData()
        p_input= None
        for jsonfile in training_data:
            with open(datadir + "/" + jsonfile, 'r') as inputfile:
                for line in inputfile:
                    #if rcount > 1000000: break
                    try: line= json.loads(line.strip())
                    except:  continue
                    for review in line["Reviews"]:
                        rcount+= 1
                        if rcount % 100000 == 0:  print(rcount)
                        if rcount % 8 != 0: continue
                        if "Overall" not in review["Ratings"]: continue
                        texts.append(review["Content"])
                        labels.append((float(review["Ratings"]["Overall"]) - 3) *0.5)
                        if len(texts) % batchsize == 0:
                            if p_input != None:
                                p_input.join()
                                texts2.append(batch_data.texts)
                            p_input = threading.Thread(target=self.transform_batch, args=(texts, batch_data))
                            p_input.start()
                            texts= []
        if p_input != None:
            p_input.join()
            texts2.append(batch_data.texts)
        texts2.append(self.wb.transform(texts))
        del(texts)
        texts= sp.vstack(texts2)
        self.wb.dictionary_freeze = True
        test= [texts[-1000:], labels[-1000:]]
        train = [texts[:-1000], labels[:-1000]]

        self.model.fit(train[0], train[1], batch_size=2048, epochs=10, validation_data=(test[0], test[1]))
        if pickle_model != "":
            self.model.save(pickle_model)
            with gzip.open(pickle_model + ".wb", 'wb') as model_file:  pkl.dump(self.wb, model_file, protocol=2)

    def predict_batch(self, texts):
        results= [x[0] for x in self.model.predict(self.wb.transform(texts))]
        return results
