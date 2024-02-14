from _06_multinational_retail_data_centralisation.database_utils import DatabaseConnector
from sqlalchemy import inspect
# from urllib.parse import urlparse

import pandas as pd
import tabula # read tables in a PDF
import nbformat # save as .ipynb
import requests
import json
import boto3
import os # to create directories


class DataExtractor:
    """
    A utility class for extracting data from various sources.
    """
    @staticmethod
    def read_rds_table(table_name: str, engine):
        """
        The read_rds_table function reads data from an RDS table into a pandas DataFrame.

        Args:
            table_name (str): Name of the table to read.
            engine: Database engine object.

        Returns:
            pd.DataFrame: DataFrame containing the table data.
        """
        df = pd.read_sql_table(table_name, engine)
        return df
    
    @staticmethod
    def list_db_tables(engine):
        """
        The list_db_tables function lists all tables in the database.

        Args:
            engine: Database engine object.

        Returns:
            list: List of table names.
        """
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return tables
    
    @staticmethod
    def retrieve_pdf_data(pdf_path: str, raw_csv_folder_path: str, raw_notebook_folder_path: str):
        """
        The retrieve_pdf_data function retrieves data from a PDF file.

        Args:
            pdf_path (str): Path to the PDF file.
            raw_csv_folder_path (str): Path to the folder where CSV files will be saved.
            raw_notebook_folder_path (str): Path to the folder where notebook files will be saved.

        Returns:
            tuple: DataFrame containing PDF data, table name and path to the CSV file.
        """
        date_details_df = tabula.read_pdf(pdf_path, pages='all')  # Extract data from the PDF
        date_details_df = pd.concat(date_details_df)
        print("Extracted PDF document from an AWS S3 bucket:\n")

        os.makedirs(raw_csv_folder_path, exist_ok=True)  # Ensure that the folder exists, create it if it doesn't

        table_name = "card_details"  # Save the DataFrame as a CSV file in the specified folder
        raw_csv_filename = os.path.join(raw_csv_folder_path, f"{table_name}.csv")
        date_details_df.to_csv(raw_csv_filename, index=False)
        print(f"Saved '{table_name}' as '{raw_csv_filename}'.\n")

        os.makedirs(raw_notebook_folder_path, exist_ok=True)  # Ensure that the folder exists, create it if it doesn't

        notebook = nbformat.v4.new_notebook()  # Create a new notebook
        code_cell = nbformat.v4.new_code_cell(f"import pandas as pd\n\n"  # Add a code cell for the table to the notebook
                                            f"# Import data from '{raw_csv_filename}' into DataFrame.\n"
                                            f"table_name = '{table_name}'\n"
                                            f"csv_file_path = '..\{raw_csv_filename}'\n"
                                            f"{table_name}_df = pd.read_csv(csv_file_path)\n"
                                            f"# Display the DataFrame\n"
                                            f"display({table_name}_df)")
        notebook.cells.append(code_cell)

        raw_notebook_filename = os.path.join(raw_notebook_folder_path, f"{table_name}.ipynb")  # Save the notebook to a .ipynb file with a name based on the fixed extracted table
        with open(raw_notebook_filename, 'w') as nb_file:
            nbformat.write(notebook, nb_file)
            print(f"Saved '{table_name}' as '{raw_notebook_filename}'.\n")

        return date_details_df, table_name, raw_csv_filename
    
    @staticmethod
    def list_number_of_stores(number_of_stores_endpoint: str, headers: dict):
        """
        The list_number_of_stores function sends a GET request to the API endpoint and returns the number of stores in the database.
 
        Args:
            number_of_stores_endpoint (str): URL of the API endpoint.
            headers (dict): Headers to be included in the request.

        Returns:
            int: Number of stores.
        """
        try:
            response = requests.get(number_of_stores_endpoint, headers=headers)  # Send GET request to the API
            if response.status_code == 200:  # Check if the request was successful (status code 200)
                data = response.json()  # Extract and return the number of stores from the response JSON
                return data['number_stores']
            else:
                print(f"Request failed with status code: {response.status_code}")  # If the request was not successful, print the status code and response text
                print(f"Response Text: {response.text}")
                return None
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None
    
    @staticmethod
    def retrieve_stores_data(retrieve_a_store_endpoint: str, 
                             headers: dict, 
                             number_of_stores: int, 
                             raw_csv_folder_path: str,
                             raw_notebook_folder_path: str
                             ):
        """
        The retrieve_stores_data function retrieves data for multiple stores from an API endpoint.

        Args:
            retrieve_a_store_endpoint (str): URL pattern for retrieving store data.
            headers (dict): Headers to be included in the request.
            number_of_stores (int): Number of stores to retrieve data for.
            raw_csv_folder_path (str): Path to the folder where CSV files will be saved.
            raw_notebook_folder_path (str): Path to the folder where notebook files will be saved.

        Returns:
            tuple: DataFrame containing store data, table name and path to the CSV file.
        """
        if number_of_stores is None:
            print("Failed to retrieve the number of stores.")
            return None

        try:
            all_stores_data = []  # Initialise an empty list to store data
            
            for store_number in range(0, number_of_stores):  # Iterate through store numbers and retrieve data for each store
                endpoint = retrieve_a_store_endpoint.format(store_number=store_number)   # Format the endpoint with the specified store number
                response = requests.get(endpoint, headers=headers) # Send GET request to the API

                if response.status_code == 200:  # Check if the request was successful (status code 200)
                    store_data = response.json()# Extract store data from the response JSON
                    all_stores_data.append(store_data)
                else:
                    print(f"Request for store {store_number} failed with status code: {response.status_code}")  # If the request was not successful, print the status code and response text
                    print(f"Response Text: {response.text}")

            stores_df = pd.DataFrame(all_stores_data)  # Convert the list of store data into a Pandas DataFrame
            
            os.makedirs(raw_csv_folder_path, exist_ok=True)  # Ensure that the folder exists, create it if it doesn't
            table_name = "store_details"  # Save the DataFrame as a CSV file in the specified folder
            raw_csv_filename = os.path.join(raw_csv_folder_path, f"{table_name}.csv")
            stores_df.to_csv(raw_csv_filename, index=False)
            print(f"Saved '{table_name}' as '{raw_csv_filename}'.\n")

            os.makedirs(raw_notebook_folder_path, exist_ok=True) # Ensure that the folder exists, create it if it doesn't
            notebook = nbformat.v4.new_notebook()  # Create a new notebook
            code_cell = nbformat.v4.new_code_cell(f"import pandas as pd\n"  # Add a code cell for the table to the notebook
                                                f"# Import data from '{raw_csv_filename}' into DataFrame.\n"
                                                f"table_name = '{table_name}'\n"
                                                f"csv_file_path = '..\{raw_csv_filename}'\n"
                                                f"{table_name}_df = pd.read_csv(csv_file_path)\n"
                                                f"# Display the DataFrame\n"
                                                f"display({table_name}_df)"
                                                )
            notebook.cells.append(code_cell)

            raw_notebook_filename = os.path.join(raw_notebook_folder_path, f"{table_name}.ipynb")  # Save the notebook to a .ipynb file with a name based on the fixed extracted table
            with open(raw_notebook_filename, 'w') as nb_file:
                nbformat.write(notebook, nb_file)
                print(f"Saved '{table_name}' as '{raw_notebook_filename}'.\n")

            return stores_df, table_name, raw_csv_filename

        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    @staticmethod
    def extract_from_s3(s3_address: str, 
                        csv_path: str, 
                        ipynb_path: str, 
                        raw_notebook_folder_path: str
                        ):
        """
        The extract_from_s3 function extracts data from an S3 bucket and saves it as CSV and IPython Notebook files.
        
        Args:
            s3_address (str): Address of the file in the S3 bucket.
            csv_path (str): Path where the CSV file will be saved.
            ipynb_path (str): Path where the IPython Notebook file will be saved.
            raw_notebook_folder_path (str): Path where the IPython Notebook file will be saved.

        Returns:
            tuple: DataFrame containing the extracted data, table name and path to the CSV file.
        """
        try:
            s3 = boto3.client('s3')  # Create S3 client
            bucket_name, object_key = s3_address.replace('s3://', '').split('/', 1) # Extract bucket name and object key from S3 address
            s3.download_file(bucket_name, object_key, csv_path)  # Download the file from S3 to the local machine as a .csv and .ipynb
            table_name = object_key.replace('products.csv', 'products_details')
            raw_csv_filename = f"{table_name}.csv"
            print(f"Saved '{table_name}' as '{raw_csv_filename}'.")

            products_df = pd.read_csv(csv_path, index_col=0)  # Read the .csv file into a Pandas DataFrame
            print(f"'{table_name}', shall be extracted: \n")
            print(products_df, "\n")
       
            os.makedirs(raw_notebook_folder_path, exist_ok=True)  # Ensure that the folder exists, create it if it doesn't
            notebook = nbformat.v4.new_notebook()  # Create a new notebook
            code_cell = nbformat.v4.new_code_cell(f"import pandas as pd\n"  # Add a code cell for the table to the notebook
                                                    f"# Import data from '{raw_csv_filename}' into DataFrame.\n\n"
                                                    f"table_name = '{table_name}'\n"
                                                    f"csv_file_path = '..\_01_raw_tables_csv\products_details.csv'\n"
                                                    f"{table_name}_df = pd.read_csv(csv_file_path, index_col=0)\n"
                                                    f"# Display the DataFrame\n"
                                                    f"display({table_name}_df)"
                                                    )
            notebook.cells.append(code_cell)

            raw_notebook_filename = os.path.join(raw_notebook_folder_path, f"{table_name}.ipynb")  # Save the notebook to a .ipynb file with a name based on the fixed extracted table
            with open(raw_notebook_filename, 'w') as nb_file:
                nbformat.write(notebook, nb_file)
                print(f"Saved '{table_name}' as '{raw_notebook_filename}'.\n")

            return products_df, table_name, raw_csv_filename

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    @staticmethod
    def retrieve_json_data(json_path: str,
                           raw_csv_folder_path: str,
                           raw_notebook_folder_path: str
                           ):
        """
        The retrieve_json_data function retrieves JSON data from a file and saves it as a CSV file and IPython Notebook.
        
        Args:
            json_path (str): Path to the JSON file.
            raw_csv_folder_path (str): Path where the CSV file will be saved.
            raw_notebook_folder_path (str): Path where the IPython Notebook file will be saved.

        Returns:
            tuple: DataFrame containing the extracted data, table name and path to the CSV file.
        """
        try:
            date_details_df = pd.read_json(json_path)
            print("Extracted JSON document from an AWS S3 bucket:\n")
            
            os.makedirs(raw_csv_folder_path, exist_ok=True)  # Ensure that the folder exists, create it if it doesn't

            
            table_name = "date_details"  # Save the DataFrame as a CSV file in the specified folder
            csv_filename = f"{table_name}.csv"
            raw_csv_filename = os.path.join(raw_csv_folder_path, csv_filename)
            date_details_df.to_csv(raw_csv_filename, index=True)
            print(f"Saved '{table_name}' as '{raw_csv_filename}'.\n")
            print(f"'{table_name}', shall be extracted:\n")
            print(date_details_df, "\n")  # Display the DataFrame

            notebook = nbformat.v4.new_notebook()  # Create a new notebook
            code_cell = nbformat.v4.new_code_cell(f"import pandas as pd\n\n"  # Add a code cell for the table to the notebook
                                                f"# Import data from '{raw_csv_filename}' into DataFrame.\n"
                                                f"table_name = '{table_name}'\n"
                                                f"csv_file_path = '..\{raw_csv_filename}'\n"
                                                f"{table_name}_df = pd.read_csv(csv_file_path, index_col=0)\n"
                                                f"# Display the DataFrame\n"
                                                f"display({table_name}_df)")

            notebook.cells.append(code_cell)

            os.makedirs(raw_notebook_folder_path, exist_ok=True)  # Ensure that the folder exists, create it if it doesn't
            notebook_file = f"{table_name}.ipynb"
            raw_notebook_filename = os.path.join(raw_notebook_folder_path, notebook_file)
            with open(raw_notebook_filename, 'w') as nb_file:
                nbformat.write(notebook, nb_file)
                print(f"Saved '{table_name}' as '{raw_notebook_filename}'.\n")

            return date_details_df, table_name, raw_csv_filename

        except Exception as e:
            print(f"An error occurred: {e}")
            return None