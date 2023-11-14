from llama_index import SimpleDirectoryReader, GPTListIndex, GPTVectorStoreIndex, LLMPredictor, PromptHelper, StorageContext, load_index_from_storage
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
import backoff
import gradio as gr
import sys
import os

#https://cookbook.openai.com/examples/how_to_handle_rate_limits
os.environ["OPENAI_API_KEY"] = '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'

openai = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key='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')


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
#@backoff.on_exception(backoff.expo, openai.error.RateLimitError)

def construct_index(directory_path):
    max_input_size = 2048
    num_outputs = 512
    max_chunk_overlap = 0.5
    chunk_size_limit = 300
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs))
    documents = SimpleDirectoryReader(directory_path).load_data()
    index = GPTVectorStoreIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index.storage_context.persist('index.json')
    return index

def chatbot(input_text):
    storage_context = StorageContext.from_defaults(persist_dir='index.json')
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(input_text)
    return response.response

iface = gr.Interface(fn=chatbot,
inputs=gr.components.Textbox(lines=7, label="Enter your text"),
outputs="text",
title="My AI Chatbot")
index = construct_index("data")
iface.launch(share=True)