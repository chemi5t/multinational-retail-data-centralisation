import yaml # to read .yaml. Help with read_db_creds
from sqlalchemy import create_engine # this ORM will transform the python objects into SQL tables

class DatabaseConnector:

    @staticmethod
    def read_db_creds(file_path):
        with open(file_path, 'r') as file:
            credentials = yaml.safe_load(file)
        return credentials
    
    @staticmethod
    def init_db_engine(credentials):
        engine = create_engine(f"{credentials['RDS_DATABASE_TYPE']}+{credentials['RDS_DBAPI']}://{credentials['RDS_USER']}:{credentials['RDS_PASSWORD']}@{credentials['RDS_HOST']}:{credentials['RDS_PORT']}/{credentials['RDS_DATABASE']}")
        return engine

# hello

