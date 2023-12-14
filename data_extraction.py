from database_utils import DatabaseConnector
from sqlalchemy import inspect
import pandas as pd
import tabula # read tables in a PDF
import nbformat # save as .ipynb

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
