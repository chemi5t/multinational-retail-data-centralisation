import pandas as pd
from database_utils import DatabaseConnector as dc

import numpy as np
import nbformat
import plotly.express as px
import missingno as msno
import re
from dateutil.parser import parse # to help with datatime edits


class DataCleaning:
    
    @staticmethod
    def clean_user_data(selected_table_df):

    # filtering mask created
        condition_to_exclude = (
            selected_table_df['first_name'].astype(str).str.contains('\d|NULL') |
            selected_table_df['last_name'].astype(str).str.contains('\d|NULL') |
            selected_table_df['country'].astype(str).str.contains('\d|NULL')
            )
        
        # Apply the filter and convert the specified columns to string datatype
        legacy_users_df_filtered = selected_table_df[~condition_to_exclude].astype({'first_name': 'string', 'last_name': 'string', 'country': 'string'})

        legacy_users_df_filtered['country'] = legacy_users_df_filtered['country'].astype('category')
            
        # Replace 'GGB' with 'GB'
        legacy_users_df_filtered['country_code'] = legacy_users_df_filtered['country_code'].replace({'GGB': 'GB'})
        legacy_users_df_filtered['country_code'] = legacy_users_df_filtered['country_code'].astype('category')

        # Assuming 'join_date' is a column in 'date_of_birth'
        legacy_users_df_filtered['date_of_birth'] = legacy_users_df_filtered['date_of_birth'].apply(parse)
        legacy_users_df_filtered['join_date'] = legacy_users_df_filtered['join_date'].apply(parse)

        # Now, convert both columns to datetime
        legacy_users_df_filtered['date_of_birth'] = pd.to_datetime(legacy_users_df_filtered['date_of_birth'], errors='coerce')
        legacy_users_df_filtered['join_date'] = pd.to_datetime(legacy_users_df_filtered['join_date'], errors='coerce')

        legacy_users_df_filtered['company'] = legacy_users_df_filtered['company'].astype('category')

        legacy_users_df_filtered['email_address'] = legacy_users_df_filtered['email_address'].astype('string')

        # Change the data type of 'user_uuid' column to 'string'
        legacy_users_df_filtered['user_uuid'] = legacy_users_df_filtered['user_uuid'].astype('string')

        # Define a function to clean phone numbers and convert to string
        def clean_and_convert_to_string(phone_numbers):
            # Remove non-numeric characters, except '(', ')', and '+'
            cleaned_number = re.sub(r'[^0-9()+]+', '', phone_numbers)
            return cleaned_number

        # Apply the cleaning function and convert to string
        legacy_users_df_filtered['phone_number'] = legacy_users_df_filtered['phone_number'].apply(clean_and_convert_to_string).astype(str)

        return legacy_users_df_filtered

   