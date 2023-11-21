import streamlit as st
import openai
import os
from vector_database_setup import get_collection

# Setup
setup_messages = [
        {"role": "system", "content": "Du bist ein Datenbankexperte, der nur Fragen über gegebene Daten und Datenstrukturen beantwortet und SQL Code schreibt und erklärt"},
        {"role": "system", "content": """Gegeben ist eine Datenbank mit folgenden Attributen: 
         SchemaName;SchemaID;DataCORELayer;ObjectName;ObjectID;ObjectType;ObjectTypeDescription;ObjectSQLCode_Anzahl_Character;ObjectSQLCode_First_32767_Characters
         Dabei ist die ObjectID einzigartig, d.h. Einträge können darüber identifiziert werden.
         Der ObjectName enthält das SAP-System aus dem die Daten stammen als Präfix in der Form *_SAP-System wobei SAP-Systeme immer zwei Zeichen lang sind
         Die Datenbank heißt Interface_Definition.
         """},
         {"role": "system", "content": """
          Ein SAP-System, z.B. D4 kann wie folgt abgefragt werden:
          SELECT * FROM Interface_Definition WHERE ObjectName LIKE "%_D4"
          """}
    ]

st.set_page_config(page_title="Bosch Data Prototype")
collection = get_collection()
openai.api_key = os.environ.get('OPENAI_API_KEY')
if 'sap_system' not in st.session_state:
    st.session_state.sap_system = ''
if 'use_case' not in st.session_state:
    st.session_state.use_case = ''
if 'messages' not in st.session_state:
    st.session_state.messages = setup_messages
if 'user_input' not in st.session_state:
    st.session_state.user_input = ''

def reset_inputs():
    st.session_state["sap_system"] = ''
    st.session_state["use_case"] = ''
    st.session_state["messages"] = setup_messages
    st.session_state["user_input"] = ''

def get_relevance_for_distance(distance):
    if 0 <= distance <= 0.16:
        return "Hoch"
    elif 0.17 <= distance <= 0.33:
        return "Mittel"
    else:
        return "Gering"

def update_chat():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                temperature = 0,
                messages = st.session_state.messages
            )
        st.session_state.messages.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})

        st.session_state.user_input = ""

def display_chat():
    with st.container():
        for message in st.session_state.messages[3:]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        st.text_input("Stelle Fragen zu SQL oder der Datenbank", key="user_input", on_change=update_chat)
        st.divider()

def display_results(result):
    with st.container():
        if len(result["ids"][0]) == 0:
            st.title("Keine Ergebnisse")
            st.caption("Für das gewählte SAP-System liegen keine Daten vor")
        for i in range(0, len(result["ids"][0])):
            metadata = result["metadatas"][0][i]
            relevance = get_relevance_for_distance(result["distances"][0][i])
            st.title(f"{i+1}. Ergebnis")
            metrics = st.columns([3, 1, 1])
            metrics[0].metric("View", metadata["ObjectName"], help="ObjectName der View")
            metrics[1].metric("SAP-System", metadata["SAP-System"], help="Name des SAP-Systems, der aus dem ObjectName extrahiert wird")
            metrics[2].metric("Relevanz", relevance, round(result["distances"][0][i], 2), "off", help="Indikation wie relevant das Ergebnis ist basierend auf der Cosine Distance in der Vektordatenbank")
            st.subheader("Zusammenfassung der View:")
            st.text(metadata["View-Description"])
            with st.expander("Originalbeschreibung"):
                st.write(result["documents"][0][i])
            st.write("---")

def show_results(result):
    tab_result, tab_chat = st.tabs(["Ergebnis", "Chatbot"])
    with tab_result:
        display_results(result)
    with tab_chat:
        display_chat()
    st.button("Reset", on_click=reset_inputs)

def query_sap_system(sap_system: str) -> []:
    return collection.get(where={"SAP-System": sap_system})

def query_use_case(use_case: str, sap_system: str = None, number_of_views: int = 3) -> []:
    if sap_system is not None:
        return collection.query(query_texts=[use_case], where={"SAP-System": sap_system}, n_results=number_of_views)
    else:
        return collection.query(query_texts=[use_case], n_results=number_of_views)

# Header
with st.container():
    st.title("View Finder")
    st.subheader("Findet SAP-Systeme, die bereits im Access Layer durch Views dargestellt werden und findet die relevantesten Views für einen Use Case")

with st.form("input_form"):
    header = st.columns([2, 2])
    header[0].subheader("SAP-System das gesucht werden soll")
    header[1].subheader("Kurze Beschreibung auf ENGLISCH welche Daten benötigt werden")
    input_row = st.columns([2, 2])
    sap_system = input_row[0].text_input("SAP-System", key="sap_system")
    use_case = input_row[1].text_area("Kurzbeschreibung", key="use_case")
    number_of_views = input_row[1].selectbox("Wie viele Ergebnisse sollen angezeigt werden?", (1, 2, 3, 4, 5))
    submit = st.form_submit_button(label="Suchen")

with st.container():
    if len(sap_system) > 0:
        if len(sap_system) == 2:
            sap_result = query_sap_system(sap_system)
            sap_status = "modelliert" if len(sap_result["ids"]) > 0 else "nicht modelliert"
            st.title("SAP-System: {}".format(sap_system))
            metrics = st.columns([2, 2])
            metrics[0].metric("Status", sap_status)
            metrics[1].metric("Anzahl Views", len(sap_result["ids"]))
        else:
            st.title(":red[Ungültiges SAP-System!]")
            st.caption("SAP-Systeme bestehen aus genau zwei Zeichen, z.B. 'D0'")
        st.divider()

with st.container():
    if len(use_case) > 0:
        if len(sap_system) > 0:
            use_case_result = query_use_case(use_case, sap_system, number_of_views)
        else:
            use_case_result = query_use_case(use_case, number_of_views=number_of_views)
        show_results(use_case_result)