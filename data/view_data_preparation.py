import pandas as pd
import numpy as np

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
    
    # Filter for the create view entries (no create function or database entries)
    df = df[df['ObjectSQLCode_First_32767_Characters'].str.contains(r'(?i)\bcreate\s+view\b', regex=True)]
    
    # Drop the actual view definition and keep only the description
    df['ObjectSQLCode_First_32767_Characters'] = df['ObjectSQLCode_First_32767_Characters'].str.replace(r'(?i)\bcreate\s+view\b.*$', '', case=False, regex=True)
    
    # Drop the unnecessary characters 
    df['ObjectSQLCode_First_32767_Characters'] = df['ObjectSQLCode_First_32767_Characters'].apply(clean_content)
    
    # Replace empty strings with NaN
    df['ObjectSQLCode_First_32767_Characters'].replace('', np.nan, inplace=True)
    
    # Drop rows with NaN in 'ObjectSQLCode_First_32767_Characters' column
    df.dropna(subset=['ObjectSQLCode_First_32767_Characters'], inplace=True)
    
    df.to_csv('View_Data_Information.csv', sep=';', index=False)

reduce_view_data_information()

