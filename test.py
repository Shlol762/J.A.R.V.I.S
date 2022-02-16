import random
import string
import json
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Dense, Dropout
import tensorflow as tf

# nltk.download("punkt")
# nltk.download("wordnet")


with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/patterns.json", "r") as f:
    data: dict = json.load(f)

lemmatizer = WordNetLemmatizer()

words = []
classes = []
doc_X = []
doc_y = []
# Loop through all the intents
# tokenize each pattern and append tokens to words, the patterns and
# the associated tag to their associated list
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        tokens = nltk.word_tokenize(pattern)
        words.extend(tokens)
        doc_X.append(pattern)
        doc_y.append(intent["tag"])

    # add the tag to the classes if it's not there already
    if intent["tag"] not in classes:
        classes.append(intent["tag"])
# lemmatize all the words in the vocab and convert them to lowercase
# if the words don't appear in punctuation
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in string.punctuation]
# sorting the vocab and classes in alphabetical order and taking the # set to ensure no duplicates occur
words = sorted(set(words))
classes = sorted(set(classes))
#
#
training = []
out_empty = [0] * len(classes)
# creating the bag of words model
for _idx, doc in enumerate(doc_X):
    _bow = []
    text = lemmatizer.lemmatize(doc.lower())
    for word in words:
        _bow.append(1) if word in text else _bow.append(0)
    # mark the index of class that the current pattern is associated
    # to
    output_row = list(out_empty)
    output_row[classes.index(doc_y[_idx])] = 1
    # add the one hot encoded BoW and associated classes to training
    training.append([_bow, output_row])
# shuffle the data and convert it to an array
random.shuffle(training)
training = np.array(training, dtype=object)
# split the features and target labels
train_X = np.array(list(training[:, 0]))
train_y = np.array(list(training[:, 1]))

input_shape = (len(train_X[0]),)
output_shape = len(train_y[0])
epochs = 200
# the deep learning model
model = Sequential()
model.add(Dense(128, input_shape=input_shape, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(output_shape, activation = "softmax"))
adam = tf.keras.optimizers.Adam(learning_rate=0.01, decay=1e-6)
model.compile(loss='categorical_crossentropy',
              optimizer=adam,
              metrics=["accuracy"])
print(model.summary())
model.fit(x=train_X, y=train_y, epochs=20000, verbose=1)
model.save('C:/Users/Shlok/Desktop/chatbot-model1.h5')

# model = load_model('C:/Users/Shlok/Desktop/chatbot-model1.h5')
#
#
# def clean_text(_text):
#     _tokens = nltk.word_tokenize(_text)
#     _tokens = [lemmatizer.lemmatize(word) for word in _tokens]
#     return _tokens
#
#
# def bag_of_words(_text, vocab):
#     _tokens = clean_text(_text)
#     bow = [0] * len(vocab)
#     for w in _tokens:
#         for idx, word in enumerate(vocab):
#             if word == w:
#                 bow[idx] = 1
#     return np.array(bow)
#
#
# def pred_class(_text, vocab, labels):
#     bow = bag_of_words(_text, vocab)
#     result = model.predict(np.array([bow]))[0]
#     thresh = 0.2
#     y_pred = [[idx, res] for idx, res in enumerate(result) if res > thresh]
#
#     y_pred.sort(key=lambda x: x[1], reverse=True)
#     return_list = []
#     for r in y_pred:
#         return_list.append(labels[r[0]])
#     return return_list
#
#
# def get_response(intents_list, intents_json):
#     tag = intents_list[0]
#     list_of_intents = intents_json["intents"]
#     for i in list_of_intents:
#         if i["tag"] == tag:
#             result = random.choice(i["responses"])
#             break
#     return result
#
#
# while True:
#     message = input("").lower()
#     intents = pred_class(message, words, classes)
#     _result = get_response(intents, data)
#     print(_result, intents)
