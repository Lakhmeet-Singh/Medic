import requests
import json


value = input("Enter a search query: ")
response = requests.get('https://api.nhs.uk/conditions/'+value+'/treatment?subscription-key=63ed187fd4db46b0898e29baea194d5f').json()
str = json.dumps(response) #dict to str
data = json.loads(str) #str to dict

def treatmetn(data):
    text = ''
    newdata = data['mainEntityOfPage']
    for data in newdata:
        if data['position'] >= 2:
            if 'mainEntityOfPage' in data:
                for sub_data in data['mainEntityOfPage']:
                    text = sub_data['text']
                    print (text)

treatmetn(data)

