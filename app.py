import json
import random
import nltk
import pickle
import numpy as np

nltk.download('popular')
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

lemmatizer = WordNetLemmatizer()

data_file = open('Pharmacy test.json').read()
intents = json.loads(data_file)

model = load_model('model.h5')


words = pickle.load(open('texts.pkl', 'rb'))
classes = pickle.load(open('labels.pkl', 'rb'))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)    # tokenize the pattern - split words into array
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words] # stem each word - create short form for word
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence) # tokenize the pattern
    bag = [0] * len(words) # bag of words - matrix of N words, vocabulary matrix
    for s in sentence_words:
        for i, wordList in enumerate(words):
            if wordList == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % wordList)
    return (np.array(bag))


def predict_class(sentence, model):
    BagOfWords = bow(sentence, words, show_details=False)
    res = model.predict(np.array([BagOfWords]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"question": sentence, "probability": str(r[1])})
        return return_list

def get_pharmacy_information(area):
    area = clean_up_sentence(area)
    list_of_intents = intents['intents']
    result = []
    for i in list_of_intents:
        if area in i["Area"]:
            result.append("OrganisationName: {}, Address: {}, Area: {}, Phone: {}, Email: {}, Website: {}".format(i['OrganisationName'],i['Address'],i['Area'],i['Phone'],i['Email'],i['Website']))
    if result:
        return result
    else:
        return "Sorry, I couldn't find a pharmacy in that area"


def getResponse(ints, intents_json):
    if ints:
        utterance = ints[0]['question']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if ('Questions' in i) and (utterance in i['Questions']):
                result = 'Which area are you looking the pharmacy in?'
                area = input(result)
                area = area.upper()
                result = []
                for i in list_of_intents:
                    if area in i["Address"]:
                        result.append("OrganisationName: {}, Address: {}, Area: {}, Phone: {}, Email: {}, Website: {}".format(i['OrganisationName'],i['Address'],i['Area'],i['Phone'],i['Email'],i['Website']))
                if result:
                    return result
                else:
                    return "Sorry, I couldn't find a pharmacy in that area"
            else:
                return "Sorry, i can't understand you"
    else:
        return "Sorry, I couldn't find a pharmacy in that area"


print('DOCTORBOT is Ready')

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res



from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)

if __name__ == "__main__":
    app.run()
