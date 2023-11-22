import yaml # to read .yaml

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
