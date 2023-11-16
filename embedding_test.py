import openai
import os
import chromadb
from vector_database_setup import get_collection
from chromadb.utils import embedding_functions


openai.api_key = os.environ.get('OPENAI_API_KEY')
openai_ef = embedding_functions.OpenAIEmbeddingFunction(model_name="text-embedding-ada-002")
client = chromadb.Client()
test_collection = client.create_collection("test_collection", embedding_function=openai_ef, metadata={"hnsw:space": "cosine"})
collection = get_collection()

def get_embedding(text):
    response = openai.Embedding.create(model='text-embedding-ada-002', input=text)
    return response['data'][0]['embedding']

#view = get_embedding("/**/ /* View: V_INTF_CDP_CostActual_V2_IFCT0_D4 */ /**/ /* = */ /* V01.00.00 2023-03-15 Ismail Okadia GS/TET3-NA */ /* This view is to provide CO-OM Cost Actuals data for Cost Driver Planning application (CDP) */ /* Data.CORE Outgoing Interface #0337 https://inside-docupedia.bosch.com/confluence/x/RBnSqQ */ /* Implemented Soft Rules */ /* Filter Cost Actual Fact Data by Company Code Positive List */ /* #FBI-SR-000000057 https://inside-docupedia.bosch.com/confluence/x/fFf1Yw */ /* Update: */ /* V01.00.00 Recreated view on top of persisted Fact [COCostActual_V2_MFCT0_D4] */ /* */")
#query = get_embedding("I want to buy tools for my garden to make it pretty and sit there and watch birds. I like sunny weather and blue skys. My favorite food is pizza and I love dogs.")

#print(view)
#print(query)

#result = collection.query(query_texts=["I want to buy tools for my garden to make it pretty and sit there and watch birds. I like sunny weather and blue skys. My favorite food is pizza and I love dogs."], where={"ObjectName": "V_INTF_CDP_CostActual_V2_IFCT0_D4"})
#print(result)

embedded_text = get_embedding("/**/ /* View: V_INTF_CDP_CostActual_V2_IFCT0_D4 */ /**/ /* = */ /* V01.00.00 2023-03-15 Ismail Okadia GS/TET3-NA */ /* This view is to provide CO-OM Cost Actuals data for Cost Driver Planning application (CDP) */ /* Data.CORE Outgoing Interface #0337 https://inside-docupedia.bosch.com/confluence/x/RBnSqQ */ /* Implemented Soft Rules */ /* Filter Cost Actual Fact Data by Company Code Positive List */ /* #FBI-SR-000000057 https://inside-docupedia.bosch.com/confluence/x/fFf1Yw */ /* Update: */ /* V01.00.00 Recreated view on top of persisted Fact [COCostActual_V2_MFCT0_D4] */ /* */")
embedded_text2 = get_embedding("Hot")
test_collection.add(ids=["3"], documents=["/**/ /* View: V_INTF_CDP_CostActual_V2_IFCT0_D4 */ /**/ /* = */ /* V01.00.00 2023-03-15 Ismail Okadia GS/TET3-NA */ /* This view is to provide CO-OM Cost Actuals data for Cost Driver Planning application (CDP) */ /* Data.CORE Outgoing Interface #0337 https://inside-docupedia.bosch.com/confluence/x/RBnSqQ */ /* Implemented Soft Rules */ /* Filter Cost Actual Fact Data by Company Code Positive List */ /* #FBI-SR-000000057 https://inside-docupedia.bosch.com/confluence/x/fFf1Yw */ /* Update: */ /* V01.00.00 Recreated view on top of persisted Fact [COCostActual_V2_MFCT0_D4] */ /* */"])
test_collection.add(ids=["4"], embeddings=[embedded_text])
embedded_query = get_embedding("I want to get an overview over all the costs of our subcompanies")
result_ne = test_collection.query(query_texts=["I want to get an overview over all the costs of our subcompanies"])
result_e = test_collection.query(query_embeddings=[embedded_query])
test_collection.add(ids=["5"], documents=["Once upon a time in a faraway land, there lived a brave knight who embarked on a quest to find a legendary dragon. He journeyed through enchanted forests, climbed towering mountains, and crossed vast deserts. Along the way, he encountered various magical creatures and faced numerous challenges. His courage and determination were unyielding as he pursued his noble mission."])
test_collection.add(ids=["6"], embeddings=[embedded_text2])
embedded_query2 = get_embedding("Cold")
print(test_collection.query(n_results=2, query_texts=["The latest advancements in quantum computing have revolutionized data processing capabilities. Quantum computers leverage the principles of quantum mechanics to perform operations on data at unprecedented speeds. This technological breakthrough holds immense potential for solving complex problems in fields like cryptography, materials science, and artificial intelligence. Researchers are continuously exploring the scalability and practical applications of these quantum systems."]))
#print(test_collection.query(query_embeddings=[embedded_query2]))
#print("NOT EMBEDDED",result_ne)
#print("EMBEDDED", result_e)