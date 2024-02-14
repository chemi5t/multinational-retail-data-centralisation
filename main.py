import nbformat # save as .ipynb
import pandas as pd
import yaml # to read .yaml. Help with read_db
import os # to create directories

from _06_multinational_retail_data_centralisation.data_cleaning import DataCleaning as dcl
from _06_multinational_retail_data_centralisation.data_extraction import DataExtractor as dex
from _06_multinational_retail_data_centralisation.database_utils import DatabaseConnector as dc
from decouple import config # Calling sensitive information

############################################################################################################################################################
# Initialise instances
data_cleaner = dcl()
api_connector = dc()
data_extractor = dex()

cred_path='db_creds.yaml'

credentials = api_connector.read_db_creds(file_path = cred_path)    # Read .yaml for credentials
engine, engine2 = api_connector.init_db_engine(credentials)      # Initialise database engine

cred_config_access = config('credentials_env') # refers to .yaml file via decouple import config; to gain access to private credentials for API
cred_config_api = api_connector.read_db_creds(file_path = cred_config_access) # extracts the credentials from .yaml file

# Define file paths
raw_csv_folder_path = '_01_raw_tables_csv'  # Define the folder path where you want to save the CSV files
raw_notebook_folder_path = '_02_manipulate_raw_tables_ipynb'  # Define the folder path where you want to save the notebooks
cleaned_csv_folder_path = '_03_cleaned_tables_csv'  # Define the folder path where you want to save the cleaned CSV files

############################################################################################################################################################

def setup_and_extract_data(cred_path: str, table_index: int = 2): # Step 1: Specify the correct file path
    """
    The setup_and_extract_data function sets up database connection and extracts data from selected table.
    Lists all tables in the database, and prompts user (bt this has been hard coded) to select a table to extract data from (defaults to index 2).
    Reads the selected table into a pandas DataFrame, displays it, then saves it as a CSV file in the specified folder path (raw_csv_folder_path). 
    The CSV filename is named after the name of the selected table with .csv extension appended at end of filename e.g orders_table -&gt; orders_table.csv
        
    Args:
        cred_path (str): Path to the credentials file.
        table_index (int): Index of the table to extract data from.

    Returns:
        tuple: DataFrame containing selected table data, name of the selected table and database engine.
    """
    tables = data_extractor.list_db_tables(engine)  # Step 4: List all tables in the database
    print("Available Tables:\n") 
    for i, table_name in enumerate(tables, 1):  # Available Tables: ['legacy_store_details', 'legacy_users', 'orders_table']  i.e. table 1, 2, 3 (indices 0, 1, 2 respectively)
        print(f"{i}. {table_name}")

    selected_index = table_index - 1  # User input for table has been predefined
    selected_table = tables[selected_index]
    print(f"Table {table_index}. '{selected_table}', shall be extracted.\n")

    selected_table_df = data_extractor.read_rds_table(selected_table, engine)  # Step 5: Read the selected table into a pandas DataFrame

    print(selected_table_df, "\n")  # Display the DataFrame

    os.makedirs(raw_csv_folder_path, exist_ok=True) # Ensure that the folder exists, create it if it doesn't
    raw_csv_filename = os.path.join(raw_csv_folder_path, f"{selected_table}.csv")  # Save the DataFrame as a CSV file in the specified folder
    selected_table_df.to_csv(raw_csv_filename, index=True)
    print(f"Saved {selected_table} DataFrame as {raw_csv_filename}. \n")

    os.makedirs(raw_notebook_folder_path, exist_ok=True)  # Ensure that the folder exists, create it if it doesn't
    notebook = nbformat.v4.new_notebook()  # Create a new notebook and add a code cell for the table to the notebook
    code_cell = nbformat.v4.new_code_cell( f"import pandas as pd\n"
                                            f"from _06_multinational_retail_data_centralisation.database_utils import DatabaseConnector as dc\n\n"
                                            f"api_connector = dc()\n"
                                            f"credentials = api_connector.read_db_creds('{cred_path}')\n"
                                            f"engine, _ = api_connector.init_db_engine(credentials)\n"
                                            f"# Import data from '{selected_table}' table into DataFrame\n"
                                            f"{selected_table}_df = pd.read_sql('{selected_table}', engine)\n"
                                            f"# Display the DataFrame\n"
                                            f"{selected_table}_df")         
    notebook.cells.append(code_cell)

    raw_notebook_filename = os.path.join(raw_notebook_folder_path, f"{selected_table}.ipynb")  # Save the notebook to a .ipynb file in the specified folder
    with open(raw_notebook_filename, 'w') as nb_file:
        nbformat.write(notebook, nb_file)
        print(f"Saved {selected_table} DataFrame as {raw_notebook_filename}.\n")

    return selected_table_df, selected_table, engine2

