import pandas as pd
from database_utils import DatabaseConnector as dc

import numpy as np
import nbformat
import plotly.express as px
import missingno as msno
import re
from dateutil.parser import parse # to help with datatime edits
from IPython.display import display
import requests


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

        # 'join_date' and 'date_of_birth'
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
    
    @staticmethod
    def called_clean_store_data(store_details_df):
        # Filter and include rows where 'lat' values are isnull
        store_details_df_filtered = store_details_df[store_details_df['lat'].isnull()]

        store_details_df_filtered = store_details_df_filtered.drop('lat', axis=1)

        # Filter and exclude rows where 'longitude' values are notnull
        store_details_df_filtered = store_details_df_filtered[store_details_df_filtered['longitude'].notnull()]

        # Filter and exclude rows where 'longitude' values are isnull i.e. we want notnull rows
        store_details_df_filtered = store_details_df_filtered[store_details_df_filtered['longitude'].notnull()]

        # Filter out letters from the 'staff_numbers'
        store_details_df_filtered['staff_numbers'] = store_details_df_filtered['staff_numbers'].str.replace(r'[^0-9]', '', regex=True)
        store_details_df_filtered['staff_numbers'] = store_details_df_filtered['staff_numbers'].astype('int64')

        # Change datatype
        store_details_df_filtered['store_type'] = store_details_df_filtered['store_type'].astype('category')
        store_details_df_filtered['store_code'] = store_details_df_filtered['store_code'].astype('string')
        store_details_df_filtered['country_code'] = store_details_df_filtered['country_code'].astype('category')

        # Replace 'eeEurope': 'Europe', 'eeAmerica': 'America'
        store_details_df_filtered['continent'] = store_details_df_filtered['continent'].replace({'eeEurope': 'Europe', 'eeAmerica': 'America'})
        store_details_df_filtered['continent'] = store_details_df_filtered['continent'].astype('category')

        # Change datatype to string
        store_details_df_filtered['address'] = store_details_df_filtered['address'].astype('string')
        store_details_df_filtered['locality'] = store_details_df_filtered['locality'].astype('string')

        # Convert the 'opening_date' column to datetime format
        store_details_df_filtered['opening_date'] = store_details_df_filtered['opening_date'].apply(parse)
        # To handle specific formats
        store_details_df_filtered['opening_date'] = store_details_df_filtered['opening_date'].combine_first(pd.to_datetime(store_details_df_filtered['opening_date'], errors='coerce', format='%Y %B %d'))
        # Convert 'expiry_date' to datetime format
        store_details_df_filtered['opening_date'] = pd.to_datetime(store_details_df_filtered['opening_date'], format='%y-%m-%d', errors='coerce')

        return store_details_df_filtered
    
    @staticmethod
    def convert_product_weights(products_df_filtered):
        def convert_weight(value):
            try:
                # Check if the value contains 'x' indicating a multiplication
                if 'x' in value:
                    # Extract numeric parts and units from both sides of 'x'
                    numeric_part1, units1, numeric_part2, units2 = re.match(r"([\d.]+)\s*([a-zA-Z]*)\s*x\s*([\d.]+)\s*([a-zA-Z]*)", value).groups()

                    # If units1 is empty, use units2
                    if not units1:
                        units1 = units2

                    # Multiply numeric parts together
                    result = float(numeric_part1) * float(numeric_part2)

                    # Handle units conversion for both parts
                    if units1.lower() in ['g', 'gram', 'grams']:
                        result /= 1000
                    elif units1.lower() in ['ml', 'milliliter', 'milliliters']:
                        result /= 1000
                    elif units1.lower() in ['kg', 'kilogram', 'kilograms']:
                        pass  # No conversion needed for kg
                    elif units1.lower() in ['oz', 'ounce', 'ounces']:
                        result *= 0.0283495
                    else:
                        # If units are not recognized, return NaN
                        return np.nan

                else:
                    # Extract numeric part and units from the value
                    numeric_part, units = re.match(r"([\d.]+)\s*([a-zA-Z]*)", value).groups()

                    # Multiply numeric part by the units
                    result = float(numeric_part)

                    # Handle units conversion
                    if units.lower() in ['g', 'gram', 'grams']:
                        result /= 1000
                    elif units.lower() in ['ml', 'milliliter', 'milliliters']:
                        result /= 1000
                    elif units.lower() in ['kg', 'kilogram', 'kilograms']:
                        pass  # No conversion needed for kg
                    elif units.lower() in ['oz', 'ounce', 'ounces']:
                        result *= 0.0283495
                    else:
                        # If units are not recognised, return NaN
                        return np.nan

                return result

            except Exception as e:
                # If any error occurs, return NaN
                return np.nan

        # Apply the conversion function to the 'weight' column
        products_df_filtered['weight'] = products_df_filtered['weight'].apply(convert_weight)
        cleaned_products_data = products_df_filtered.rename(columns={'weight': 'weight (kg)'})

        return cleaned_products_data

    @staticmethod
    def clean_products_data(products_df):
        # Show rows where 'product_price' values are notnull
        products_df_filtered = products_df[products_df['product_price'].notnull()]

        # regular expression to filter out rows where 'category' contains numbers
        products_df_filtered = products_df_filtered[~products_df_filtered['category'].str.contains('\d')]
        products_df_filtered['category'] = products_df_filtered['category'].astype('category')

        # Convert the 'date_added' column to datetime format
        products_df_filtered['date_added'] = products_df_filtered['date_added'].apply(parse)
        products_df_filtered['date_added'] = products_df_filtered['date_added'].combine_first(pd.to_datetime(products_df_filtered['date_added'], errors='coerce', format='%Y %B %d'))
        
        # Convert 'removed' to datatype 'category'
        products_df_filtered['removed'] = products_df_filtered['removed'].astype('category')
        
        return products_df_filtered