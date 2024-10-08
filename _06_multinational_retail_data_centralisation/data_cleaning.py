from dateutil.parser import parse # to help with datatime edits
from IPython.display import display
# from _06_multinational_retail_data_centralisation.database_utils import DatabaseConnector as dc

import numpy as np
import pandas as pd
import re
# import nbformat
# import plotly.express as px
# import missingno as msno
# import requests


class DataCleaning:
    """
    A class containing static methods to clean different types of data.
    """
    @staticmethod
    def clean_user_data(selected_table_df):
        """
        The clean_user_data function takes in a DataFrame containing user data and returns a cleaned version of the same.
        The function first filters out rows that contain invalid values for 'first_name', 'last_name', or 'country'.
        It then replaces all instances of GGB with GB, converts both date columns to datetime, changes the data type 
        of 'phone_numbers', 'user_uuid' and 'email_address' to string. Also changes data type of 'country', 'country_code' 
        and 'company' to 'category'

        Args:
            selected_table_df (pandas.DataFrame): The DataFrame containing user data.

        Returns:
            pandas.DataFrame: Cleaned user data.
        """

        # filtering mask created
        condition_to_exclude = (selected_table_df['first_name'].astype(str).str.contains('\d|NULL') |
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
            """
            The clean_and_convert_to_string function takes in a list of phone numbers and removes all non-numeric characters, except '(', ')', and '+'.
            
            Parameters:
                phone_numbers (str): A string containing phone numbers.
            
            Returns:
                str: The cleaned phone number string.
            """
            # Remove non-numeric characters, except '(', ')', and '+'
            cleaned_number = re.sub(r'[^0-9()+]+', '', phone_numbers)
            return cleaned_number

        # Apply the cleaning function and convert to string
        legacy_users_df_filtered['phone_number'] = legacy_users_df_filtered['phone_number'].apply(clean_and_convert_to_string).astype(str)

        return legacy_users_df_filtered
 
    @staticmethod
    def clean_card_data(card_details_df):
        """
        The clean_card_data function takes a DataFrame containing card details as input and returns a cleaned version of the same.
        The cleaning process involves removing rows where all values are null in the DataFrame. Converting 'expiry_date' to datetime 
        format (month/year). Removing rows 'expiry_date' is null. Converting 'date_payment_confirmed' to datetime format (year-month-day). 
        Converting 'card_provider' to datatype 'category'. Removing '?' from 'card_number' column and converting to datatype 'string'.
        
        Args:
            card_details_df (pandas.DataFrame): The DataFrame containing card details.

        Returns:
            pandas.DataFrame: Cleaned card details.
        """
         
        # Remove rows where all values are null in the DataFrame
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
        """
        The called_clean_store_data function cleans the store details data.

        Args:
            store_details_df (pandas.DataFrame): The DataFrame containing store details.

        Returns:
            pandas.DataFrame: Cleaned store details.
        """
        # drop na from 'continent' column
        store_details_df_filtered = store_details_df.dropna(subset=['continent'])

        # Replace 'eeEurope': 'Europe', 'eeAmerica': 'America'
        store_details_df_filtered.loc[:, 'continent'] = store_details_df_filtered['continent'].replace({'eeEurope': 'Europe', 'eeAmerica': 'America'})

        # Filtering mask created to islocate values containing numbers
        condition_to_exclude = store_details_df_filtered['continent'].astype(str).str.contains('\d')

        # Mask applied to exclude numbers from the 'continent' column
        store_details_df_filtered = store_details_df_filtered[~condition_to_exclude]

        store_details_df_filtered['continent'] = store_details_df_filtered['continent'].astype('category')

        store_details_df_filtered = store_details_df_filtered.drop('lat', axis=1)

        # Change datatype to category
        store_details_df_filtered['store_type'] = store_details_df_filtered['store_type'].astype('category')

        # Change datatype to string
        store_details_df_filtered['store_code'] = store_details_df_filtered['store_code'].astype('string')

        # Change datatype to category
        store_details_df_filtered['country_code'] = store_details_df_filtered['country_code'].astype('category')

        # Filter out letters from the 'staff_numbers'
        store_details_df_filtered['staff_numbers'] = store_details_df_filtered['staff_numbers'].str.replace(r'[^0-9]', '', regex=True)

        # Change datatype to string
        store_details_df_filtered['address'] = store_details_df_filtered['address'].astype('string')

        # Change datatype to string
        store_details_df_filtered['locality'] = store_details_df_filtered['locality'].astype('string')

        store_details_df_filtered['opening_date'] = pd.to_datetime(store_details_df_filtered['opening_date'], format='mixed', errors='coerce')

        # Convert 'country_code' to string
        store_details_df_filtered['country_code'] = store_details_df_filtered['country_code'].astype('str')

        # Remove rows where 'country_code' is NULL
        store_details_df_filtered = store_details_df_filtered[store_details_df_filtered['country_code'] != 'NULL']

        # display(store_details_df_filtered.info())
        # display(store_details_df_filtered)

        return store_details_df_filtered

    @staticmethod
    def convert_product_weights(products_df_filtered):
        """
        The convert_product_weights function takes a DataFrame as input and returns the same DataFrame with weights converted to kilograms.
        The function can handle strings with or without units, and it can also handle multiplication of two weights.
        For example:
            - '100g' will be converted to 0.100 kg
            - '2 x 100g' will be converted to 0.200 kg (i.e., 2 * 100 g)

        Args:
            products_df_filtered (pandas.DataFrame): The DataFrame containing product details.

        Returns:
            pandas.DataFrame: Cleaned product details with weights converted to kilograms.
        """
        def convert_weight(value):
            """
            The convert_weight function takes a string as input and returns the weight in kilograms.
            The function can handle strings with or without units, and it can also handle multiplication of two weights.
            
            Args:
                value (string): Pass the value to be converted.

            Returns:
                float: The converted weight.
            """
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

                return round(result, 3)

            except Exception as e:
                # If any error occurs, return NaN
                return np.nan

        # Apply the conversion function to the 'weight' column
        products_df_filtered['weight'] = products_df_filtered['weight'].apply(convert_weight)
        cleaned_products_data = products_df_filtered.rename(columns={'weight': 'weight_(kg)'})

        return cleaned_products_data

    @staticmethod
    def clean_products_data(products_df):
        """
        The clean_products_data function cleans the products data.

        Args:
            products_df (pandas.DataFrame): The DataFrame containing product details.

        Returns:
            pandas.DataFrame: Cleaned product details.
        """
        # Show rows where 'product_price' values are notnull
        products_df_filtered = products_df[products_df['product_price'].notnull()]

        # regular expression to filter out rows where 'category' contains numbers
        products_df_filtered = products_df_filtered[~products_df_filtered['category'].str.contains('\d')]
        products_df_filtered['category'] = products_df_filtered['category'].astype('category')

        # Convert the 'date_added' column to datetime format
        products_df_filtered['date_added'] = products_df_filtered['date_added'].apply(parse)
        products_df_filtered['date_added'] = products_df_filtered['date_added'].combine_first(pd.to_datetime(products_df_filtered['date_added'], errors='coerce', format='%Y %B %d'))
        
        # Correct the spelling in the column 'removed'
        products_df_filtered['removed'] = products_df_filtered['removed'].replace('Still_avaliable', 'Still_available')

        # Convert 'removed' to datatype 'category'
        products_df_filtered['removed'] = products_df_filtered['removed'].astype('category')
        
        return products_df_filtered
    
    @staticmethod
    def clean_orders_data(selected_table_df):
        """
        The clean_orders_data function takes in a pandas DataFrame containing order details and returns a cleaned version of the same.
        The function drops specified columns from the original DataFrame, namely: first_name, last_name and 1.

        Args:
            selected_table_df (pandas.DataFrame): The DataFrame containing order details.

        Returns:
            pandas.DataFrame: Cleaned order details.
        """
        # Drop specified columns
        columns_to_drop = ['first_name', 'last_name', '1']
        orders_df_filtered = selected_table_df.drop(columns=columns_to_drop)
        
        return orders_df_filtered
        
    @staticmethod
    def clean_date_data(date_details_df):
        """
        The clean_date_data function takes in a dataframe of date details and filters out the rows that do not contain
        the time periods 'Evening', 'Morning', 'Midday' or 'Late_Hours'. It then converts the column containing these values
        to a category datatype. The function returns this cleaned dataframe.

        Args:
            date_details_df (pandas.DataFrame): The DataFrame containing date details.

        Returns:
            pandas.DataFrame: Cleaned date details.
        """
        # filtering mask created
        condition_to_include = date_details_df['time_period'].astype(str).str.contains('Evening|Morning|Midday|Late_Hours')
        date_details_df_filtered = date_details_df[condition_to_include]

        # Convert 'time_period' to datatype 'category'
        date_details_df_filtered.loc[:, 'time_period'] = date_details_df_filtered['time_period'].astype('category')

        return date_details_df_filtered
