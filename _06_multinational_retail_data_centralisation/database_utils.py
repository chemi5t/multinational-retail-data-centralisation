import yaml # to read .yaml. Help with read_db_creds

# from sklearn.datasets import load_iris
from sqlalchemy import create_engine # this ORM will transform the python objects into SQL tables


class DatabaseConnector:
    """
    A utility class for handling database connections and operations.
    """
    @staticmethod
    def read_db_creds(file_path: str):
        """
        The read_db_creds function reads the database credentials from a YAML file.
        
        Args:
            file_path (str): Path to the YAML file containing credentials.

        Returns:
            dict: Database credentials as a dictionary.
        """
        with open(file_path, 'r') as file:
            credentials = yaml.safe_load(file)
        return credentials
    
    @staticmethod
    def init_db_engine(credentials: dict):
        """
        The init_db_engine function initializes the database engine based on the provided credentials.

        Args:
            credentials (dict): Dictionary containing database connection details.

        Returns:
            tuple: A tuple containing database engine objects.
        """
        engine = create_engine(f"{credentials['RDS_DATABASE_TYPE']}+{credentials['RDS_DBAPI']}://{credentials['RDS_USER']}:{credentials['RDS_PASSWORD']}@{credentials['RDS_HOST']}:{credentials['RDS_PORT']}/{credentials['RDS_DATABASE']}")
        engine2 = create_engine(f"{credentials['DATABASE_TYPE']}+{credentials['DBAPI']}://{credentials['USER']}:{credentials['PASSWORD']}@{credentials['HOST']}:{credentials['PORT']}/{credentials['DATABASE']}")

        return engine, engine2
    
    @staticmethod
    def upload_to_db(selected_table_df, selected_table: str, engine2):
        """
        The upload_to_db function takes a DataFrame, the name of a database table, and an engine object as arguments.
        It then uploads the data in the DataFrame to the database table in pgAdmin 4 using SQLAlchemy.

        Args:
            selected_table_df (DataFrame): DataFrame containing the data to be uploaded.
            selected_table (str): Name of the database table.
            engine2: Database engine object.
        """
        selected_table_df.to_sql(selected_table, engine2, if_exists='replace', index=False)
        print(f"Data uploaded to table '{selected_table}'.\n")



