import json
import nltk
import markdown

nltk.download('popular')
nltk.download('punkt')
from nltk.tokenize import word_tokenize


pharmacy_data = open('pharmacy data.json').read()
pharmacy_intent = json.loads(pharmacy_data)


def get_pharmacy_response(query, pharmacy_intent_json):
    result = []
    name = "Name:"
    name_title = markdown.markdown(f'**{name}**')
    address = "Address:"
    address_title = markdown.markdown(f'**{address}**')
    area = "Area:"
    area_title = markdown.markdown(f'**{area}**')
    phone = "Phone:"
    phone_title = markdown.markdown(f'**{phone}**')
    email = "Email:"
    email_title = markdown.markdown(f'**{email}**')
    website = "Website:"
    website_title = markdown.markdown(f'**{website}**')
    if query:
        list_of_pharmacy_intent = pharmacy_intent_json['intents']
        tokens = nltk.word_tokenize(query)
        for i in list_of_pharmacy_intent:
            for token in tokens:
                if (token in i['Address'].upper()):
                    name_result = f"{name_title}{i['OrganisationName']}"
                    address_result = f"{address_title}{i['Address']}"
                    area_result = f"{area_title}{i['Area']}"
                    phone_result = f"{phone_title}{i['Phone']}"
                    email_result = f"{email_title}{i['Email']}"
                    website_result = f"{website_title}{i['Website']}"
                    result.append(f"{name_result} {address_result} {area_result} {phone_result} {email_result} {website_result}")
        if result:
            return result
        else:
            return "Sorry, I couldn't find a pharmacy in that area"
    else:
        return "Sorry, I can't understand you"