import pandas as pd
from database_utils import DatabaseConnector as dc

import numpy as np
import nbformat
import plotly.express as px
import missingno as msno
import re
from dateutil.parser import parse # to help with datatime edits
from IPython.display import display


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
 
    @staticmethod
    def clean_card_data(card_details_df):
         
        # Remove rows where "card_number" is null
        card_details_df_filtered = card_details_df.dropna(how='all')

        # Convert 'expiry_date' to datetime format
        card_details_df_filtered['expiry_date'] = pd.to_datetime(card_details_df_filtered['expiry_date'], format='%m/%y', errors='coerce')

        # Format 'expiry_date' for display (month/year)
        card_details_df_filtered['expiry_date'] = card_details_df_filtered['expiry_date'].dt.strftime('%m/%y')

        # Remove rows where "expiry_date" is null
        card_details_df_filtered = card_details_df_filtered.dropna(subset=['expiry_date'])

        # Convert 'date_payment_confirmed' to datetime format
        card_details_df_filtered['date_payment_confirmed'] = card_details_df_filtered['date_payment_confirmed'].apply(parse)
        card_details_df_filtered['date_payment_confirmed'] = pd.to_datetime(card_details_df_filtered['date_payment_confirmed'], format='%y-%m-%d', errors='coerce')

        # Convert 'card_provider' to datatype 'category'
        card_details_df_filtered['card_provider'] = card_details_df_filtered['card_provider'].astype('category')

        # Remove '?' from 'card_number' column
        card_details_df_filtered['card_number'] = card_details_df_filtered['card_number'].astype('str').apply(lambda x: x.replace("?", ''))
        card_details_df_filtered['card_number'] = card_details_df_filtered['card_number'].astype('string')

        return card_details_df_filtered