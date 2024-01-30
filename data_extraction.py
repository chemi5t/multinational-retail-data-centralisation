from database_utils import DatabaseConnector
from sqlalchemy import inspect
import pandas as pd
import tabula # read tables in a PDF
import nbformat # save as .ipynb

import requests
import json
import boto3
from urllib.parse import urlparse


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
        date_details_df = tabula.read_pdf(pdf_path, pages='all')
        date_details_df = pd.concat(date_details_df)
        print("Extracted PDF document from an AWS S3 bucket: ")

        # Save the DataFrame as a CSV file
        table_name = "card_details"
        csv_filename = f"{table_name}.csv"
        date_details_df.to_csv(csv_filename, index=False)
        print(f"Saved '{table_name}' as '{csv_filename}'.")

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
            print(f"Saved '{table_name}' as '{notebook_file}'.\n")
        
        return date_details_df, table_name, csv_filename
    
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

            #############

            # Save the DataFrame as a CSV file
            table_name = "store_details"
            csv_filename = f"{table_name}.csv"
            stores_df.to_csv(csv_filename, index=False)
            print(f"Saved '{table_name}' as '{csv_filename}'.")

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
                print(f"Saved '{table_name}' as '{notebook_file}'.\n")
            
            return stores_df, table_name, csv_filename

        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
    # @staticmethod
    # def extract_from_s3(s3_address, local_file_path):
    #     try:
    #         # Create S3 client
    #         s3 = boto3.client('s3')

    #         # Extract bucket name and object key from S3 address
    #         if s3_address.startswith('s3://'):
    #             # Handle 's3://' format
    #             bucket_name, object_key = s3_address.replace('s3://', '').split('/', 1)
    #         elif s3_address.startswith('https://'):
    #             # Handle 'https://' format
    #             parsed_url = urlparse(s3_address)
    #             bucket_name = parsed_url.netloc.split('.')[0]
    #             object_key = parsed_url.path.lstrip('/')
    #         else:
    #             raise ValueError("Invalid S3 address format")

    #         # Download the file from S3 to the local machine
    #         s3.download_file(bucket_name, object_key, local_file_path)

    #         # Determine the table_name based on the file type
    #         if '.json' in object_key:
    #             table_name = object_key.replace('date_details.json', 'date_details')
    #         else:
    #             table_name = object_key.replace('products.csv', 'products_details')

    #         # Read the file into a Pandas DataFrame
    #         if '.json' in object_key:
    #             with open(local_file_path, 'r') as json_file:
    #                 data_df = pd.json_normalize(json.load(json_file))
    #         elif '.csv' in object_key:
    #             data_df = pd.read_csv(local_file_path, index_col=0)
    #         else:
    #             raise ValueError("Unsupported file type")

    #         # Display the DataFrame
    #         print(f"\nExtracted data from '{object_key}':\n")
    #         print(data_df)

    #                         # # Save the DataFrame as a CSV file
    #                         # csv_filename = f"{table_name}.csv"
    #                         # data_df.to_csv(csv_filename, index=False)
    #                         # print(f"\nSaved '{table_name}' as '{csv_filename}'.")

    #         # Save the DataFrame as a ipynb file

    #         if '.json' in object_key:
    #             # Create a new notebook
    #             notebook = nbformat.v4.new_notebook()
    #             # Add a code cell for the table to the notebook
    #             code_cell = nbformat.v4.new_code_cell(f"import pandas as pd\n"
    #                                                 f"import json\n"
    #                                                 f"# Import data from '{table_name}.json' into DataFrame.\n"
    #                                                 f"json_file_path = '{table_name}.json'\n"
    #                                                 f"{table_name}_df = pd.json_normalize(json.load(open(json_file_path)))\n"
    #                                                 f"# Display the DataFrame\n"
    #                                                 f"display({table_name}_df)")

    #             notebook.cells.append(code_cell)
    #         else:
    #                         # # Save the DataFrame as a CSV file
    #                         # csv_filename = f"{table_name}.csv"
    #                         # data_df.to_csv(csv_filename, index=False)
    #                         # print(f"\nSaved '{table_name}' as '{csv_filename}'.")

    #             # Create a new notebook
    #             notebook = nbformat.v4.new_notebook()
    #             # Add a code cell for the table to the notebook
    #             code_cell = nbformat.v4.new_code_cell(f"import pandas as pd\n"
    #                                                 f"# Import data from '{table_name}.csv' into DataFrame.\n"
    #                                                 f"csv_file_path = '{table_name}.csv'\n"
    #                                                 f"{table_name}_df = pd.read_csv(csv_file_path)\n"
    #                                                 f"# Display the DataFrame\n"
    #                                                 f"display({table_name}_df)")

    #             notebook.cells.append(code_cell)

    #         # Save the notebook to a .ipynb file with a name based on the fixed extracted table
    #         notebook_file = f"{table_name}.ipynb"
    #         with open(notebook_file, 'w') as nb_file:
    #             nbformat.write(notebook, nb_file)
    #             print(f"\nSaved '{table_name}' as '{notebook_file}'.\n")

    #         return data_df, table_name, local_file_path

    #     except FileNotFoundError as e:
    #         print(f"\nFile not found: {e}")
    #         return None
    #     except Exception as e:
    #         print(f"\nAn unexpected error occurred: {e}")
    #         return None


    @staticmethod
    def extract_from_s3(s3_address, local_file_path):
        try:
            # Create S3 client
            s3 = boto3.client('s3')

            # Extract bucket name and object key from S3 address
            bucket_name, object_key = s3_address.replace('s3://', '').split('/', 1)

            # Download the file from S3 to the local machine as a .csv and .ipynb
            s3.download_file(bucket_name, object_key, local_file_path)

            table_name = object_key.replace('products.csv', 'products_details')
            csv_filename = f"{table_name}.csv"
            print(f"Saved '{table_name}' as '{csv_filename}'.")

            # Read the .csv file into a Pandas DataFrame
            products_df = pd.read_csv(local_file_path, index_col=0)

            print(f"'{table_name}', shall be extracted: \n")
            print(products_df, "\n")

            # Create a new notebook
            notebook = nbformat.v4.new_notebook()
            # Add a code cell for the table to the notebook
            code_cell = nbformat.v4.new_code_cell(f"import pandas as pd\n"
                                                f"# Import data from '{csv_filename}' into DataFrame.\n"
                                                f"table_name = '{table_name}'\n"
                                                f"csv_file_path = '{table_name}.csv'\n"
                                                f"{table_name}_df = pd.read_csv(csv_file_path, index_col=0)\n"
                                                f"# Display the DataFrame\n"
                                                f"display({table_name}_df)")

            notebook.cells.append(code_cell)

            # Save the notebook to a .ipynb file with a name based on the fixed extracted table
            notebook_file = f"{table_name}.ipynb"
            with open(notebook_file, 'w') as nb_file:
                nbformat.write(notebook, nb_file)
                print(f"Saved '{table_name}' as '{notebook_file}'.\n")

            return products_df, table_name, csv_filename

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    @staticmethod
    def retrieve_json_data(json_path = "https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json"):
        date_details_df = pd.read_json(json_path)
        print("Extracted JSON document from an AWS S3 bucket: ")

        # Save the DataFrame as a CSV file
        table_name = "date_details"
        csv_filename = f"{table_name}.csv"
        date_details_df.to_csv(csv_filename, index=True)
        print(f"Saved '{table_name}' as '{csv_filename}'.")

        print(f"\n'{table_name}', shall be extracted: \n")

        # Display the DataFrame
        print(date_details_df, "\n")

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
            print(f"Saved '{table_name}' as '{notebook_file}'.\n")
        
        return date_details_df, table_name, csv_filename