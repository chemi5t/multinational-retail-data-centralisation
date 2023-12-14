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
 
    @staticmethod
    def clean_card_data (card_details_df):
        # Show the rows where "card_number" isnull
        nulls_in_card_number = card_details_df["card_number"].isnull()
        card_details_df_filtered = card_details_df[~nulls_in_card_number]

        # Remove '?' from 'card_number' column
        card_details_df_filtered['card_number'] = card_details_df_filtered['card_number'].str.replace('?', '')

        # Check for entries that match a numeric pattern
        card_details_df_filtered = card_details_df_filtered[card_details_df_filtered['card_number'].str.isnumeric()]
        card_details_df_filtered['card_number'] = card_details_df_filtered['card_number'].astype('string')

        # Convert 'expiry_date' to datetime format
        card_details_df_filtered['expiry_date'] = pd.to_datetime(card_details_df_filtered['expiry_date'], format='%m/%y', errors='coerce')

        # Convert 'date_payment_confirmed' to datetime format
        card_details_df_filtered['date_payment_confirmed'] = card_details_df_filtered['date_payment_confirmed'].apply(parse)
        card_details_df_filtered['date_payment_confirmed'] = pd.to_datetime(card_details_df_filtered['date_payment_confirmed'], format='%y-%m-%d', errors='coerce')

        card_details_df_filtered['card_provider'] = card_details_df_filtered['card_provider'].astype('category')

        return card_details_df_filtered

    

        # print("Show the rows where \"card_number\" isnull:\n")
        # nulls_in_card_number = card_details_df["card_number"].isnull()
        # card_details_df_isnull = card_details_df[nulls_in_card_number]
        # print(card_details_df_isnull)
        # print("The table abovw shows rows with no data - this will need to be removed.\n")

        # # Display information about the DataFrame
        # print("card_details_df_isnull.info().\n")
        # print(card_details_df_isnull.info())

        # print("Show df excluding the NUlls found in card_number:\n")
        # card_details_df_filtered = card_details_df[~nulls_in_card_number]
        # card_details_df_filtered

        # # Check for entries that do not match a numeric pattern
        # non_numeric_entries = card_details_df_filtered[~card_details_df_filtered['card_number'].str.isnumeric()]

        # # Display the results
        # print("Entries with non-numeric characters:")
        # print(non_numeric_entries)
        # print(non_numeric_entries.info())
        # print(non_numeric_entries.describe())

        # # Check for the presence of '?' in 'card_number' column
        # count_with_question_mark = card_details_df_filtered['card_number'].str.contains('\?')

        # # Count the number of True values (entries with '?')
        # count_with_question_mark = len(card_details_df_filtered[count_with_question_mark])

        # # Display the count
        # print("Number of entries with '?':", count_with_question_mark, "\n")

        # # Remove '?' from 'card_number' column
        # card_details_df_filtered['card_number'] = card_details_df_filtered['card_number'].str.replace('?', '')
        # print("'?' replaced in card_number column.\n")

        # # Check for entries that do not match a numeric pattern
        # non_numeric_entries = card_details_df_filtered[~card_details_df_filtered['card_number'].str.isnumeric()]

        # # Display the results
        # print("Entries with non-numeric pattern in card_number column to exclude from df:\n")
        # print(non_numeric_entries)
        # print(non_numeric_entries.info())
        # print(non_numeric_entries.describe())

        # # Check for entries that do match a numeric pattern
        # print("Entries with numeric characters:\n")
        # card_details_df_filtered = card_details_df_filtered[card_details_df_filtered['card_number'].str.isnumeric()]
        # card_details_df_filtered['card_number'] = card_details_df_filtered['card_number'].astype('string')
        # print(card_details_df_filtered)
        # print(card_details_df_filtered.info())

        # # Convert 'expiry_date' to datetime format
        # card_details_df_filtered['expiry_date'] = pd.to_datetime(card_details_df_filtered['expiry_date'], format='%m/%y', errors='coerce')

        # # Display the updated DataFrame information
        # print(card_details_df_filtered.info())
        # print(card_details_df_filtered)


        # # Convert 'date_payment_confirmed' to datetime format
        # print("Need to convert date_payment_confirmed to datetime64[ns].\n")
        # print(card_details_df_filtered.info())
        # print("Converted date_payment_confirmed to datetime64[ns].\n")
        # card_details_df_filtered['date_payment_confirmed'] = card_details_df_filtered['date_payment_confirmed'].apply(parse)
        # print(card_details_df_filtered.info())
        # card_details_df_filtered['date_payment_confirmed'] = pd.to_datetime(card_details_df_filtered['date_payment_confirmed'], format='%y-%m-%d', errors='coerce')
        # print(card_details_df_filtered)

        # card_details_df_filtered['card_provider'] = card_details_df_filtered['card_provider'].astype('category')
        # print(card_details_df_filtered.info())

        # return card_details_df_filtered


