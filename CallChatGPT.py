import sys
import requests
import json

# Read the command-line argument
EscapedJoinedText = sys.argv[1]

# Define the URL, headers, and data
url = 'https://api.openai.com/v1/chat/completions'
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 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'
}
data = {
    'model': 'gpt-3.5-turbo-16k',
    'messages': [
        {
            'role': 'system',
            'content': 'You are a multilingual digital analyst specializing in extracting insights from social media data across multiple languages.'
        },
        {
            'role': 'user',
            'content': 'Hello Assistant, I have a list of tweets, some of which may appear similar or repeated. I want you to analyze these tweets and identify three distinct topics of discussion from them. For each topic, please provide a brief description and the number of a representative tweet. Do your best to analyze the tweets even if they are not in English. The tweets are as follows:\n' + EscapedJoinedText

        }
    ]
}

# Convert the data to a JSON-formatted string
data_json = json.dumps(data)

# Send the POST request
response = requests.post(url, headers=headers, data=data_json)

# Print the response
with open('C:\\PowerAutomateLab\\Generation\\output.txt', 'w', encoding='utf-8') as f:
    f.write(str(response.json()))

