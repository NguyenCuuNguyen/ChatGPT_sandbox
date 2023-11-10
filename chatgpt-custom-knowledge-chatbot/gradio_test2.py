import os
import openai
import gradio as gr

#get user chat history & store it in a list and add it to previous state
openai.api_key = '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'
prompt = "what's America's HPV sentiment?"
def api_calling(prompt):
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completion.choices[0].text
    return message

def message_history(input, history):
    history = history or []
    print(f"history = {history}")
    s = list(sum(history, ()))
    s.append(input)
    # print('########################################')
    # print(s)
    inp = ' '.join(s)
    # print(f"Input: {inputt}")
    output = api_calling(inp)
    history.append((input,output))
    return history, history

block = gr.Blocks(theme=gr.themes.Monochrome())
with block:
    gr.Markdown("""<h1><center>ChatGPT  
    ChatBot with Gradio and OpenAI</center></h1> 
    """)
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder=prompt)
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(message_history,
                 inputs=[message, state],
                 outputs=[chatbot, state])
block.launch(debug=True, share=True)