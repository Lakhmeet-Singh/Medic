import requests
import pprint
import json

value = input("Enter a search query: ")
user_input = value.split(" ")
response =requests.get('https://api.nhs.uk/conditions/'+'-'.join(user_input)+'?subscription-key=63ed187fd4db46b0898e29baea194d5f').json()
# print (response)
str = json.dumps(response) #dict to str
data = json.loads(str) #str to dict

def name_description(data):
    name = data['name']
    description = data['description']
    url = data['url']
    print(name + ' - ' + description)
    print (url)
    # print('>>')

def parts_of_data(data):
    newdata = data['hasPart']
    for data in newdata:
        heading = data['headline'] 
        nested_description = data['description']
        print(heading)
        # print('-')
        print(nested_description)
        # print('>>>>>>')

        hasPart = data['hasPart']
        for nested_data in hasPart:
            # print(nested_data)
            try: 
                headline = nested_data['headline']
                text = nested_data['text']
                print(headline)
                print(text)
                # print('||')
            except KeyError:
                print('')

def parts(data):
    newdata = data['mainEntityOfPage']
    for data in newdata:
        hasPart = data['hasPart']
        for nested_data in hasPart:
            try: 
                heading = nested_data['headline'] 
                text = nested_data['text']
                print(heading)
                # print('-')
                print(text)
                # print('>>>>>>')
            except KeyError:
                 print('erorr')  

        # hasPart = data['hasPart']
        # for nested_data in hasPart:
        #     # print(nested_data)
        #     try: 
        #         headline = nested_data['headline']
        #         text = nested_data['text']
        #         print(headline)
        #         print(text)
        #         # print('||')
        #     except KeyError:
        #         print('')          
name_description(data)
# parts_of_data(data)
parts(data)