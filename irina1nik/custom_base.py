from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTVectorStoreIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
import sys
import os
import gradio as gr
import openai


#from clean_csv import clean
# from IPython.display import Markdown, display

os.environ['OPENAI_API_KEY'] = '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'
openai.api_key = os.environ["OPENAI_API_KEY"]
def construct_index(directory_path):
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 2000
    # set maximum chunk overlap
    max_chunk_overlap = 20
    # set chunk size limit
    chunk_size_limit = 600 

    # define prompt helper
    prompt_helper = PromptHelper(max_input_size, num_outputs, chunk_size_limit=chunk_size_limit)
#PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="text-davinci-003", max_tokens=num_outputs))
 
    documents = SimpleDirectoryReader(directory_path).load_data()
    
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)

    #index.save_to_disk('index.json')
    index.storage_context.persist(persist_dir=r'C:/Users/Iris Nguyen/Documents/ChatGPT/irina1nik/')

    return index

def ask_ai(query):
    index = GPTVectorStoreIndex.load_from_disk('index.json')
    while True: 
        # query = input("What do you want to ask? ")
        response = index.query(query)
        print(f"Response: {response.response}")
        return response.response

def upload_file(files):
    paths = []

def main():
    construct_index("context_data/data")
    
    with gr.Blocks() as demo:
        question = gr.Textbox(label="Question")
        #upload_btn = gr.UploadButton(label="Upload CSV", file_types = ['.csv', '.xlsx'], live=True)     #, file_count = "single"
        answer = gr.Textbox(label="GPT says")
        submit_btn = gr.Button("Submit")
        submit_btn.click(fn=ask_ai, inputs=question, outputs=answer, api_name="ask_ai")
        #output_csv = gr.DataFrame(clean())
       # table = gr.Dataframe(headers=["publish", "content", "link"], type="pandas", col_count=3) #, value=clean()
        #image = gr.Plot()
        #upload_btn.upload(fn=clean, inputs=upload_btn, outputs=table, api_name="upload_csv")
    demo.launch(share=True)

if __name__ == '__main__':
    main()
