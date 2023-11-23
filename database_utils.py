import yaml # to read .yaml. Help with read_db_creds
import psycopg2 # a PostgreSQL adapter for Python

class DatabaseConnector:

    @staticmethod
    def read_db_creds(file_path):
        try:
            with open(file_path, 'r') as file:
                credentials = yaml.safe_load(file)
                print(credentials)
            return credentials
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File {file_path} not found.")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error while parsing YAML: {e}")

# Usage:
file_path = 'db_creds.yaml'  # Specify the correct file path
try:
    credentials = DatabaseConnector.read_db_creds(file_path)
except FileNotFoundError as e:
    print(e)
except yaml.YAMLError as e:
    print(e)


# Now create a method init_db_engine which will read the credentials from the return of read_db_creds and initialise and return an sqlalchemy database engine.

    def init_db_engine(credentials):

        with psycopg2.connect(host= credentials[RDS_HOST], user=credentials[RDS_USER], password=credentials[RDS_PASSWORD], dbname=credentials[RDS_DATABASE], port=credentials[RDS_PORT]) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'""")
                for table in cur.fetchall():
                    print(table)