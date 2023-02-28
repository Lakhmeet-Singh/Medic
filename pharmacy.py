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
                    result.append(f"{name_title} {i['OrganisationName']}")
                    result.append(f"{address_title} {i['Address']}")
                    result.append(f"{area_title} {i['Area']}")
                    result.append(f"{phone_title} {i['Phone']}")
                    result.append(f"{email_title} {i['Email']}")
                    result.append(f"{website_title} {i['Website'].replace(',', '') if i['Website'] != 'Not Found' else 'Not Found'}")
                    result.append(f'<br><br>')
        if result:
            return " ".join(result)
        else:
            return "Sorry, I couldn't find a pharmacy in that area"
    else:
        return "Sorry, I can't understand you"
