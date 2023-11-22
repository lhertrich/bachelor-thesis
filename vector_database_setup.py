import chromadb
import openai
import os
import pandas as pd
from chromadb.utils import embedding_functions

client = None

def get_collection():
    global client
    # Setup
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(model_name="text-embedding-ada-002")
    if client is None:
        # Get client     
        client = chromadb.PersistentClient(path="/Users/levin/Documents/Uni/6. Semester/Bachelorarbeit/Prototyping/prototype 2.0/chromadb")
    collection = client.get_or_create_collection(name='bosch_data_v2', embedding_function=openai_ef, metadata={"hnsw:space": "cosine"})
    return collection

if __name__ == '__main__':
    # Delete collection and create it new
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(model_name="text-embedding-ada-002")
    client = chromadb.PersistentClient(path="/Users/levin/Documents/Uni/6. Semester/Bachelorarbeit/Prototyping/prototype 2.0/chromadb")
    client.delete_collection('bosch_data')
    collection = client.get_or_create_collection(name='bosch_data', embedding_function=openai_ef, metadata={"hnsw:space": "cosine"})

    # Get relevant data from csv
    df = pd.read_csv('data/View_Data_Information.csv', sep=';')
    df = df[['ObjectID', 'ObjectName', 'ObjectSQLCode_First_32767_Characters']]
    df = df.rename(columns={'ObjectSQLCode_First_32767_Characters': 'ViewDescription'})
    df = df[df['ObjectName'].str.contains(r".*_[A-Za-z0-9]{2}$", regex=True)]
    #df_d4 = df[df['ObjectName'].str.contains(r".*_D4$", regex=True)]
    #df_d3 = df[df['ObjectName'].str.contains(r".*_D3$", regex=True)]
    #df_g0 = df[df['ObjectName'].str.contains(r".*_G0$", regex=True)]
    #df_g6 = df[df['ObjectName'].str.contains(r".*_G6$", regex=True)]
    #df_m2 = df[df['ObjectName'].str.contains(r".*_M2$", regex=True)]
    #complete_df = pd.concat([df_d4.iloc[0:5], df_d3.iloc[0:5], df_g0.iloc[0:5], df_g6.iloc[0:5], df_m2.iloc[0:5]], ignore_index=True)
    complete_df = df
    complete_df.to_csv('data/protoype_view_data.csv', sep=';', index=False)

    init_template = "Du bist ein Datenbankexperte, der die wichtigsten Informationen aus einer Beschreibung zu einer View extrahieren und sinnvoll darstellen kann"
    chat_template_1 = "Bitte extrahiere den Namen der View, die Beschreibung, Links zur internen Dokumentation, das Outgoing Interface und Restrictions aus dem folgenden Text falls vorhanden. Falls eine oder mehrere der gesuchten Informationen nicht explizit gegeben ist schreibe: 'Nicht angegeben', gebe bei den Links nur die Links ohne weitere Zusätze an. Stelle die Informationen Stichpunktartig dar, ohne Bullet Points oder ähnliches zu verwenden: /**/ /* View: V_INTF_PnL_G3 */ /**/ /* =*/ /* V01.09.00 2023-03-07 Hui Yang BD/XSP4 & Tatjana Derdus CI/DAV2.3 & Yannick Sigwalt GS/BDO12 */ /* Interface view for transfer of monthly sales transactions data to Optravis */ /* This view implements the following Soft Rules */ /* #FBI-SR-000000066 https://inside-docupedia.bosch.com/confluence/pages/viewpage.action?pageId=1767424464 */ /* Restrictions: */ /* - Restricted to certain company codes (legal entities in the scope of BBM) */ /* Changes: */ /* - V01.09.00 Corrected field Plant */ /* - V01.08.00 Performance Optimization Ilja Frolov GS/BDD1 2023-03-03 */ /* - V01.07.00 Added field Plant */ /* - V01.06.00 Softrule V_SR_CompanyCodeForOptravis_V1 included */ /* - V01.05.00 Reworked view to use new CO-PA RAWVault and added Field ProfitCenter */ /* - V01.04.00 Added column SourceSystem (2021-02-10) */ /* - V01.03.00 Rename MaterialOrig to Material; Add SalesDocumentType (2020-12-16) */ /* - V01.02.00 Adjust TotalNetSales calculation based on changed customer requirement */ /* Use new MDS-based tables for CompanyCodeScope definition (2020-11-11) */ /* - V01.01.00 Replace WWR04 by ARTNR as source for MaterialOrig (2020-10-19) */ /* - V01.00.01 Re-worked based on refined customer requirement (2020-09-30) */ /* - V01.00.00 Initial version (2020-09-03) */ /* =*/"
    chat_template_2 = """
    Name der View: V_INTF_PnL_G3
    Beschreibung: Interface view for transfer of monthly sales transactions data to Optravis
    Links zur internen Dokumentation: https://inside-docupedia.bosch.com/confluence/pages/viewpage.action?pageId=1767424464
    Outgoing Interface: Nicht angegeben
    Restrictions: Restricted to certain company codes (legal entities in the scope of BBM)
    """
    chat_template_3 = "Bitte extrahiere den Namen der View, die Beschreibung, Links zur internen Dokumentation, das Outgoing Interface und Restrictions aus dem folgenden Text falls vorhanden. Gebe bei den Links nur die Links ohne weitere Zusätze an. Stelle die Informationen Stichpunktartig dar, ohne Bullet Points oder ähnliches zu verwenden: {system}"

    counter = 0
    for index, row in complete_df.iterrows():
        formated_chat_3 = chat_template_3.format(system=row['ViewDescription'])
        print("Going to call OpenAI API")
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
        counter = counter + 1
        print("Called OpenAI API, counter: ", counter)
        collection.add(documents=row["ViewDescription"],
                   metadatas=[{"ObjectName": row["ObjectName"], "SAP-System": row["ObjectName"][-2:], "View-Description": response['choices'][0]['message']['content']}],
                   ids=[str(row["ObjectID"])])
        print("Added to vector database")


    
