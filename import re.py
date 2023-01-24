import re
import json

with open('Pharmacy test.json') as json_file:
    dict = json.load(json_file)

for intent in dict['intents']:
    address = intent['Address']
    if address:
        x = re.search(".{8}$", address)
        if x:
            match = re.search("{3}", x.group())
        if match:
            print(match.group())