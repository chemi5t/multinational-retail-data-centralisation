from database_utils import DatabaseConnector
from sqlalchemy import inspect
import pandas as pd

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
    

