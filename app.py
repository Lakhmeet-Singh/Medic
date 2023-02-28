import json
import random
import nltk
import pickle
import requests
import json
import markdown
import numpy as np

from nltk.stem import WordNetLemmatizer
from keras.models import load_model

from health import get_symptoms_info, name_description, hasPart, mainEntityOfPage, get_treatment_info, treatment_info
from standard import get_standard_response
from terms import medical_terms, medicines_terms
from pharmacy import get_pharmacy_response
from medicines import get_medicine_info, medicine_name_description, medicine_hasPart

data_file = open('data.json').read()
intents = json.loads(data_file)

pharmacy_data = open('pharmacy data.json').read()
pharmacy_intent = json.loads(pharmacy_data)

model = load_model('model.h5')
lemmatizer = WordNetLemmatizer()

words = pickle.load(open('texts.pkl', 'rb'))
classes = pickle.load(open('labels.pkl', 'rb'))

def preprocess_text(text):
    # Tokenize the input text and lemmatize each token
    tokens = nltk.word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens] # stem each word - create short form for word
    return lemmatized_tokens

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def create_bag_of_words(text, words, show_details=True):
    # Create a bag of words representation of the input text
    lemmatized_tokens = preprocess_text(text)  # tokenize the pattern
    bag_of_words = [0] * len(words) # bag of words - matrix of N words, vocabulary matrix
    for token in lemmatized_tokens:
        for i, word in enumerate(words):
            if word == token:
                bag_of_words[i] = 1    # assign 1 if current word is in the vocabulary position
                if show_details:
                    print("Found word in bag: %s" % word)
    return np.array(bag_of_words)


def predict_intent(text, model):
    # Predict the intent of the input text using the trained model
    bag_of_words = create_bag_of_words(text, words, show_details=False)
    predictions = model.predict(np.array([bag_of_words]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, p] for i, p in enumerate(predictions) if p > ERROR_THRESHOLD]

    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    intent_list = [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]
    return intent_list

#tokensizing the sentence to find the medical term
def tokenize_health_question(question):
    words = nltk.word_tokenize(question)
    medical_words = []
    for word in words:
        if word in medical_terms:
            medical_words.append(word)
    return medical_words

def tokenize_medicines_question(question):
    words = nltk.word_tokenize(question)
    medicines_words = []
    for word in words:
        if word in medicines_terms:
            medicines_words.append(word)
    return medicines_words


#Chatbot response to user querys
def chatbot_response(msg):
    ints = predict_intent(msg, model)
    if ints[0]['intent'] == 'symptoms':
        medical_terms = tokenize_health_question(msg) # pass only the medical terms to the api
        if medical_terms:
            symptoms_info = get_symptoms_info(medical_terms)
            nameDescription = name_description(symptoms_info)
            return 'Symptoms name and description: <br><br> {}'.format(nameDescription)
        else:
            return "Sorry! I couldn't understand you. Could you please rephrase your question?"

    elif ints[0]['intent'] == 'additional_detail':
        medical_terms = tokenize_health_question(msg)
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
                info = 'Additional Information: <br> {}'.format(hasPart_Data)
                note_info = bold_title + note
                return info + '<br><br>' + note_info
            else:
                title = "Note: "
                bold_title = markdown.markdown(f'**{title}**')
                info = 'Additional Information: <br> {}'.format(mainEntityOfPage_Data)
                note_info = bold_title + note
                return info + '<br><br>' + note_info
        else:
            return "Sorry! I couldn't understand you. Could you please rephrase your question?"

    elif ints[0]['intent'] == 'treatment':
        medical_terms = tokenize_health_question(msg)
        if medical_terms:
            symptoms_info = get_treatment_info(medical_terms)
            treatment = treatment_info(symptoms_info)
            return 'Treatment: <br> {}'.format(treatment)
        else:
            return "Sorry! I couldn't understand you. Could you please rephrase your question?"
        
    elif ints[0]['intent'] == 'medicine':
        medicines_terms = tokenize_medicines_question(msg)
        if medicines_terms:
            medicine_info = get_medicine_info(medicines_terms)
            nameDescription_medicine = medicine_name_description(medicine_info)
            return 'Medicine name and description: <br><br> {}'.format(nameDescription_medicine)
        else:
            return "Sorry! I couldn't understand you. Could you please rephrase your question?"

    elif ints[0]['intent'] == 'medicine_additional_detail':
        medicines_terms = tokenize_medicines_question(msg)
        if medicines_terms:
            medicine_info = get_medicine_info(medicines_terms)
            additional_detail_medicine = medicine_hasPart(medicine_info)
            return 'Additional Information: <br><br> {}'.format(additional_detail_medicine)
        else:
            return "Sorry! I couldn't understand you. Could you please rephrase your question?"
          
    elif ints[0]['intent'] == 'pharmacy':
        pharmacy_info = "The pharmacy is in: AREA or POSTCODE"
        italic_note = markdown.markdown(f'*{pharmacy_info}*')
        note = "Please type your query in the following format and area/postcode in capital letters: " + italic_note
        return "Which area are you looking the pharmacy in?" + '<br><br>' + note
    
    elif ints[0]['intent'] == 'pharmacy_follow_up_question':
        return get_pharmacy_response(msg, pharmacy_intent )
        
    else:
        res = get_standard_response(ints, intents)
        return res

print('DOCTORBOT is Ready')




