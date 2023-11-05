import chromadb
import openai
import os
import pandas as pd
from chromadb.utils import embedding_functions



# Setup 
openai.api_key = os.environ.get('OPENAI_API_KEY')
openai_ef = embedding_functions.OpenAIEmbeddingFunction(model_name="text-embedding-ada-002")
client = chromadb.PersistentClient(path="/Users/levin/Documents/Uni/6. Semester/Bachelorarbeit/Prototyping/prototype 2.0")
#client.delete_collection("test_collection")
test_collection = client.get_or_create_collection(name="test_collection", embedding_function=openai_ef, metadata={"hnsw:space": "cosine"})

"""
pattern = r'^[^_]*_[^_]*_[A-Za-z0-9]{2}$'
# Get relevant data from csv
df = pd.read_csv('View_Data_Information.csv', sep=';')
df = df[['SchemaID', 'ObjectName', 'ObjectSQLCode_First_32767_Characters']]
df = df.rename(columns={'ObjectSQLCode_First_32767_Characters': 'ViewDescription'})
df = df[df['ObjectName'].str.contains(r".*_[A-Za-z0-9]{2}$", regex=True)]
df_d4 = df[df['ObjectName'].str.contains(r".*_D4$", regex=True)]
df_g0 = df[df['ObjectName'].str.contains(r".*_G0$", regex=True)]
df_m2 = df[df['ObjectName'].str.contains(r".*_M2$", regex=True)]

test_df = pd.concat([df_d4.iloc[0:2], df_g0.iloc[0:2], df_m2.iloc[0:2]], ignore_index=True)
"""
init_template = "Du bist ein Datenbankexperte, der die wichtigsten Informationen aus einer Beschreibung zu einer View extrahieren und sinnvoll darstellen kann"
chat_template_1 = "Bitte extrahiere den Namen der View, die Beschreibung, Links zur internen Dokumentation, das Outgoing Interface und Restrictions aus dem folgenden Text falls vorhanden. Falls eine oder mehrere der gesuchten Informationen nicht explizit gegeben ist schreibe: 'Nicht angegeben', gebe bei den Links nur die Links ohne weitere Zusätze an. Stelle die Informationen Stichpunktartig dar, ohne Bullet Points oder ähnliches zu verwenden: /**/ /* View: V_INTF_PnL_G3 */ /**/ /* =*/ /* V01.09.00 2023-03-07 Hui Yang BD/XSP4 & Tatjana Derdus CI/DAV2.3 & Yannick Sigwalt GS/BDO12 */ /* Interface view for transfer of monthly sales transactions data to Optravis */ /* This view implements the following Soft Rules */ /* #FBI-SR-000000066 https://inside-docupedia.bosch.com/confluence/pages/viewpage.action?pageId=1767424464 */ /* Restrictions: */ /* - Restricted to certain company codes (legal entities in the scope of BBM) */ /* Changes: */ /* - V01.09.00 Corrected field Plant */ /* - V01.08.00 Performance Optimization Ilja Frolov GS/BDD1 2023-03-03 */ /* - V01.07.00 Added field Plant */ /* - V01.06.00 Softrule V_SR_CompanyCodeForOptravis_V1 included */ /* - V01.05.00 Reworked view to use new CO-PA RAWVault and added Field ProfitCenter */ /* - V01.04.00 Added column SourceSystem (2021-02-10) */ /* - V01.03.00 Rename MaterialOrig to Material; Add SalesDocumentType (2020-12-16) */ /* - V01.02.00 Adjust TotalNetSales calculation based on changed customer requirement */ /* Use new MDS-based tables for CompanyCodeScope definition (2020-11-11) */ /* - V01.01.00 Replace WWR04 by ARTNR as source for MaterialOrig (2020-10-19) */ /* - V01.00.01 Re-worked based on refined customer requirement (2020-09-30) */ /* - V01.00.00 Initial version (2020-09-03) */ /* =*/"
chat_template_2 = """Name der View: V_INTF_PnL_G3
Beschreibung: Interface view for transfer of monthly sales transactions data to Optravis
Links zur internen Dokumentation: https://inside-docupedia.bosch.com/confluence/pages/viewpage.action?pageId=1767424464
Outgoing Interface: Nicht angegeben
Restrictions: Restricted to certain company codes (legal entities in the scope of BBM)
"""
chat_template_3 = "Bitte extrahiere den Namen der View, die Beschreibung, Links zur internen Dokumentation, das Outgoing Interface und Restrictions aus dem folgenden Text falls vorhanden. Gebe bei den Links nur die Links ohne weitere Zusätze an. Stelle die Informationen Stichpunktartig dar, ohne Bullet Points oder ähnliches zu verwenden: {system}"

"""
for index, row in test_df.iterrows():
    print("ViewDescription: ", row["ViewDescription"])
    formated_chat_3 = chat_template_3.format(system=row['ViewDescription'])
    print(formated_chat_3)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature = 0,
        messages=[
            {"role": "system", "content": init_template},
            {"role": "user", "content": chat_template_1},
            {"role": "assistant", "content": chat_template_2},
            {"role": "user", "content": formated_chat_3}
        ]
    )
    print("response: ", response)
    test_collection.add(documents=response['choices'][0]['message']['content'],
                   metadatas=[{"ObjectName": row["ObjectName"], "SAP-System": row["ObjectName"][-2:]}],
                   ids=[str(row["SchemaID"])])
"""
print(test_collection.get(include=["metadatas", "documents"]))


result = test_collection.query(query_texts=['I want to get cost data for different sub companies'],
                               n_results=1)
print(result["documents"][0][0])
