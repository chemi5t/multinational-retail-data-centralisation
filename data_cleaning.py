import pandas as pd
from database_utils import DatabaseConnector as dc

import numpy as np
import nbformat
import plotly.express as px
import missingno as msno

class DataCleaning:
    
    @staticmethod
    def clean_user_data(selected_table_df):





    
    @staticmethod
    def clean_user_data(selected_table_df):
        # Drop duplicate rows
        selected_table_df = selected_table_df.drop_duplicates()

        # Handle missing values (replace NaNs with a specified value or strategy)
        selected_table_df = selected_table_df.fillna(0)  # Replace NaNs with 0, for example

        # Convert data types if needed (e.g., convert a column to datetime)
        selected_table_df['date_column'] = pd.to_datetime(selected_table_df['date_column'], errors='coerce')

        # Remove outliers (you may need a more sophisticated approach based on your data)
        selected_table_df = DataCleaning.remove_outliers(selected_table_df, 'numeric_column')

        # Perform additional cleaning steps based on your specific requirements

        return selected_table_df

    @staticmethod
    def remove_outliers(df, column_name, z_threshold=3):
        # Remove outliers using Z-score
        z_scores = (df[column_name] - df[column_name].mean()) / df[column_name].std()
        df_no_outliers = df[(z_scores.abs() < z_threshold) | z_scores.isna()]
        return df_no_outliers
