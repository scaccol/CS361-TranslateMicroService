# Author: Lauren Scacco
# Date: 05-07-2022
# Description: Python service to handle GET and POST requests in REST API. 
# Microservice designed to pass messages for a step-by-step recipe program.

# Set-up Instructions: Make sure to have pip installed on your machine. Then in a command 
# prompt in the folder you have this program stored in, run "pip install flask". 
# You might see an error saying 'Import "flask" could not be resloved', but you can ignore it.

# Run Instructions: To start the service, use command python -m flask run

import json
from flask import Flask, request
app = Flask(__name__)

def db_filter(id, lang):
    with open("database.json", "r") as infile:
        data = json.load(infile)
        for line in data["messages"]:    
            if line["id"] == id and line["language"] == lang:
                return line


@app.get('/translator') # $id=<id>$language=<lang>
def get_messages():
    id = request.args.get('id')
    lang = request.args.get('language')
    with open("database.json", "r") as infile:
        result = db_filter(id, lang)

    # Set posted json to message.json
    with open("message.json", 'w') as outfile:
        outfile.write(json.dumps(result))
    return result

@app.post('/translator')
def add_message():

    data = request.data.decode('UTF-8').replace("'",'"')        
    data = data.replace('\r', '')
    data = data.replace('\n', '')
    data = data.replace('    ', '')
    content = json.loads(data)

    # Set posted json to message.json
    with open("message.json", 'w') as outfile:
        outfile.write(json.dumps(content))
    
    # Determine if the json is already in the db. If not, add it.
    id = content['id']
    lang = content['language']
    print(id, lang)
    result = db_filter(id, lang)
    if result:
        return db_filter(id, lang)
    else:
        with open("database.json", "r") as infile:
            data = json.load(infile)            
            data["messages"].append(content)
        with open("database.json", "w") as outfile:
            outfile.write(json.dumps(data))
        
        return content
