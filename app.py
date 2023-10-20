from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate
from database_connection import DatabaseConnection
import re

llm = OpenAI(openai_api_key='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', temperature=0)

init_template = "Du bist ein Datenbankexperte der Wissen über eine Datenbanktabelle table_view_field_definition hat. Die Tabelle hat folgende Attribute: DatabaseName, ModelCode, EntityClassCode, EntityStereotype, Comment. Das Attribut EntityClassCode ist wie folgt aufgebaut: Präfix_SAP-Tabellenname_SAP-System."
dialog_template_1 = "Bitte gebe eine SQL Abfrage aus mit der sich überprüfen lässt, ob das SAP-System B2 bereits in der Tabelle enthalten ist."
dialog_template_2 = "SELECT COUNT(*) FROM table_view_field_definition WHERE EntityClassCode LIKE '%B2';"
dialog_template_3 = "Bitte gebe eine SQL Abfrage aus mit der sich überprüfen lässt, ob das SAP-System GK bereits in der Tabelle enthalten ist."
dialog_template_4 = "SELECT COUNT(*) FROM table_view_field_definition WHERE EntityClassCode LIKE '%GK';"
template = "Gegeben ist eine Datenbanktabelle table_view_field_definition mit folgenden Attributen: DatabaseName, ModelCode, EntityClassCode, EntityStereotype, Comment. Das Attribut EntityClassCode ist wie folgt aufgebaut: Präfix_SAP-Tabellenname_SAP-System. Bitte gebe eine SQL Abfrage aus mit der sich überprüfen lässt, ob das SAP-System {system} bereits in der Tabelle enthalten ist. Dafür muss geprüft werden ob ein EntityClassCode existiert, der auf das SAP-System endet."

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", init_template),
    ("human", dialog_template_1),
    ("ai", dialog_template_2),
    ("human", dialog_template_3),
    ("ai", dialog_template_4),
    ("human", template)
])

while True:
    user_input = input("Welches SAP System soll gesucht werden? (type 'quit' to quit): ")
    if user_input.lower() == "quit":
        break

    messages = chat_prompt.format_messages(system=user_input)
    answer = llm.predict_messages(messages).content
    match = re.search(r'AI: (\bSELECT\b.*)', answer)

    if match:
        corrected_answer = match.group(1)
    else:
        print("Sorry there was a mistake from the LLM, application has to be started again")
        break

    db_connection = DatabaseConnection()
    result = db_connection.execute_query(corrected_answer)
    print(result)

    if result[0][0] > 0:
        print("System {name} is modelled".format(name=user_input))
    else:
        print("System {name} is not modelled".format(name=user_input))

    interface_sql_code = "SELECT COUNT(*) from interface_definition WHERE ObjectName LIKE '%{}'"
    views = db_connection.execute_query(interface_sql_code.format(user_input))
    print(views)

    next_system = input("Soll ein weiteres System gesucht werden? (y/n)")
    if next_system.lower() == "n" or next_system.lower() == "no":
        break