def one_etl_leagacy_users():
    """
    The one_etl_leagacy_users function extracts, transforms, and loads data for legacy users.
    It first sets up the database connection and extracts the specified table's data as a DataFrame.
    Then it cleans that DataFrame using the clean_user_data function from our data_cleaner module.
    It saves that cleaned DataFrame as a CSV file in our cleaned CSVs folder.
    Finally, it uploads that cleaned DataFrame to pgAdmin 4 using SQLAlchemy.   
    """
    selected_table_df, selected_table, engine2 = setup_and_extract_data(cred_path = cred_path, table_index = 2)
    cleaned_user_df = data_cleaner.clean_user_data(selected_table_df)  # Clean the selected table DataFrame
    print(f"Cleaned '{selected_table}' DataFrame: \n")
    print(cleaned_user_df, "\n")

    os.makedirs(cleaned_csv_folder_path, exist_ok=True)  # Ensure that the folder exists, create it if it doesn't
    cleaned_csv_filename = os.path.join(cleaned_csv_folder_path, f"{selected_table}_data_cleaned.csv")  # Save the cleaned DataFrame as a CSV file in the specified folder
    cleaned_user_df.to_csv(cleaned_csv_filename, index=False)
    print(f"Saved cleaned '{selected_table}' DataFrame as '{cleaned_csv_filename}'.")

    api_connector.upload_to_db(cleaned_user_df, 'dim_users', engine2)  # Upload the cleaned data to the database

def two_etl_card_details():
    """
    The two_etl_card_details function extracts, transforms, and loads data for card details.
    It extracts the pdf data as a DataFrame.
    Then it cleans that DataFrame using the clean_card_data function from our data_cleaner module.
    It saves that cleaned DataFrame as a CSV file in our cleaned CSVs folder.
    Finally, it uploads that cleaned DataFrame to pgAdmin 4 using SQLAlchemy.   
    """
    s3_card_details = cred_config_api['s3_card_details'] # access the .yaml key
    date_details_df, table_name, raw_csv_filename = data_extractor.retrieve_pdf_data(pdf_path = s3_card_details, 
                                                                                     raw_csv_folder_path = raw_csv_folder_path, 
                                                                                     raw_notebook_folder_path = raw_notebook_folder_path 
                                                                                     )  # Retrieve PDF from AWS S3 bucket and convert to CSV
    print(f"'{table_name}', shall be extracted.\n")
    print(date_details_df, "\n")  # Display the DataFrame

    cleaned_date_df = data_cleaner.clean_card_data(date_details_df)
    print(f"Cleaned '{table_name}' DataFrame:\n")
    print(cleaned_date_df, "\n")

    os.makedirs(cleaned_csv_folder_path, exist_ok=True)  # Ensure that the folder exists, create it if it doesn't
    cleaned_csv_filename = os.path.join(cleaned_csv_folder_path, f"{table_name}_data_cleaned.csv")  # Save the cleaned DataFrame as a CSV file in the specified folder
    cleaned_date_df.to_csv(cleaned_csv_filename, index=False)
    print(f"Saved cleaned '{table_name}' DataFrame as '{cleaned_csv_filename}'.\n")

    api_connector.upload_to_db(cleaned_date_df, 'dim_card_details', engine2)  # Upload the cleaned data to the database

