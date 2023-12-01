from database_utils import DatabaseConnector as dc
from data_extraction import DataExtractor as dex
from data_cleaning import DataCleaning as dcl
import missingno as msno # Visualising Missing Data
import plotly.express as px # Visualising histogram


import pandas as pd
import numpy as np
import nbformat # save as .ipynb

def setup_and_extract_data(file_path='db_creds.yaml'): # Step 1: Specify the correct file path
    database_connector = dc()
    credentials = database_connector.read_db_creds(file_path)    # Step 2: Read credentials
    engine = database_connector.init_db_engine(credentials)      # Step 3: Initialise database engine
    data_extractor = dex()

    # Rest of your code for extracting data and saving the notebook
    tables = data_extractor.list_db_tables(engine)   
    # Available Tables: ['legacy_store_details', 'legacy_users', 'orders_table']            
    print("Available Tables: ", tables)                          # Step 4: List all tables in the database
    for table_name in tables:
        # Create a new notebook
        notebook = nbformat.v4.new_notebook()
        # Add a code cell for each table to the notebook
        code_cell = nbformat.v4.new_code_cell(f"import pandas as pd\n"
                                              f"from database_utils import DatabaseConnector as dc\n\n"
                                              f"database_connector = dc()\n"
                                              f"credentials = database_connector.read_db_creds('{file_path}')\n"
                                              f"engine = database_connector.init_db_engine(credentials)\n\n"
                                              f"# Import data from '{table_name}' table into DataFrame\n"
                                              f"{table_name}_df = pd.read_sql('{table_name}', engine)\n\n"
                                              f"# Display the DataFrame\n"
                                              f"{table_name}_df")
                                              
        notebook.cells.append(code_cell)
        
        # Save the notebook to a .ipynb file with a name based on the table
        notebook_file = f"{table_name}_data.ipynb"
        with open(notebook_file, 'w') as nb_file:
            nbformat.write(notebook, nb_file)

if __name__ == "__main__":
    setup_and_extract_data()