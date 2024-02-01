from data_cleaning import DataCleaning as dcl
from data_extraction import DataExtractor as dex
from database_utils import DatabaseConnector as dc
from decouple import config #  calling sensitive information

import nbformat # save as .ipynb
import pandas as pd
import yaml # to read .yaml. Help with read_db  
import pandas as pd
from database_utils import DatabaseConnector as dc

import numpy as np
import nbformat
import plotly.express as px
import missingno as msno
import re
from dateutil.parser import parse # to help with datatime edits
from IPython.display import display
import requests
    

def setup_and_extract_data(file_path='db_creds.yaml', table_index = 2): # Step 1: Specify the correct file path
    database_connector = dc()
    credentials = database_connector.read_db_creds(file_path)    # Step 2: Read credentials
    engine, engine2 = database_connector.init_db_engine(credentials)      # Step 3: Initialise database engine
    data_extractor = dex()

    # Step 4: List all tables in the database
    tables = data_extractor.list_db_tables(engine)
    
    # Display the list of tables to the user
    # Available Tables: ['legacy_store_details', 'legacy_users', 'orders_table']  i.e. table 1, 2, 3 respectively (indices 0, 1, 2 respectively)
    print("\nAvailable Tables: \n")
    for i, table_name in enumerate(tables, 1):
        print(f"{i}. {table_name}")

    # Get user input for table selection
   
    table_index
    selected_index = table_index - 1
    selected_table = tables[selected_index]
    print(f"\nTable {table_index}. '{selected_table}', shall be extracted. \n")

    # Step 5: Read the selected table into a pandas DataFrame
    selected_table_df = data_extractor.read_rds_table(selected_table, engine)

    # Display the DataFrame
    print(selected_table_df, "\n")

    # Save the DataFrame as a CSV file
    csv_filename = f"{selected_table}.csv"
    selected_table_df.to_csv(csv_filename, index=True)
    print(f"Saved {selected_table} DataFrame as {csv_filename}")

    # Create a new notebook
    notebook = nbformat.v4.new_notebook()
    # Add a code cell for the table to the notebook
    code_cell = nbformat.v4.new_code_cell(f"import pandas as pd\n"
                                            f"from database_utils import DatabaseConnector as dc\n\n"
                                            f"database_connector = dc()\n"
                                            f"credentials = database_connector.read_db_creds('{file_path}')\n"
                                            f"engine, _ = database_connector.init_db_engine(credentials)\n\n"
                                            f"# Import data from '{selected_table}' table into DataFrame\n"
                                            f"{selected_table}_df = pd.read_sql('{selected_table}', engine)\n\n"
                                            f"# Display the DataFrame\n"
                                            f"{selected_table}_df")
                                            
    notebook.cells.append(code_cell)

    # Save the notebook to a .ipynb file with a name based on the selected table
    notebook_file = f"{selected_table}.ipynb"
    with open(notebook_file, 'w') as nb_file:
        nbformat.write(notebook, nb_file)
        print(f"Saved {selected_table} DataFrame as {selected_table}_data.ipynb\n")
    
    
    return selected_table_df, selected_table, engine2

