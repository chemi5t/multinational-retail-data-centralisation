from database_utils import DatabaseConnector
from sqlalchemy import inspect
import pandas as pd
import tabula # read tables in a PDF
import nbformat # save as .ipynb

import requests
import json

class DataExtractor:

    @staticmethod
    def read_rds_table(table_name, engine):
        df = pd.read_sql_table(table_name, engine)
        return df
    
    @staticmethod
    def list_db_tables(engine):
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return tables
    
    @staticmethod
    def retrieve_pdf_data(pdf_path = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"):
        card_details_df = tabula.read_pdf(pdf_path, pages='all')
        card_details_df = pd.concat(card_details_df)
        print("\nExtracted PDF document from an AWS S3 bucket: ")

        # Save the DataFrame as a CSV file
        table_name = "card_details"
        csv_filename = f"{table_name}.csv"
        card_details_df.to_csv(csv_filename, index=False)
        print(f"Saved 'card details' as {csv_filename}")

        # Create a new notebook
        notebook = nbformat.v4.new_notebook()
        # Add a code cell for the table to the notebook
        code_cell = nbformat.v4.new_code_cell(f"import pandas as pd\n"
                                            f"# Import data from '{csv_filename}' into DataFrame.\n"
                                            f"table_name = '{table_name}'\n"
                                            f"csv_file_path = '{table_name}.csv'\n"
                                            f"{table_name}_df = pd.read_csv(csv_file_path)\n"
                                            f"# Display the DataFrame\n"
                                            f"display({table_name}_df)")

        notebook.cells.append(code_cell)

        # Save the notebook to a .ipynb file with a name based on the fixed extracted table
        notebook_file = f"{table_name}.ipynb"
        with open(notebook_file, 'w') as nb_file:
            nbformat.write(notebook, nb_file)
            print(f"Saved {table_name} DataFrame as {notebook_file}\n")
        
        return card_details_df, table_name, csv_filename
    
    @staticmethod
    def list_number_of_stores(number_of_stores_endpoint, headers):
        
        try:
            # Send GET request to the API
            response = requests.get(number_of_stores_endpoint, headers=headers)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Extract and return the number of stores from the response JSON
                data = response.json()
                return data['number_stores']
            else:
                # If the request was not successful, print the status code and response text
                print(f"Request failed with status code: {response.status_code}")
                print(f"Response Text: {response.text}")
                return None

        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None
    
    @staticmethod
    def retrieve_stores_data(retrieve_a_store_endpoint, headers, number_of_stores):
        if number_of_stores is None:
            print("Failed to retrieve the number of stores.")
            return None

        try:
            # Initialize an empty list to store data
            all_stores_data = []

            # Iterate through store numbers and retrieve data for each store
            for store_number in range(0, number_of_stores):
                # Format the endpoint with the specified store number
                endpoint = retrieve_a_store_endpoint.format(store_number=store_number)

                # Send GET request to the API
                response = requests.get(endpoint, headers=headers)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Extract store data from the response JSON
                    store_data = response.json()
                    all_stores_data.append(store_data)
                else:
                    # If the request was not successful, print the status code and response text
                    print(f"Request for store {store_number} failed with status code: {response.status_code}")
                    print(f"Response Text: {response.text}")

            # Convert the list of store data into a Pandas DataFrame
            stores_df = pd.DataFrame(all_stores_data)

            return stores_df

        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None