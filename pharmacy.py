import json
import nltk

nltk.download('popular')
nltk.download('punkt')
from nltk.tokenize import word_tokenize


pharmacy_data = open('pharmacy data.json').read()
pharmacy_intent = json.loads(pharmacy_data)


def get_pharmacy_response(query, pharmacy_intent_json):
    result = []
    if query:
        list_of_pharmacy_intent = pharmacy_intent_json['intents']
        tokens = nltk.word_tokenize(query)
        for i in list_of_pharmacy_intent:
            for token in tokens:
                if (token in i['Address'].upper()):
                    result.append("OrganisationName: {}, Address: {}, Area: {}, Phone: {}, Email: {}, Website: {}".format(i['OrganisationName'],i['Address'],i['Area'],i['Phone'],i['Email'],i['Website']))
        
        if result:
            return result
        else:
            return "Sorry, I couldn't find a pharmacy in that area"
    else:
        return "Sorry, I can't understand you"

# while True:
#     s = input('>>>>')
#     print(get_pharmacy_response(s, pharmacy_intent))