def three_etl_store_details():
    """
    The three_etl_store_details function extracts, transforms, and loads data for store details.
    It extracts the data via an API as a DataFrame.
    Then it cleans that DataFrame using the called_clean_store_data function from our data_cleaner module.
    It saves that cleaned DataFrame as a CSV file in our cleaned CSVs folder.
    Finally, it uploads that cleaned DataFrame to pgAdmin 4 using SQLAlchemy.   
    """
    x_api_key = cred_config_api['api_key'] # access the .yaml key
    headers = {'x-api-key': x_api_key}
    number_of_stores_endpoint = cred_config_api['number_of_stores_endpoint']
    retrieve_a_store_endpoint = cred_config_api['retrieve_a_store_endpoint']
    number_of_stores = data_extractor.list_number_of_stores(number_of_stores_endpoint, headers)  # retrieve the number of stores
    print(f"The number of stores to retrieve data from: {number_of_stores}")
    stores_df, table_name, csv_filename = data_extractor.retrieve_stores_data(retrieve_a_store_endpoint, 
                                                                              headers, 
                                                                              number_of_stores,
                                                                              raw_csv_folder_path,
                                                                              raw_notebook_folder_path
                                                                              )  # retrieve data for all stores and save in a Pandas df
    if stores_df is not None:
        print(f"'{table_name}', shall be extracted.\n")
        print(stores_df, "\n")
    else:
        print("Failed to retrieve stores data.")

    cleaned_store_df = data_cleaner.called_clean_store_data(stores_df)
    print(f"Cleaned '{table_name}' DataFrame: \n")
    print(cleaned_store_df, "\n")

    os.makedirs(cleaned_csv_folder_path, exist_ok=True)  # Ensure that the folder exists, create it if it doesn't
    cleaned_csv_filename = os.path.join(cleaned_csv_folder_path, f"{table_name}_data_cleaned.csv")  # Save the cleaned DataFrame as a CSV file in the specified folder
    cleaned_store_df.to_csv(cleaned_csv_filename, index=False)
    print(f"Saved cleaned '{table_name}' DataFrame as '{cleaned_csv_filename}'.\n")

    api_connector.upload_to_db(cleaned_store_df, 'dim_store_details', engine2)  # Upload the cleaned data to the database

def four_etl_product_details():
    """
    The four_etl_product_details function extracts, transforms, and loads data for product details.
    It extracts the data from the S3 address as a DataFrame.
    Then it cleans that DataFrame using the clean_products_data function from our data_cleaner module.
    It saves that cleaned DataFrame as a CSV file in our cleaned CSVs folder. 
    Finally, it uploads that cleaned DataFrame to pgAdmin 4 using SQLAlchemy.   
    """
    s3_address_products = cred_config_api['s3_address_products'] # access the .yaml key
    local_csv_file_path_products = cred_config_api['local_csv_file_path_products'] # specifies the desired local path to save the file
    local_ipynb_file_path_products = cred_config_api['local_ipynb_file_path_products'] 
    products_df, table_name, csv_filename = data_extractor.extract_from_s3(s3_address = s3_address_products, 
                                                                          csv_path = local_csv_file_path_products, 
                                                                          ipynb_path = local_ipynb_file_path_products,
                                                                          raw_notebook_folder_path = raw_notebook_folder_path
                                                                          )
    if products_df is not None:
        print(f"'{table_name}', shall be extracted.\n")
        print(products_df, "\n")
    else:
        print("Failed to retrieve products data.")

    products_df_filtered = data_cleaner.clean_products_data(products_df)
    cleaned_products_data = data_cleaner.convert_product_weights(products_df_filtered)
    print(f"Cleaned '{table_name}' DataFrame:\n")
    print(cleaned_products_data, "\n")

    os.makedirs(cleaned_csv_folder_path, exist_ok=True)  # Ensure that the folder exists, create it if it doesn't
    cleaned_csv_filename = os.path.join(cleaned_csv_folder_path, f"{table_name}_data_cleaned.csv")  # Save the cleaned DataFrame as a CSV file in the specified folder
    cleaned_products_data.to_csv(cleaned_csv_filename, index=True)
    print(f"Saved cleaned '{table_name}' DataFrame as '{cleaned_csv_filename}'.\n")

    api_connector.upload_to_db(cleaned_products_data, 'dim_products', engine2)  # Upload the cleaned data to the database

