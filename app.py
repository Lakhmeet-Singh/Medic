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

lemmatizer = WordNetLemmatizer()

data_file = open('data.json').read()
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


# Chatbot Conversation


#Standard Conversation
def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if (i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result

#Health API Call
ignore_words = ['[', ']', '\xa0', '/n', '[":']
def get_symptoms_info(symptoms):
    user_input = '-'.join(symptoms)
    response = requests.get('https://api.nhs.uk/conditions/'+user_input+'?subscription-key=63ed187fd4db46b0898e29baea194d5f').json()
    str = json.dumps(response) #dict to str
    data = json.loads(str) #str to dict
    return data

#Extracting name and description from Health API 
def name_description(data):
    name = data['name']
    description = data['description']
    url = data['url']
    text = "URL: "
    add_info_title = "Note: "
    more_info = "More information - Symptom name"
    bold_note_info = markdown.markdown(f'*{more_info}*')
    add_info = "If you require additional information, please type your query in the following format: " + bold_note_info
    bold_note_title = markdown.markdown(f'**{add_info_title}**')
    bold_text = markdown.markdown(f'**{text}**')
    bold_name = markdown.markdown(f'**{name + ": "}**')
    for word in ignore_words:
        if word in description:
            description = description.replace(word, " ")
    return bold_name + description + '\n' + bold_text + url + '\n' +  bold_note_title + add_info


#Extracting other information from Health API 
def hasPart(data):
    parts_data_1 = []
    parts_data_2 = []
    newdata = data['hasPart']
    for data in newdata:
        heading = data['headline'] 
        nested_description = data['description']
        bold_heading = markdown.markdown(f'**{heading}**')
        parts_data_1.append(bold_heading + nested_description)

        hasPart = data['hasPart']
        for nested_data in hasPart:
            try: 
                headline = nested_data['headline']
                text = nested_data['text']
                bold_headline = markdown.markdown(f'**{headline}**')
                for word in ignore_words:
                    if word in text:
                        text = text.replace(word , " ")
                parts_data_2.append(bold_headline + text)
            except KeyError:
                pass
    return parts_data_1 + parts_data_2

#Extracting other information from Health API where hasPart is not there.
def mainEntityOfPage(data):
    newdata = data['mainEntityOfPage']
    parts_data = []
    for data in newdata:
        hasPart = data['hasPart']
        for nested_data in hasPart:
            try: 
                headline = nested_data['headline'] 
                text = nested_data['text']
                bold_headline = markdown.markdown(f'**{headline}**')
                for word in ignore_words:
                    if word in text:
                        text = text.replace(word, " ")
                parts_data.append(bold_headline + text)
            except KeyError:
                 pass
    return parts_data

#treatment api call
def get_treatment_info(symptoms):
    user_input = '-'.join(symptoms)
    try:
        response = requests.get('https://api.nhs.uk/conditions/'+user_input+'/treatment?subscription-key=63ed187fd4db46b0898e29baea194d5f').json()
        str = json.dumps(response) #dict to str
        data = json.loads(str) #str to dict
        return data
    except:
        return "Sorry, no treatment information found for the given symptoms."


def treatment_info(data):
    text_array = []
    try:
        newdata = data['mainEntityOfPage']
        for data in newdata:
            if data['position']:
                for sub_data in data['mainEntityOfPage']:
                    text = sub_data['text']
                    text_array.append(text)
    except:
        return "Sorry, no treatment information found for the given symptoms."
    return text_array
    
# Load a medical terms lexicon or pre-trained model
medical_terms = set(["abdominal-aortic-aneurysm-screening", "abdominal-aortic-aneurysm", "abdominal-aortic-aneurysm-screening", "abortion", "abscess", 
          "acanthosis-nigricans", "achalasia", "acid-and-chemical-burns", "reflux-in-babies", "acne", "acoustic-neuroma", "acromegaly", "actinic-keratoses", 
          "actinomycosis", "acupuncture", "acute-cholecystitis", "acute-kidney-injury", "acute-lymphoblastic-leukaemia", "acute-myeloid-leukaemia", "acute-pancreatitis", 
          "acute-respiratory-distress-syndrome", "addison's-disease", "adenoidectomy", "age-related-cataracts", "age-related-macular-degeneration-amd", "agoraphobia", "air-embolism", 
          "albinism", "alcohol-misuse", "alcohol-poisoning", "alcohol-related-liver-disease", "alexander-technique", "alkaptonuria", "allergic-rhinitis", "allergies", "altitude-sickness",
          "alzheimer's-disease", "lazy-eye", "memory-loss-amnesia", "amniocentesis", "amputation", "amyloidosis", "anabolic-steroid-misuse", "iron-deficiency-anaemia", 
          "vitamin-B12-or-folate-deficiency-anaemia", "anaesthesia", "anal-cancer", "anal-fissure", "anal-fistula", "anal-pain", "anaphylaxis", "androgen-insensitivity-syndrome", 
          "abdominal-aortic-aneurysm", "brain-aneurysm", "angelman-syndrome", "angina", "angioedema", "angiography", "coronary-angioplasty-and-stent-insertion", "animal-and-human-bites", 
          "ankle-pain", "ankylosing-spondylitis", "anorexia-nervosa", "lost-or-changed-sense-of-smell", "antacids", "antibiotics", "anticoagulant-medicines", "antidepressants", "antifungal-medicines", 
          "antihistamines", "antiphospholipid-syndrome", "antisocial-personality-disorder", "itchy-anus", "anxiety-disorders-in-children", "aortic-valve-replacement", "aphasia", "appendicitis", "arrhythmia",
          "arterial-thrombosis", "arthritis", "arthroscopy", "asbestosis", "autism", "aspergillosis", "aspirin", "asthma", "astigmatism", "ataxia", "atherosclerosis", "athletes-foot", "atopic-eczema",
          "atrial-fibrillation", "attention-deficit-hyperactivity-disorder-adhd", "auditory-processing-disorder", "autism", "autosomal-dominant-polycystic-kidney-disease-adpkd",
          "autosomal-recessive-polycystic-kidney-disease-arpkd", "bird-flu"])

#tokensizing the sentence to find the medical term
def tokenize_question(question):
    words = nltk.word_tokenize(question)
    medical_words = []
    for word in words:
        if word in medical_terms:
            medical_words.append(word)
    return medical_words


#Medicine API Call


#Chatbot response to user querys
def chatbot_response(msg):
    ints = predict_class(msg, model)
    text = 'treatment'
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
            if hasPart_Data:
                return 'Additional Information: {}'.format(hasPart_Data)
            else:
                return 'Additional Information: {}'.format(mainEntityOfPage_Data)
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
    
    else:
        res = getResponse(ints, intents)
        return res

print('DOCTORBOT is Ready')




# value = input("Enter a search query: ")
# # medical_terms = tokenize_question(value)
# # symptoms_info = get_treatment_info(medical_terms)
# # treatment = treatment_info(symptoms_info)
# # print (treatment)

# print (get_symptoms_info(value))
