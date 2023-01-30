import json
import requests
import json
import markdown

from nltk.stem import WordNetLemmatizer
from keras.models import load_model


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
    text = "Usefull Links: "
    add_info_title = "Note: "
    more_info = "More information - Symptom name"
    italic_note_info = markdown.markdown(f'*{more_info}*')
    add_info = "If you require additional information, please type your query in the following format: " + italic_note_info
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