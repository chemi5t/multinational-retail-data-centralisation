import yaml # to read .yaml. Help with read_db_creds
from sqlalchemy import create_engine # this ORM will transform the python objects into SQL tables
from sklearn.datasets import load_iris

class DatabaseConnector:

    @staticmethod
    def read_db_creds(file_path='db_creds.yaml'):
        with open(file_path, 'r') as file:
            credentials = yaml.safe_load(file)
        return credentials
    
    @staticmethod
    def init_db_engine(credentials: dict):
        engine = create_engine(f"{credentials['RDS_DATABASE_TYPE']}+{credentials['RDS_DBAPI']}://{credentials['RDS_USER']}:{credentials['RDS_PASSWORD']}@{credentials['RDS_HOST']}:{credentials['RDS_PORT']}/{credentials['RDS_DATABASE']}")
        engine2 = create_engine(f"{credentials['DATABASE_TYPE']}+{credentials['DBAPI']}://{credentials['USER']}:{credentials['PASSWORD']}@{credentials['HOST']}:{credentials['PORT']}/{credentials['DATABASE']}")

        return engine, engine2
    
    @staticmethod
    def upload_to_db(selected_table_df, selected_table, engine2):
        selected_table_df.to_sql(selected_table, engine2, if_exists='replace', index=False)
        print(f"Data uploaded to table '{selected_table}'.\n")


DatabaseConnector.read_db_creds()

