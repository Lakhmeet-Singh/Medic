import json
import requests
import json
import markdown

from nltk.stem import WordNetLemmatizer
from keras.models import load_model


ignore_words = ['[', ']', '\xa0', '/n', '[":']

#Health API Call
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

from bs4 import BeautifulSoup
#Extracting other information from Health API 
def hasPart(data):
    parts_data_1 = []
    parts_data_2 = []
    newdata = data['hasPart']
    for data in newdata:
        heading = data['headline'] 
        nested_description = data['description']
        bold_heading = f' <br> <strong style="padding-top: 10px; padding-bottom: 10px;">{heading}</strong>'
        parts_data_1.append(bold_heading + '<p style="padding-bottom: 10px;">' + '<ul style="padding-left: 10px;">' + nested_description + ' </ul> </p>')

        hasPart = data['hasPart']
        for nested_data in hasPart:
            try: 
                headline = nested_data['headline']
                text = nested_data['text']
                bold_headline = f' <br> <strong style="padding-top: 10px; padding-bottom: 10px;">{headline}</strong>'
                for word in ignore_words:
                    if word in text:
                        text = text.replace(word , " ")
                parts_data_2.append(bold_headline + '<p style="padding-bottom: 10px;">' + '<ul style="padding-left: 10px;">' + text + '</ul> </p>')
            except KeyError:
                pass
    output = ' '.join(parts_data_1 + parts_data_2)
    output = output.replace('<a ', '<a style="text-decoration: underline; color: white;')
    return output




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
                bold_headline = f'<br> <strong style="padding-top: 10px; padding-bottom: 10px;">{headline}</strong><br>'
                for word in ignore_words:
                    if word in text:
                        text = text.replace(word, " ")
                parts_data.append(bold_headline + '<p style="padding-bottom: 10px;">' + '<ul style="padding-left: 10px;">' + text + '</ul></p>')
            except KeyError:
                pass
    output = ' '.join(parts_data)
    output = output.replace('<a ', '<a style="text-decoration: underline; color: white;" ')
    return output


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
                    text_array.append('<p style="padding-bottom: 10px;">' + '<ul style="padding-left: 10px;">' + text + '</ul></p>')
    except:
        return "Sorry, no treatment information found for the given symptoms."
    output = ' '.join(text_array)
    output = output.replace('<h3', '<h4 style="padding-top: 10px; font-weight: bold; font-size: 18px"')
    output = output.replace('</h3>', '</h4>')
    output = output.replace('<a ', '<a style="text-decoration: underline; color: white;" ')
    return output