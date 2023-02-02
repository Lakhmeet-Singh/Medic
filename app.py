import json
import random
import nltk
import pickle
import requests
import json
import markdown
import numpy as np

nltk.download('popular')
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

from health import get_symptoms_info, name_description, hasPart, mainEntityOfPage, get_treatment_info, treatment_info
from standard import get_standard_response
from symptoms import medical_terms
from pharmacy import get_pharmacy_response

data_file = open('data.json').read()
intents = json.loads(data_file)

pharmacy_data = open('Pharmacy test.json').read()
pharmacy_intent = json.loads(pharmacy_data)


model = load_model('model.h5')
lemmatizer = WordNetLemmatizer()

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
    # filter out predictions below a threshold
    BagOfWords = bow(sentence, words, show_details=False)
    res = model.predict(np.array([BagOfWords]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


#tokensizing the sentence to find the medical term
def tokenize_question(question):
    words = nltk.word_tokenize(question)
    medical_words = []
    for word in words:
        if word in medical_terms:
            medical_words.append(word)
    return medical_words


#Chatbot response to user querys
def chatbot_response(msg):
    ints = predict_class(msg, model)
    if ints[0]['intent'] == 'symptoms':
        medical_terms = tokenize_question(msg) # pass only the medical terms to the api
        if medical_terms:
            symptoms_info = get_symptoms_info(medical_terms)
            nameDescription = name_description(symptoms_info)
            return 'Symptoms name and description: {}'.format(nameDescription)
        else:
            return "Sorry! I couldn't understand you. Could you please rephrase your question?"

    elif ints[0]['intent'] == 'additional_Detail':
        medical_terms = tokenize_question(msg)
        if medical_terms:
            symptoms_info = get_symptoms_info(medical_terms)
            hasPart_Data = hasPart(symptoms_info)
            mainEntityOfPage_Data = mainEntityOfPage(symptoms_info)
            more_info = "Can you provide me with the treatment for - Symptom name"
            italic_note_info = markdown.markdown(f'*{more_info}*')
            note = "If you require information about treatment, please type your query in the following format: " + italic_note_info
            if hasPart_Data:
                title = "Note: "
                bold_title = markdown.markdown(f'**{title}**')
                info = 'Additional Information: {}'.format(hasPart_Data)
                note_info = bold_title + note
                return info + note_info
            else:
                return 'Additional Information: {} Note: {}'.format(mainEntityOfPage_Data, note)
        else:
            return "Sorry! I couldn't understand you. Could you please rephrase your question?"

    elif ints[0]['intent'] == 'treatment':
        medical_terms = tokenize_question(msg)
        if medical_terms:
            symptoms_info = get_treatment_info(medical_terms)
            treatment = treatment_info(symptoms_info)
            return 'Treatment: {}'.format(treatment)
        else:
            return "Sorry! I couldn't understand you. Could you please rephrase your question?"
    
    elif ints[0]['intent'] == 'pharmacy':
        return "Which area are you looking the pharmacy in?"
    
    elif ints[0]['intent'] == 'pharmacy_follow_up_question':
        return get_pharmacy_response(msg, pharmacy_intent )

    else:
        res = get_standard_response(ints, intents)
        return res

print('DOCTORBOT is Ready')




# value = input("Enter a search query: ")
# # medical_terms = tokenize_question(value)
# # symptoms_info = get_treatment_info(medical_terms)
# # treatment = treatment_info(symptoms_info)
# # print (treatment)

# print (get_symptoms_info(value))
