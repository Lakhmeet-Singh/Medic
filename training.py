import nltk
import tensorflow as tf
import json
import pickle
import random
import numpy as np

from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

data_file = open('data.json').read()
intents = json.loads(data_file)

lemmatizer = WordNetLemmatizer()

words = []
classes = []
documents = []
ignore_words = ['?', '!','.', ',']


for intent in intents['intents']:
    for pattern in intent['patterns']:
        wordList = nltk.word_tokenize(pattern)      # tokenize each word
        words.extend(wordList)                      # extend - appending the content to the list
        documents.append((wordList, intent['tag'])) # append - appending the list to the list
        if intent['tag'] not in classes:            # add to our classes list
            classes.append(intent['tag'])

# lemmatize and lower each word and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words))) # sort words
classes = sorted(list(set(classes))) # sort classes

# documents = combination between patterns and intents
print(len(documents), "documents")
# classes = intents, tags
print(len(classes), "classes", classes)
# words = all words, vocabulary
print(len(words), "unique lemmatized words", words)

pickle.dump(words, open('texts.pkl', 'wb'))
pickle.dump(classes, open('labels.pkl', 'wb'))


#Machine Learning


training = [] # create the training data
empty_output = [0] * len(classes) # create an empty array for the output

# training set, bag of words for each sentence
for doc in documents:
    bag = []                 # initialize the bag of words
    pattern_words = doc[0]   # list of tokenized words for the pattern
    pattern_words = [lemmatizer.lemmatize(w.lower()) for w in pattern_words] # lemmatize each word - create base word, in attempt to represent related words

    # create the bag of words array with 1, if word match found in current pattern
    for wordList in words:
        bag.append(1) if wordList in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag (for each pattern)
    row_output = list(empty_output)
    row_output[classes.index(doc[1])] = 1
    training.append([bag, row_output])

# shuffle our features and turn into np.array
random.shuffle(training)
Data_type = object
training = np.array(training, dtype=Data_type)


# Neural Network Model


# create train and test lists. X - patterns, Y - intents
train_x = list(training[:, 0])
train_y = list(training[:, 1])
print("Training data created")

test_x = train_x[150:]
test_y = train_y[150:]

# Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of
# neurons equal to number of intents to predict output intent with softmax
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5)) #prevent overfitting
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5)) #prevent overfitting
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
SGD = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=SGD, metrics=['accuracy'])

# fitting and saving the model
HIST = model.fit(np.array(train_x), np.array(train_y), epochs=50, batch_size=5, verbose=1)
model.save('model.h5', HIST)

print("model created")

# #Plot Graphs
# import matplotlib.pyplot as plt
# from sklearn.metrics import confusion_matrix
# import seaborn as sns
# import itertools


# # Predict the test data
# predictions = model.predict(test_x)
# predicted_labels = np.argmax(predictions, axis=1)

# # Generate the confusion matrix
# cm = confusion_matrix(np.argmax(test_y, axis=1), predicted_labels)

# # Plot the confusion matrix as an image
# class_names = ['Greeting', 'Follow up Questions', 'Goodbye', 'Thank You', 'No Answer', 'Options', 'Symptom Additional Detail', 'Treatment', 'Pharmacy', 'Pharmacy Question', 'Medicine Additional Detail', 'Symptoms', 'Medicine']
# plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Greens)
# plt.title("Confusion Matrix")
# plt.colorbar()
# tick_marks = np.arange(len(class_names))
# plt.xticks(tick_marks, class_names, rotation=90, fontsize=10)
# plt.yticks(tick_marks, class_names, fontsize=10)

# # Add text annotations to the plot
# thresh = cm.max() / 2.
# for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
#     plt.text(j, i, cm[i, j],
#              horizontalalignment="center",
#              color="white" if cm[i, j] > thresh else "black")

# plt.tight_layout()
# plt.ylabel('True label', fontsize=14, color='Green', labelpad=20)
# plt.xlabel('Predicted label', fontsize=14, color='Green', labelpad=20) 
# plt.show()



# # Plot the training loss and accuracy
# plt.plot(HIST.history['loss'])
# plt.plot(HIST.history['accuracy'])
# plt.title('Model Training')
# plt.ylabel('Value')
# plt.xlabel('Epoch')
# plt.legend(['loss', 'accuracy'], loc='upper right')
# plt.show()
