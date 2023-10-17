import sys
import requests
import json

# Read the command-line argument
EscapedJoinedText = "This is, of course, absurd.The idea the state should coerce parents to vaccinate kids who have _already had_ an infection w a recent strain of COVID using a version that  _no longer circulates_ based on nothing more than titers of antibody in an underpowered trial is laughable. Australia needs to urgently improve #COVID19Aus vaccination rates in 5-11 year olds. Only 40% of kids in this age have received 2 doses. Critical for the current pandemic wave that kids are protected. Now that cardiac arrests IN CHILDREN are the new normal thanks to the vaccines, we need defibtillatos in every school! "

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
with open(r"C:\Users\Iris Nguyen\Documents\ChatGPT\chatGPT_API\output.txt", 'w', encoding='utf-8') as f:
    f.write(str(response.json()))