def five_etl_orders_details():
    """
    The five_etl_orders_details function extracts, transforms, and loads data for orders details.
    It first sets up the database connection and extracts the specified table's data as a DataFrame.
    Then it cleans that DataFrame using the clean_orders_data function from the data_cleaner module.
    Next it saves that cleaned DataFrame as a CSV file in a specified folder on disk (the 'cleaned' subfolder).
    Finally, it uploads that cleaned DataFrame to pgAdmin 4 using SQLAlchemy.   
    """
    selected_table_df, selected_table, engine2 = setup_and_extract_data(cred_path = cred_path, table_index = 3)
    cleaned_user_df = data_cleaner.clean_orders_data(selected_table_df)  # Clean the selected table DataFrame
    print(f"Cleaned '{selected_table}' DataFrame: \n")
    print(cleaned_user_df, "\n")

    os.makedirs(cleaned_csv_folder_path, exist_ok=True)  # Ensure that the folder exists, create it if it doesn't
    cleaned_csv_filename = os.path.join(cleaned_csv_folder_path, f"{selected_table}_data_cleaned.csv")  # Save the cleaned DataFrame as a CSV file in the specified folder
    cleaned_user_df.to_csv(cleaned_csv_filename, index=True)
    print(f"Saved cleaned '{selected_table}' DataFrame as '{cleaned_csv_filename}'.\n")

    api_connector.upload_to_db(cleaned_user_df, 'orders_table', engine2)  # Upload the cleaned data to the database

def six_etl_date_events():
    """
    The six_etl_date_events function extracts, transforms, and loads data for date events.
    It extracts the data from a JSON file as a DataFrame.
    Then it cleans that DataFrame using the clean_date_data function from our data_cleaner module.
    It saves that cleaned DataFrame as a CSV file in our cleaned CSVs folder. 
    Finally, it uploads that cleaned DataFrame to pgAdmin 4 using SQLAlchemy.  
    """
    s3_address_date_events = cred_config_api['s3_address_date_events'] # access the .yaml key
    date_details_df, table_name, raw_csv_filename = data_extractor.retrieve_json_data(json_path = s3_address_date_events, 
                                                                                      raw_notebook_folder_path = raw_notebook_folder_path,
                                                                                      raw_csv_folder_path = raw_csv_folder_path
                                                                                      )  # Retrieve JSON data from the AWS S3 bucket and convert it to CSV format
    date_details_df_filtered = data_cleaner.clean_date_data(date_details_df)  # Clean the date events DataFrame
    print(f"Cleaned '{table_name}' DataFrame:\n")  # Display the cleaned DataFrame
    print(date_details_df_filtered, "\n")

    os.makedirs(cleaned_csv_folder_path, exist_ok=True)  # Ensure that the folder exists, create it if it doesn't
    cleaned_csv_filename = os.path.join(cleaned_csv_folder_path, f"{table_name}_data_cleaned.csv")  # Save the cleaned DataFrame as a CSV file in the specified folder
    date_details_df_filtered.to_csv(cleaned_csv_filename, index=False)
    print(f"Saved cleaned '{table_name}' DataFrame as '{cleaned_csv_filename}'.\n")

    api_connector.upload_to_db(date_details_df_filtered, 'dim_date_times', engine2)  # Upload the cleaned data to the database

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
    
if __name__ == "__main__":
    print("######################################## 1. ETL of Legacy Users ########################################")
    one_etl_leagacy_users()

    print("######################################## 2. ETL of Card Details ########################################")
    two_etl_card_details()

    print("######################################## 3. ETL of Store Details ########################################")
    three_etl_store_details()

    print("######################################## 4. ETL of Product Details ########################################")
    four_etl_product_details()

    print("######################################## 5. ETL of Orders Details ########################################")
    five_etl_orders_details()

    print("######################################## 6. ETL of Date Events ########################################")
    six_etl_date_events()


