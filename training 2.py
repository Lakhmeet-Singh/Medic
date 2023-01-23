import nltk
import tensorflow as tf
import json
import pickle
import random
import numpy as np
import pandas as pd

from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.layers import Dense, activation, Dropout
from keras.optimizers import SGD

data_file = open('Pharmacy test.json').read()
intents = json.loads(data_file)

lemmatizer = WordNetLemmatizer()

words = []
classes = []
documents = []
ignore_words = ['?', '!', '.', ',']

for intent in intents['intents']:
    if 'Questions' in intent:
        questions = intent['Questions']
        for question in questions:
            word_list = nltk.word_tokenize(question)
            words.extend(word_list)
            documents.append((word_list, 'question'))
            classes.append('question')
    if all(key in intent for key in ("Address", "OrganisationName", "Area", "Phone", "Website", "Email")):
        address = intent["Address"]
        name = intent["OrganisationName"]
        area = intent["Area"]
        phone = intent["Phone"]
        website = intent["Website"]
        email = intent["Email"]
        word_list = nltk.word_tokenize(address + name + area + phone + website + email)
        words.extend(word_list)
        documents.append((word_list, 'response'))
        classes.append('response')

# lemmatize and lower each word and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))  # sort words
classes = sorted(list(set(classes)))  # sort classes

# documents = combination between patterns and intents
print(len(documents), "documents")
# classes = intents
print(len(classes), "classes", classes)
# words = all words, vocabulary
print(len(words), "unique lemmatized words", words)

pickle.dump(words, open('texts.pkl', 'wb'))
pickle.dump(classes, open('labels.pkl', 'wb'))

# Machine Learning


training = []  # create our training data
output_empty = [0] * len(classes)  # create an empty array for our output

# training set, bag of words for each sentence
for doc in documents:
    bag = []  # initialize our bag of words
    pattern_words = doc[0]  # list of tokenized words for the pattern
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in
                     pattern_words]  # lemmatize each word - create base word, in attempt to represent related words

    # create our bag of words array with 1, if word match found in current pattern
    for wordList in words:
        bag.append(1) if wordList in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

# shuffle our features and turn into np.array
random.shuffle(training)
Data_type = object
training = np.array(training, dtype=Data_type)

# Neural Network Model


# create train and test lists. X - patterns, Y - intents
train_x = list(training[:, 0])
train_y = list(training[:, 1])
print("Training data created")

# Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of
# neurons equal to number of intents to predict output intent with softmax
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
SGD = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=SGD, metrics=['accuracy'])

# fitting and saving the model
HIST = model.fit(np.array(train_x), np.array(train_y), epochs=10, batch_size=5, verbose=1)
model.save('model.h5', HIST)

print("model created")
