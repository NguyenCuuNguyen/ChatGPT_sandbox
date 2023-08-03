import os
import sys
import constants
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.indexes import VectorstoreIndexCreator

os.environ["OPENAI_API_KEY"] = constants.APIKEY

query = sys.argv[1]
print("query is {query}")

loader = CSVLoader(file_path=r"C:\Users\Iris Nguyen\Documents\ChatGPT\Data\ML_output_scrambled.csv", encoding="utf8")
data = loader.load()
print(f"data is {data}")

index = VectorstoreIndexCreator().from_loaders([loader])
print(index.query(query))