def called_clean_store_data(store_details_df):
    # Filter and include rows where 'lat' values are isnull
    store_details_df_filtered = store_details_df[store_details_df['lat'].isnull()]

    store_details_df_filtered = store_details_df_filtered.drop('lat', axis=1)

                # # Filter and exclude rows where 'longitude' values are isnull i.e. we want notnull rows
                # store_details_df_filtered = store_details_df_filtered[store_details_df_filtered['longitude'].notnull()]

    # Filter and exclude rows where 'store_code' values are isnull i.e. we want notnull rows
    store_details_df_filtered = store_details_df_filtered[store_details_df_filtered['store_code'].notnull()]

    # Filter out letters from the 'staff_numbers'
    store_details_df_filtered['staff_numbers'] = store_details_df_filtered['staff_numbers'].str.replace(r'[^0-9]', '', regex=True)
    store_details_df_filtered['staff_numbers'] = store_details_df_filtered['staff_numbers'].astype('int64')

    # Change datatype
    store_details_df_filtered['store_type'] = store_details_df_filtered['store_type'].astype('category')
    store_details_df_filtered['store_code'] = store_details_df_filtered['store_code'].astype('string')
    store_details_df_filtered['country_code'] = store_details_df_filtered['country_code'].astype('category')

    # Replace 'eeEurope': 'Europe', 'eeAmerica': 'America'
    store_details_df_filtered['continent'] = store_details_df_filtered['continent'].replace({'eeEurope': 'Europe', 'eeAmerica': 'America'})
    store_details_df_filtered['continent'] = store_details_df_filtered['continent'].astype('category')

    # Change datatype to string
    store_details_df_filtered['address'] = store_details_df_filtered['address'].astype('string')
    store_details_df_filtered['locality'] = store_details_df_filtered['locality'].astype('string')

    # Convert the 'opening_date' column to datetime format
    store_details_df_filtered['opening_date'] = store_details_df_filtered['opening_date'].apply(parse)
    # To handle specific formats
    # store_details_df_filtered['opening_date'] = store_details_df_filtered['opening_date'].combine_first(pd.to_datetime(store_details_df_filtered['opening_date'], errors='coerce', format='%Y %B %d'))
    store_details_df_filtered['opening_date'] = store_details_df_filtered['opening_date'].combine_first(pd.to_datetime(store_details_df_filtered['opening_date'], errors='coerce', format='mixed'))
    # Convert 'expiry_date' to datetime format
    # store_details_df_filtered['opening_date'] = pd.to_datetime(store_details_df_filtered['opening_date'], format='%y-%m-%d', errors='coerce')
    store_details_df_filtered['opening_date'] = pd.to_datetime(store_details_df_filtered['opening_date'], format='mixed', errors='coerce')

    print(store_details_df_filtered.info())
    print(store_details_df_filtered)

    return store_details_df_filtered
    
##############################################################################################
# Upload the cleaned data to the database
api_connector = dc()
api_extractor = dex() 
 # Clean the selected table DataFrame
data_cleaner = dcl() # cleaning the leagacy user data 

selected_table_df, selected_table, engine2 = setup_and_extract_data(table_index = 2)

# to gain access to private credentials for API
cred_access = config('credentials_env') # refers to .yaml file ## from decouple import config
cred_api = api_connector.read_db_creds(file_path = cred_access) # extracts the .yaml file

x_api_key = cred_api['api_key'] # access the .yaml key
headers = {'x-api-key': x_api_key}

number_of_stores_endpoint = cred_api['number_of_stores_endpoint']
retrieve_a_store_endpoint = cred_api['retrieve_a_store_endpoint']

# retrieve the number of stores
number_of_stores = api_extractor.list_number_of_stores(number_of_stores_endpoint, headers)
print(f"The number of stores to retrieve data from: {number_of_stores}")

# retrieve data for all stores and save in a Pandas df
stores_df, table_name, csv_filename = api_extractor.retrieve_stores_data(retrieve_a_store_endpoint, headers, number_of_stores)

if stores_df is not None:
    print(f"'{table_name}', shall be extracted. \n")
    print(stores_df, "\n")
else:
    print("Failed to retrieve stores data.")

cleaned_store_df = called_clean_store_data(stores_df)

print(f"Cleaned '{table_name}' DataFrame: \n")
print(cleaned_store_df, "\n")

# Save the cleaned DataFrame as a CSV file
cleaned_csv_filename = f"{table_name}_data_cleaned.csv"
cleaned_store_df.to_csv(cleaned_csv_filename, index=False)
print(f"Saved cleaned '{table_name}' DataFrame as '{cleaned_csv_filename}'.")

# Upload the cleaned data to the database
api_connector.upload_to_db(cleaned_store_df, 'dim_store_details', engine2)