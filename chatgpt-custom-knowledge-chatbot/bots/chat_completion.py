import openai
import gradio as gr
import os

os.environ['OPENAI_API_KEY'] = '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'

def initialize_messages() -> list:
    """Initialize the chat messages with system and user messages."""
    # TODO; since this prompt is not sufficient in steering the bot to use only the custom knowledge, experiment with it.
    return [
        {"role": "system", "content": "You are a multilingual digital analyst specializing in extracting insights from social media data across multiple languages, only respond with knowledge knowledge you know for sure, dont hallucinate information."},
        {"role": "user", "content": "Hello Assistant, I have a list of tweets, some of which may appear similar or repeated. I want you to analyze these tweets and identify patterns and trends even if they are not in English."}  # Replace with custom knowledge base.
    ]


def get_user_input() -> str:
    """Get user input from the command line."""
    return input("User: ")


def add_message(messages: list, role: str, content: str):
    """Add a message to the list of chat messages."""
    messages.append({"role": role, "content": content})


def generate_chat_response(messages: list) -> str:
    """Generate a chat response using the OpenAI API."""
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return completion.choices[0].message.content


def main():
    messages = initialize_messages()

    while True:
        user_message = get_user_input()
        add_message(messages, "user", user_message)

        chat_response = generate_chat_response(messages)
        print(f'ChatGPT: {chat_response}')
        add_message(messages, "assistant", chat_response)


if __name__ == '__main__':
    main()


