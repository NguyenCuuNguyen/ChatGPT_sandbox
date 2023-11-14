from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, LLMPredictor, ServiceContext, PromptHelper
from langchain import OpenAI
import gradio as gr
import gradio.components
import os
import openai

os.environ["OPENAI_API_KEY"] = ''

def construct_index(directory_path):
    openai.api_key = ''
    max_input_size = 4096
    num_outputs = 512
    chunk_size_limit = 600
    max_chunk_overlap = 0.5
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    docs = SimpleDirectoryReader(directory_path).load_data()
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    index = GPTVectorStoreIndex(docs, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.storage_context.persist('index.json')

    return index

def chatbot(input_text):
    index = GPTVectorStoreIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response

iface = gr.Interface(fn=chatbot,
                     inputs=gr.inputs.Textbox(lines=7, label="Enter your text"),
                     outputs="text",
                     title="Custom-trained AI Chatbot")

index = construct_index("data")
iface.launch(share=True)