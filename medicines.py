import json
import requests
import json
import markdown

from nltk.stem import WordNetLemmatizer
from keras.models import load_model


ignore_words = ['[', ']', '\xa0', '/n', '[":']

#Medicines API Call
def get_medicine_info(symptoms):
    user_input = '-'.join(symptoms)
    response = requests.get('https://api.nhs.uk/medicines/'+user_input+'?subscription-key=28b51bbacf624c068a66bb5f46b14013').json()
    str = json.dumps(response) #dict to str
    data = json.loads(str) #str to dict
    return data


#Extracting name and description from Medicines API 
def medicine_name_description(med):
    data = med
    name = data['name']
    url = data['url']
    first_description = data['description']
    text = "Usefull Links: "
    add_info_title = "Note: "
    more_info = "Can you provide more information about medicine: Medicine Name"
    italic_note_info = markdown.markdown(f'*{more_info}*')
    add_info = "If you require additional information, please type your query in the following format: " + italic_note_info
    bold_note_title = markdown.markdown(f'**{add_info_title}**')
    bold_text = markdown.markdown(f'**{text}**')
    bold_name = markdown.markdown(f'**{name + ": "}**')

    newdata = data['hasPart']
    for des in newdata:
        description = des['description']
        sentences = description.split('"')
        first_sentence = sentences[0]
        break

    for word in ignore_words:
        if word in description:
            description = description.replace(word, " ")
        if word in first_description:
            first_description = first_description.replace(word, " ")
    return bold_name +  description + '\n' + first_description + '\n' + bold_text + url + '\n' +  bold_note_title + add_info


def medicine_hasPart(med):
    data = med
    medicine_part1 = []
    medicine_part2 = []
    newdata = data['hasPart']
    for data in newdata:
        description = data['description']
        medicine_part1.append(description)
    
        hasPart = data['hasPart']
        for nested_data in hasPart:
            try: 
                headline = nested_data['headline']
                text = nested_data['text']
                bold_headline = f'<br> <strong style="padding-bottom: 10px;">{headline}</strong> <br>'
                for word in ignore_words:
                    if word in text:
                        text = text.replace(word , " ")
                medicine_part2.append(bold_headline + '<p style="padding-bottom: 10px;">' + '<ul style="padding-left: 10px;">' + text + '</ul> </p>')
            except KeyError:
                pass
    # print (medicine_part1 + medicine_part2)
    output = ' '.join(medicine_part1 + medicine_part2)
    output = output.replace('<h2', '<h4 style="padding-top: 10px; font-weight: bold;"')
    output = output.replace('</h2>', '</h4>')
    output = output.replace('<a ', '<a style="text-decoration: underline; color: white;" ')
    return output