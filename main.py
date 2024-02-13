import nbformat # save as .ipynb
import pandas as pd
import yaml # to read .yaml. Help with read_db
import os # to create directories

from _06_multinational_retail_data_centralisation.data_cleaning import DataCleaning as dcl
from _06_multinational_retail_data_centralisation.data_extraction import DataExtractor as dex
from _06_multinational_retail_data_centralisation.database_utils import DatabaseConnector as dc
from decouple import config #  calling sensitive information

def setup_and_extract_data(file_path='db_creds.yaml', table_index = 2): # Step 1: Specify the correct file path
    database_connector = dc()
    credentials = database_connector.read_db_creds(file_path)    # Step 2: Read credentials
    engine, engine2 = database_connector.init_db_engine(credentials)      # Step 3: Initialise database engine
    data_extractor = dex()

    # Step 4: List all tables in the database
    tables = data_extractor.list_db_tables(engine)
    
    # Display the list of tables to the user
    # Available Tables: ['legacy_store_details', 'legacy_users', 'orders_table']  i.e. table 1, 2, 3 respectively (indices 0, 1, 2 respectively)
    print("Available Tables: \n")
    for i, table_name in enumerate(tables, 1):
        print(f"{i}. {table_name}")

    # Get user input for table selection
    table_index # <---------------- comment this out 
    selected_index = table_index - 1
    selected_table = tables[selected_index]
    print(f"Table {table_index}. '{selected_table}', shall be extracted. \n")

    # Step 5: Read the selected table into a pandas DataFrame
    selected_table_df = data_extractor.read_rds_table(selected_table, engine)

    # Display the DataFrame
    print(selected_table_df, "\n")

    # Define the folder path where you want to save the CSV files
    raw_csv_folder_path = '_01_raw_tables_csv'
    # Ensure that the folder exists, create it if it doesn't
    os.makedirs(raw_csv_folder_path, exist_ok=True)

    # Save the DataFrame as a CSV file in the specified folder
    raw_csv_filename = os.path.join(raw_csv_folder_path, f"{selected_table}.csv")

    selected_table_df.to_csv(raw_csv_filename, index=True)
    print(f"Saved {selected_table} DataFrame as {raw_csv_filename}. \n")

    # Define the folder path where you want to save the notebooks
    raw_notebook_folder_path = '_02_manipulate_raw_tables_ipynb'
    # Ensure that the folder exists, create it if it doesn't
    os.makedirs(raw_notebook_folder_path, exist_ok=True)

    # Create a new notebook
    notebook = nbformat.v4.new_notebook()
    # Add a code cell for the table to the notebook
    code_cell = nbformat.v4.new_code_cell( f"import pandas as pd\n"
                                            f"from _06_multinational_retail_data_centralisation.database_utils import DatabaseConnector as dc\n\n"
                                            f"database_connector = dc()\n"
                                            f"credentials = database_connector.read_db_creds('{file_path}')\n"
                                            f"engine, _ = database_connector.init_db_engine(credentials)\n"
                                            f"# Import data from '{selected_table}' table into DataFrame\n"
                                            f"{selected_table}_df = pd.read_sql('{selected_table}', engine)\n"
                                            f"# Display the DataFrame\n"
                                            f"{selected_table}_df")
                                            
    notebook.cells.append(code_cell)

    # Save the notebook to a .ipynb file in the specified folder
    raw_notebook_filename = os.path.join(raw_notebook_folder_path, f"{selected_table}.ipynb")
    with open(raw_notebook_filename, 'w') as nb_file:
        nbformat.write(notebook, nb_file)
        print(f"Saved {selected_table} DataFrame as {raw_notebook_filename}.\n")

    return selected_table_df, selected_table, engine2


# def save_dataframe(date_details_df): # Step 1: Specify the correct file path

#     # Save the DataFrame as a CSV file
#     csv_filename = f"{selected_table}_data.csv"
#     selected_table_df.to_csv(csv_filename)
#     print(f"Saved {selected_table} DataFrame as {csv_filename}")

#     # Create a new notebook
#     notebook = nbformat.v4.new_notebook()
#     # Add a code cell for the table to the notebook
#     code_cell = nbformat.v4.new_code_cell(f"import pandas as pd\n"
#                                             f"from database_utils import DatabaseConnector as dc\n\n"
#                                             f"database_connector = dc()\n"
#                                             f"credentials = database_connector.read_db_creds('{file_path}')\n"
#                                             f"engine = database_connector.init_db_engine(credentials)\n\n"
#                                             f"# Import data from '{selected_table}' table into DataFrame\n"
#                                             f"{selected_table}_df = pd.read_sql('{selected_table}', engine)\n\n"
#                                             f"# Display the DataFrame\n"
#                                             f"{selected_table}_df")
                                            
