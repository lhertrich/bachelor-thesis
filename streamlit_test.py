import streamlit as st

def clear_form():
    st.session_state["sap_system"] = ""
    st.session_state["use_case"] = ""

with st.form("input_form"):
    c1, c2 = st.columns([1, 1])
    with c1:
        st.text_input("SAP-System", key="sap_system")
    with c2:
        st.text_input("Beschreibung auf Englisch", key="use_case")
    submit = st.form_submit_button(label="Suchen")

if submit:
    st.write("Result")
    clear = st.button(label="Neue Suche", on_click=clear_form)
    
    