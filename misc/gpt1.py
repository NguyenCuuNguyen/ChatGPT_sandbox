#https://api.python.langchain.com/en/latest/chat_models/langchain.chat_models.openai.ChatOpenAI.html

from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, ServiceContext, StorageContext, load_index_from_storage
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
import gradio as gr
import os
import shutil

os.environ["OPENAI_API_KEY"] = ''
ChatOpenAI.openai_api_key = ''


def construct_index(directory_path, custom_path=[]):
    # set number of output tokens
    num_outputs = 256
    # _llm_predictor = LLMPredictor(llm=ChatOpenAI(openai_api_key="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", temperature=0.5, model_name="gpt-3.5-turbo", max_tokens=num_outputs))
    _llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="gpt-3.5-turbo", max_tokens=num_outputs))
    service_context = ServiceContext.from_defaults(llm_predictor=_llm_predictor)
    docs = SimpleDirectoryReader(directory_path).load_data()
    # if custom_path:
        # docs = SimpleDirectoryReader(custom_path[0]).load_data()
    #docs = SimpleDirectoryReader("../../../../nguyencuu/AppData/Local/Temp/gradio/aca317d818f5d5a8e381adeff7d8df5abf24322e").load_data()
        
        # docs += custom_docs
    print(f"docs length {len(docs)}")
    index = GPTVectorStoreIndex.from_documents(docs, service_context=service_context)
    
    #Directory in which the indexes will be stored
    index.storage_context.persist(persist_dir="indexes")

    return index

def run_chatbot(input_text, context=[]):
    
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="indexes")
    
    #load indexes from directory using storage_context
    query_engne = load_index_from_storage(storage_context).as_query_engine()
    
    response = query_engne.query(input_text)
    context.append((input_text, response.response))
    return gr.update(value=""), context

def upload_file(files):
    file_paths = [file.name for file in files]
    print(f"file_paths {file_paths}")
     # index = construct_index("data", path)
    #for path in file_paths:
    directory, file = os.path.split(file_paths[0]) #TODO: do multi files have same directory?
    index = construct_index(directory)
    return file_paths


#Creating the web UIusing gradio
def create_gradio_interface():
    paths = ""
    with gr.Blocks() as demo:
        gr.Markdown("# ChatGPT Custom Data Bot")
        gr.Markdown("Switch tab to use chatGPT or upload custom data")
        with gr.Tab("Conversation"):
            chatbot = gr.Chatbot() #chatbot component
            # state = gr.State([]) #session state persisting across multiple submits
            with gr.Row():
                txt = gr.Textbox(
                    show_label=False,
                    placeholder="Enter your question and press enter"
                ).style(container=False)
                print(f"txt is {txt}")
                clear = gr.Button("Clear")
            txt.submit(run_chatbot, [txt, chatbot], [txt, chatbot])
            clear.click(lambda: None, None, chatbot, queue=False)

        with gr.Tab("Upload file"):
            #gr.Row == horizontally:
            #with gr.Row(): #uncomment to show file preview
            #file_input = gr.File()
            file_output = gr.File()
            upload_button = gr.UploadButton("Upload a File", file_types=[".pdf",".csv",".docx", ".xlsx"], file_count="multiple")
            paths = upload_button.upload(upload_file, upload_button, file_output)
            print(f"upload_button")
    return demo, paths


def main():
    blocks, files = create_gradio_interface()
    #TODO: how to separate newly added file's processing with existing file's processing
    blocks.launch(share=True)

if __name__ == "__main__":
    main()