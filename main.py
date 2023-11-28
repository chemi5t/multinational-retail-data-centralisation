from database_utils import DatabaseConnector as dc
from data_extraction import DataExtractor as dex
# from data_cleaning import DataCleaning as dcl
import pandas as pd


file_path = 'db_creds.yaml'                                  # Step 1: Specify the correct file path
database_connector = dc()
credentials = database_connector.read_db_creds(file_path)    # Step 2: Read credentials
engine = database_connector.init_db_engine(credentials)      # Step 3: Initialise database engine

data_extractor = dex()

tables = data_extractor.list_db_tables(engine)               # Step 4: List all tables in the database
print("Available Tables: ", tables)                          # Available Tables: ['legacy_store_details', 'legacy_users', 'orders_table']

def extract_data_into_csv(tables):
    for table_name in tables:
        df = data_extractor.read_rds_table(table_name, engine)   # Step 5: Extract tables containing user data and return pandas DataFrames
        # print(f"{table_name} DataFrame:")
        # print(df)
        df.to_csv(f'{table_name}.csv')

pulling_data = extract_data_into_csv(tables)