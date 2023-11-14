#https://api.python.langchain.com/en/latest/chat_models/langchain.chat_models.openai.ChatOpenAI.html

from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, ServiceContext, StorageContext, load_index_from_storage
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
import gradio as gr
import os

os.environ["OPENAI_API_KEY"] = ''
ChatOpenAI.openai_api_key = ''

def construct_index(directory_path, custom_path=""):
    # set number of output tokens
    num_outputs = 256
    # _llm_predictor = LLMPredictor(llm=ChatOpenAI(openai_api_key="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", temperature=0.5, model_name="gpt-3.5-turbo", max_tokens=num_outputs))
    _llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="gpt-3.5-turbo", max_tokens=num_outputs))
    service_context = ServiceContext.from_defaults(llm_predictor=_llm_predictor)
    docs = SimpleDirectoryReader(directory_path).load_data()
    if custom_path:
        custom_docs = SimpleDirectoryReader(directory_path).load_data()
        docs += custom_docs

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
    #returning the response
    return response.response, context


def upload_file(files):
    file_paths = [file.name for file in files]
    return file_paths


#Creating the web UIusing gradio
def create_gradio_interface():
    paths = ""
    with gr.Blocks() as demo:
        gr.Markdown("Switch tab to use chatGPT or upload custom data")
        with gr.Tab("Conversation"):
            chatbot = gr.Chatbot() #chatbot component
            # state = gr.State([]) #session state persisting across multiple submits
            with gr.Row():
                txt = gr.Textbox(
                    show_label=False,
                    placeholder="Enter your question and press enter"
                ).style(container=False)
            txt.submit(run_chatbot, [txt, chatbot], [txt, chatbot])

        with gr.Tab("Upload file"):
            #gr.Row == horizontally:
            #with gr.Row(): #uncomment to show file preview
            #file_input = gr.File()
            file_output = gr.File()
            upload_button = gr.UploadButton("Upload a File", file_types=[".pdf",".csv",".docx", ".xlsx"], file_count="multiple")
            paths = upload_button.upload(upload_file, upload_button, file_output)
    return demo, paths
    

# iface = gr.Interface(fn=run_chatbot,
#                      inputs=gr.inputs.Textbox(lines=10, label="Enter your question here"),
#                      outputs="text",
#                      title="Custom-trained AI Chatbot")


def main():
    blocks, files = create_gradio_interface()

    #Constructing indexes based on the documents in traininData folder
    #This can be skipped if you have already trained your app and need to re-run it
    index = construct_index("data", files)

    #launching the web UI using gradio
    blocks.launch(share=True)

if __name__ == "__main__":
    main()