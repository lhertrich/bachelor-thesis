import streamlit as st
from vector_database_setup import get_collection

# Setup
st.set_page_config(page_title="Bosch Data Prototype")
collection = get_collection()

# Header
with st.container():
    st.title("View Finder")
    st.subheader("Finde SAP-Systeme, die bereits in der Result Zone durch Views dargestellt werden und finde die relevantesten Views für einen Use Case")

def get_relevance_for_distance(distance):
    if -0.3 <= distance <= 0.3:
        return "Hoch"
    elif -0.6 <= distance <= 0.6:
        return "Mittel"
    else:
        return "Gering"

def show_results(result):
    with st.container():
        st.write(result)
        st.write(len(result["ids"][0]))
        for i in range(0, len(result["ids"][0])):
            relevance = get_relevance_for_distance(result["distances"][0][i])
            st.subheader(f"{i+1}. Ergebnis")
            st.write("Relevanz: ", relevance)
            st.text(result["metadatas"][0][i]["View-Description"])
            
            st.write("---")
      
        another_search_button = st.button("Search for another SAP-System", key="another_search_button")
        if another_search_button:
            st.session_state["sap_system_valid"] = None

def query_views():
    with st.container():
        use_case = st.text_input("Bitte geben Sie eine kurze Beschreibung auf ENGLISCH wofür die Daten des SAP-Systems benötigt werden", key="use_case")
        search_use_case_button = st.button("Suche Views", key="search_use_case_button")
        if search_use_case_button and use_case:
            query_result = collection.query(query_texts=[use_case], where={"SAP-System": st.session_state.sap_system}, n_results=3)
            st.write(show_results(query_result))

def search_sap_system():
    with st.container():
        sap_system = st.text_input("Welches SAP-System soll gesucht werden?", key="sap_system")
        search_sap_button = st.button("Suche SAP-System", key="search_sap_button")
        if search_sap_button:
            if len(sap_system) == 2:
                sap_result = collection.get(where={"SAP-System": sap_system})
                number_of_results = len(sap_result["ids"])
                if number_of_results > 0:
                    st.session_state["sap_system_valid"] = sap_system
                    st.write(f"Es existieren {number_of_results} Views für das SAP-System {sap_system}")
                else: 
                    st.write(f"Es existieren noch keine Views für das SAP-System {sap_system}")
            elif sap_system:
                st.write("Ungültiges SAP-System! SAP-Systeme müssen zwei Zeichen lang sein, z.B. 'D4'")        
    
search_sap_system()

if "sap_system_valid" in st.session_state and st.session_state["sap_system_valid"] is not None:
    query_views()

