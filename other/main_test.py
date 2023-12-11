from database_utils import DatabaseConnector as dc
from data_extraction import DataExtractor as dex
from data_cleaning import DataCleaning as dcl
import missingno as msno # Visualising Missing Data
import plotly.express as px # Visualising histogram


import pandas as pd
import numpy as np
import nbformat # save as .ipynb

def setup_and_extract_data(): # Step 1: Specify the correct file path
    database_connector = dc()
    credentials = database_connector.read_db_creds(file_path)    # Step 2: Read credentials
    engine = database_connector.init_db_engine(credentials)      # Step 3: Initialise database engine
    data_extractor = dex()

    # Step 4: List all tables in the database
    tables = data_extractor.list_db_tables(engine)
    
    # Display the list of tables to the user
    print("Available Tables:")
    for i, table_name in enumerate(tables, 1):
        print(f"{i}. {table_name}")

    # Get user input for table selection
    table_index = input("Enter the number corresponding to the table you want to extract: ")

    try:
        # Convert the input to an integer and get the selected table name
        selected_index = int(table_index) - 1
        selected_table = tables[selected_index]

        # Step 5: Read the selected table into a pandas DataFrame
        selected_table_df = data_extractor.read_rds_table(selected_table, engine)

        # Display the DataFrame
        print(selected_table_df)

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
        
        return selected_table_df, selected_table

    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid number corresponding to the table.")
    
    return None


if __name__ == "__main__":
    selected_table_df = setup_and_extract_data()
    if selected_table_df is not None:
        # Clean the selected table DataFrame
        cleaned_table_df = dcl.clean_user_data(selected_table_df)

        # Display the cleaned DataFrame
        print("Cleaned DataFrame:")
        print(cleaned_table_df)

        # Save the cleaned DataFrame as a CSV file
        cleaned_csv_filename = f"cleaned_{selected_table}_data.csv"
        cleaned_table_df.to_csv(cleaned_csv_filename, index=False)
        print(f"Saved cleaned {selected_table} DataFrame as {cleaned_csv_filename}")

if __name__ == "__main__":
    selected_table, selected_table_df = setup_and_extract_data()
 
    # Clean the selected table DataFrame
    cleaned_table_df = dcl.clean_user_data(selected_table_df)
    print("Cleaned DataFrame:")
    print(cleaned_table_df)

    # Save the cleaned DataFrame as a CSV file
    cleaned_csv_filename = f"cleaned_{selected_table}_data.csv"
    cleaned_table_df.to_csv(cleaned_csv_filename, index=False)
    print(f"Saved cleaned {selected_table} DataFrame as {cleaned_csv_filename}")