#     notebook.cells.append(code_cell)


if __name__ == "__main__":

    print("######################################## 1. leagacy_users ########################################")

    selected_table_df, selected_table, engine2 = setup_and_extract_data(table_index = 2)

    # Clean the selected table DataFrame
    data_cleaner = dcl()

    cleaned_user_df = data_cleaner.clean_user_data(selected_table_df)

    print(f"Cleaned '{selected_table}' DataFrame: \n")
    print(cleaned_user_df, "\n")

    # Define the folder path where you want to save the cleaned CSV files
    cleaned_csv_folder_path = '_03_cleaned_tables_csv'
    # Ensure that the folder exists, create it if it doesn't
    os.makedirs(cleaned_csv_folder_path, exist_ok=True)

    # Save the cleaned DataFrame as a CSV file in the specified folder
    cleaned_csv_filename = os.path.join(cleaned_csv_folder_path, f"{selected_table}_data_cleaned.csv")
    cleaned_user_df.to_csv(cleaned_csv_filename, index=False)
    print(f"Saved cleaned '{selected_table}' DataFrame as '{cleaned_csv_filename}'.")

    # Upload the cleaned data to the database
    api_connector = dc()
    api_connector.upload_to_db(cleaned_user_df, 'dim_users', engine2)

    print("######################################## 2. card_details ########################################")
    # to gain access to private credentials for API
    cred_access = config('credentials_env') # refers to .yaml file ## from decouple import config
    cred_api = api_connector.read_db_creds(file_path = cred_access) # extracts the .yaml file

    s3_card_details = cred_api['s3_card_details'] # access the .yaml key

    # Retrieve PDF from AWS S3 bucket and convert to CSV
    api_extractor = dex() 

    date_details_df, table_name, csv_filename = api_extractor.retrieve_pdf_data(pdf_path = s3_card_details)
    print(f"'{table_name}', shall be extracted. \n")

    # Display the DataFrame
    print(date_details_df, "\n")

    cleaned_date_df = data_cleaner.clean_card_data(date_details_df)

    print(f"Cleaned '{table_name}' DataFrame: \n")
    print(cleaned_date_df, "\n")

    # Define the folder path where you want to save the cleaned CSV files
    cleaned_csv_folder_path = '_03_cleaned_tables_csv'
    # Ensure that the folder exists, create it if it doesn't
    os.makedirs(cleaned_csv_folder_path, exist_ok=True)

    # Save the cleaned DataFrame as a CSV file in the specified folder
    cleaned_csv_filename = os.path.join(cleaned_csv_folder_path, f"{table_name}_data_cleaned.csv")
    cleaned_date_df.to_csv(cleaned_csv_filename, index=False)
    print(f"Saved cleaned '{table_name}' DataFrame as '{cleaned_csv_filename}'.")

    # Upload the cleaned data to the database
    api_connector.upload_to_db(cleaned_date_df, 'dim_card_details', engine2)

    print("######################################## 3. store_details ########################################")
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
        print(f"'{table_name}', shall be extracted.\n")
        print(stores_df, "\n")
    else:
        print("Failed to retrieve stores data.")

    cleaned_store_df = data_cleaner.called_clean_store_data(stores_df)

    print(f"Cleaned '{table_name}' DataFrame: \n")
    print(cleaned_store_df, "\n")

    # Save the cleaned DataFrame as a CSV file in the specified folder
    cleaned_csv_filename = os.path.join(cleaned_csv_folder_path, f"{table_name}_data_cleaned.csv")
    cleaned_store_df.to_csv(cleaned_csv_filename, index=False)
    print(f"Saved cleaned '{table_name}' DataFrame as '{cleaned_csv_filename}'.\n")

    # Upload the cleaned data to the database
    api_connector.upload_to_db(cleaned_store_df, 'dim_store_details', engine2)


    print("######################################## 4. product_details ########################################")

    s3_address_products = cred_api['s3_address_products'] # access the .yaml key
    local_csv_file_path_products = cred_api['local_csv_file_path_products'] # specifies the desired local path to save the file
    local_ipynb_file_path_products = cred_api['local_ipynb_file_path_products'] 

    products_df, table_name, csv_filename = api_extractor.extract_from_s3(s3_address = s3_address_products, 
                                                                          csv_path = local_csv_file_path_products, 
                                                                          ipynb_path = local_ipynb_file_path_products
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

    # Save the cleaned DataFrame as a CSV file in the specified folder
    cleaned_csv_filename = os.path.join(cleaned_csv_folder_path, f"{table_name}_data_cleaned.csv")
    cleaned_products_data.to_csv(cleaned_csv_filename, index=True)
    print(f"Saved cleaned '{table_name}' DataFrame as '{cleaned_csv_filename}'.\n")

    # Upload the cleaned data to the database
    api_connector.upload_to_db(cleaned_products_data, 'dim_products', engine2)

    print("######################################## 5. orders_details ########################################")

    selected_table_df, selected_table, engine2 = setup_and_extract_data(table_index = 3)

    # Clean the selected table DataFrame
    data_cleaner = dcl() 

    cleaned_user_df = data_cleaner.clean_orders_data(selected_table_df)

    print(f"Cleaned '{selected_table}' DataFrame: \n")
    print(cleaned_user_df, "\n")

    
    # Define the folder path where you want to save the cleaned CSV files
    cleaned_csv_folder_path = '_03_cleaned_tables_csv'
    # Ensure that the folder exists, create it if it doesn't
    os.makedirs(cleaned_csv_folder_path, exist_ok=True)

    # Save the cleaned DataFrame as a CSV file in the specified folder
    cleaned_csv_filename = os.path.join(cleaned_csv_folder_path, f"{selected_table}_data_cleaned.csv")
    cleaned_user_df.to_csv(cleaned_csv_filename, index=True)
    print(f"Saved cleaned '{selected_table}' DataFrame as '{cleaned_csv_filename}'.")

    # Upload the cleaned data to the database
    api_connector = dc()
    api_connector.upload_to_db(cleaned_user_df, 'orders_table', engine2)

    print("######################################## 6. date_events ########################################")
    s3_address_date_events = cred_api['s3_address_date_events'] # access the .yaml key
    # Retrieve JSON data from the AWS S3 bucket and convert it to CSV format
    date_details_df, table_name, raw_csv_filename = api_extractor.retrieve_json_data(json_path = s3_address_date_events)

    # Clean the date events DataFrame
    date_details_df_filtered = data_cleaner.clean_date_data(date_details_df)

    # Display the cleaned DataFrame
    print(f"Cleaned '{table_name}' DataFrame:\n")
    print(date_details_df_filtered, "\n")

    # Define the folder path where you want to save the cleaned CSV files
    cleaned_csv_folder_path = '_03_cleaned_tables_csv'
    # Ensure that the folder exists, create it if it doesn't
    os.makedirs(cleaned_csv_folder_path, exist_ok=True)

    # Save the cleaned DataFrame as a CSV file in the specified folder
    raw_csv_filename = os.path.join(cleaned_csv_folder_path, f"{table_name}_data_cleaned.csv")
    date_details_df_filtered.to_csv(raw_csv_filename, index=False)
    print(f"Saved cleaned '{table_name}' DataFrame as '{raw_csv_filename}'.\n")

    # Upload the cleaned data to the database
    api_connector.upload_to_db(date_details_df_filtered, 'dim_date_times', engine2)



    # s3_address_date_events = cred_api['s3_address_date_events'] # access the .yaml key
    # local_file_path_date_details = cred_api['local_file_path_date_details'] # specifies the desired local path to save the file
    # products_df, table_name, csv_filename = api_extractor.extract_from_s3(s3_address = s3_address_date_events, local_file_path = local_file_path_date_details)

                    # if products_df is not None:
                    #     print(f"'{table_name}', shall be extracted. \n")
                    #     print(products_df, "\n")
                    # else:
                    #     print("Failed to retrieve products data.")

    # products_df_filtered = data_cleaner.clean_products_data(products_df)

    # cleaned_products_data = data_cleaner.convert_product_weights(products_df_filtered)

    # print(f"Cleaned '{table_name}' DataFrame: \n")
    # print(cleaned_products_data, "\n")
    
    # # Save the cleaned DataFrame as a CSV file
    # cleaned_csv_filename = f"{table_name}_data_cleaned.csv"
    # cleaned_products_data.to_csv(cleaned_csv_filename, index=True)
    # print(f"Saved cleaned '{table_name}' DataFrame as '{cleaned_csv_filename}'.")

    # # Upload the cleaned data to the database
    # api_connector.upload_to_db(cleaned_products_data, 'dim_products', engine2)