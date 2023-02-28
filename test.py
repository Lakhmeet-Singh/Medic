import requests
import json
import nltk
import terms

nltk.download('popular')
nltk.download('punkt')
from nltk.tokenize import word_tokenize

value = input("Enter a search query: ")

def api(symptom):
    response = requests.get('https://api.nhs.uk/medicines/?subscription-key=28b51bbacf624c068a66bb5f46b14013').json()
    str = json.dumps(response) #dict to str
    data = json.loads(str) #str to dict
    return data

def api_medicine(symptom):
    data = medicine(symptom)
    print(data)
    result = []
    for medicine_name in data:
        medicine_name = medicine_name.lower().split(" (")[0].replace(" ", "-")
        response = requests.get(f'https://api.nhs.uk/medicines/{medicine_name}?subscription-key=28b51bbacf624c068a66bb5f46b14013').json()
        result.append(response)
    return result



def api_data(data):
    text = api_medicine(data)
    results = []
    for t in text:
        name = t['name']
        description = t['description']
        results.append(name + ": " + description)
    print(results)


#high blood pressure
medical_terms = terms.medical_terms_list
medical_terms_tokens = [term.split("-") for term in medical_terms]
# print(medical_terms_tokens)


def medicine(value):
    data = api(value)
    medicine_name = []
    for des in data['significantLink']:
        description = des['description']
        name = des['name']
        if value in description:
            medicine_name.append(name)
    return medicine_name

# medicine(value)
api_data(value)
