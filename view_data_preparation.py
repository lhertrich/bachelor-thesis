import pandas as pd

def read_file():
    return pd.read_csv(r'3_Interface_Definition.csv', sep=';')

def reduce_view_data_create_view():
    df = read_file()
    df['ObjectSQLCode_First_32767_Characters'] = df['ObjectSQLCode_First_32767_Characters'].str.replace(r'^.*?create view', 'create view', case=False, regex=True)
    df.to_csv('View_Data_createView.csv', sep=';', index=False)

def clean_content(content):
    # Remove /* and */
    #content = content.replace("/*", "").replace("*/", "")
    # Remove sequences of =- and -=
    content = content.replace("=-", "").replace("-=", "")
    # Remove sequences of ==
    content = content.replace("==", "")
    # Remove sequences of multiple spaces with a single space
    content = " ".join(content.split())
    return content
    
def reduce_view_data_information():
    df = read_file()
    df['ObjectSQLCode_First_32767_Characters'] = df['ObjectSQLCode_First_32767_Characters'].str.replace(r'create view.*$', '', case=False, regex=True)
    df['ObjectSQLCode_First_32767_Characters'] = df['ObjectSQLCode_First_32767_Characters'].apply(clean_content)
    df.to_csv('View_Data_Information.csv', sep=';', index=False)

reduce_view_data_information()

