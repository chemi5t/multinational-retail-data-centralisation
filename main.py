from database_utils import DatabaseConnector as dc
from data_extraction import DataExtractor as dex
from data_cleaning import DataCleaning as dcl
# import missingno as msno # Visualising Missing Data
# import plotly.express as px # Visualising histogram

import pandas as pd
# import numpy as np
import nbformat # save as .ipynb

from decouple import config #  calling sensitive information
import yaml # to read .yaml. Help with read_db


def setup_and_extract_data(file_path='db_creds.yaml'): # Step 1: Specify the correct file path
    database_connector = dc()
    credentials = database_connector.read_db_creds(file_path)    # Step 2: Read credentials
    engine, engine2 = database_connector.init_db_engine(credentials)      # Step 3: Initialise database engine
    data_extractor = dex()

    # Step 4: List all tables in the database
    tables = data_extractor.list_db_tables(engine)
    
    # Display the list of tables to the user
    # Available Tables: ['legacy_store_details', 'legacy_users', 'orders_table']  
    print("\nAvailable Tables: \n")
    for i, table_name in enumerate(tables, 1):
        print(f"{i}. {table_name}")

    # Get user input for table selection
   
    table_index = 2
    selected_index = table_index - 1
    selected_table = tables[selected_index]
    print(f"\nTable 2. '{selected_table}', shall be extracted. \n")

    # Step 5: Read the selected table into a pandas DataFrame
    selected_table_df = data_extractor.read_rds_table(selected_table, engine)

    # Display the DataFrame
    print(selected_table_df, "\n")

    # Save the DataFrame as a CSV file
    csv_filename = f"{selected_table}_data.csv"
    selected_table_df.to_csv(csv_filename, index=False)
    print(f"Saved {selected_table} DataFrame as {csv_filename}")

    # Create a new notebook
    notebook = nbformat.v4.new_notebook()
    # Add a code cell for the table to the notebook
    code_cell = nbformat.v4.new_code_cell(f"import pandas as pd\n"
                                            f"from database_utils import DatabaseConnector as dc\n\n"
                                            f"database_connector = dc()\n"
                                            f"credentials = database_connector.read_db_creds('{file_path}')\n"
                                            f"engine = database_connector.init_db_engine(credentials)\n\n"
                                            f"# Import data from '{selected_table}' table into DataFrame\n"
                                            f"{selected_table}_df = pd.read_sql('{selected_table}', engine)\n\n"
                                            f"# Display the DataFrame\n"
                                            f"{selected_table}_df")
                                            
    notebook.cells.append(code_cell)

    # Save the notebook to a .ipynb file with a name based on the selected table
    notebook_file = f"{selected_table}_data.ipynb"
    with open(notebook_file, 'w') as nb_file:
        nbformat.write(notebook, nb_file)
        print(f"Saved {selected_table} DataFrame as {selected_table}_data.ipynb\n")
    
    
    return selected_table_df, selected_table, engine2

def save_dataframe(card_details_df): # Step 1: Specify the correct file path

    # Save the DataFrame as a CSV file
    csv_filename = f"{selected_table}_data.csv"
    selected_table_df.to_csv(csv_filename, index=False)
    print(f"Saved {selected_table} DataFrame as {csv_filename}")

    # Create a new notebook
    notebook = nbformat.v4.new_notebook()
    # Add a code cell for the table to the notebook
    code_cell = nbformat.v4.new_code_cell(f"import pandas as pd\n"
                                            f"from database_utils import DatabaseConnector as dc\n\n"
                                            f"database_connector = dc()\n"
                                            f"credentials = database_connector.read_db_creds('{file_path}')\n"
                                            f"engine = database_connector.init_db_engine(credentials)\n\n"
                                            f"# Import data from '{selected_table}' table into DataFrame\n"
                                            f"{selected_table}_df = pd.read_sql('{selected_table}', engine)\n\n"
                                            f"# Display the DataFrame\n"
                                            f"{selected_table}_df")
                                            
    notebook.cells.append(code_cell)


if __name__ == "__main__":

    # cleaner = dcl()
    # cleaner.

    selected_table_df, selected_table, engine2 = setup_and_extract_data()

    # Clean the selected table DataFrame
    cleaned_table_df = dcl.clean_user_data(selected_table_df)

    print(f"\nCleaned '{selected_table}' DataFrame: \n")
    print(cleaned_table_df, "\n")

    # Save the cleaned DataFrame as a CSV file
    cleaned_csv_filename = f"{selected_table}_data_cleaned.csv"
    cleaned_table_df.to_csv(cleaned_csv_filename, index=False)
    print(f"Saved cleaned '{selected_table}' DataFrame as '{cleaned_csv_filename}'.")

    # Upload the cleaned data to the database
    dc.upload_to_db(cleaned_table_df, 'dim_users', engine2)

    # Retrieve PDF from AWS S3 bucket and convert to CSV
    card_details_df, table_name, csv_filename = dex.retrieve_pdf_data()
   
    cleaned_card_details_df = dcl.clean_card_data(card_details_df)

    print(f"\nCleaned '{table_name}' DataFrame: \n")
    print(cleaned_card_details_df, "\n")

    # Save the cleaned DataFrame as a CSV file
    cleaned_csv_filename = f"{table_name}_data_cleaned.csv"
    cleaned_card_details_df.to_csv(cleaned_csv_filename, index=False)
    print(f"Saved cleaned '{table_name}' DataFrame as '{cleaned_csv_filename}'.")

    # Upload the cleaned data to the database
    dc.upload_to_db(cleaned_card_details_df, 'dim_card_details', engine2)

    # API section

    # to gain access to private credentials for API
    cred_access = config('credentials_env') # refers to .yaml file
    api_connector = dc()
    cred_api = api_connector.read_db_creds(file_path = cred_access) # extracts the .yaml file

    x_api_key = cred_api['api_key'] # access the .yaml key
    headers = {'x-api-key': x_api_key}

    number_of_stores_endpoint = cred_api['number_of_stores_endpoint']
    retrieve_a_store_endpoint = cred_api['retrieve_a_store_endpoint']

    api_extractor = dex()

    # retrieve the number of stores
    number_of_stores = api_extractor.list_number_of_stores(number_of_stores_endpoint, headers)
    print(f"\nRetrieving the number of stores: {number_of_stores}")

    # retrieve data for all stores and save in a Pandas df
    stores_df = api_extractor.retrieve_stores_data(retrieve_a_store_endpoint, headers, number_of_stores)

    if stores_df is not None:
        print("Stores data:")
        print(stores_df)
    else:
        print("Failed to retrieve stores data.")


