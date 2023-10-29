import chromadb
import os
import pandas as pd
from chromadb.utils import embedding_functions
import openai

# Setup of OpenAI and chromadb
openai.api_key = os.environ.get('OPENAI_API_KEY')
key = os.environ.get('OPENAI_API_KEY')
openai_ef = embedding_functions.OpenAIEmbeddingFunction(api_key=key, model_name="text-embedding-ada-002")
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="view-information")
sap_system = "D4"

# Read csv file 
df = pd.read_csv('View_Data_Information.csv', sep=';')
df = df[['SchemaID', 'ObjectName', 'ObjectSQLCode_First_32767_Characters']]
df = df.rename(columns={'ObjectSQLCode_First_32767_Characters': 'ViewDescription'})
df = df.iloc[0:2]

# Embedding function (from OpenAI Docs)
def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

# Embedd the information
df['embedding'] = df.ViewDescription.apply(lambda x: get_embedding(x))

for index, row in df.iterrows():
    collection.add(documents=[row["ViewDescription"]],
                   embeddings=[row["embedding"]],
                   metadatas=[{"ObjectName": row["ObjectName"]}],
                   ids=[str(row["SchemaID"])])

# Example request 
example_request = "I want to use the view to get the maintenance costs of the last 5 years"
request_embedding = get_embedding(example_request)

# Query chromadb for matches
result = collection.query(query_embeddings=[request_embedding],
                 n_results=2)
print(result)

# Query filter for sap-system D4 ,where={"ObjectName": "%_{}".format(sap_system)}