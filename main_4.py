import pandas as pd
import numpy as np
import re
from dateutil.parser import parse # to help with datatime edits

import requests
    
    

def retrieve_stores_data(retrieve_store_endpoint, headers, number_of_stores=451):

    # Initialize an empty list to store data
    all_stores_data = []

    # Iterate through store numbers and retrieve data for each store
    for store_number in range(0, number_of_stores):
        # Format the endpoint with the specified store number
        endpoint = retrieve_store_endpoint + str(store_number)

        # Send GET request to the API
        response = requests.get(endpoint, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract store data from the response JSON
            store_data = response.json()
            all_stores_data.append(store_data)
        else:
            # If the request was not successful, print the status code and response text
            print(f"Request for store {store_number} failed with status code: {response.status_code}")
            print(f"Response Text: {response.text}")

    # Convert the list of store data into a Pandas DataFrame
    stores_df = pd.DataFrame(all_stores_data)
    return stores_df

def called_clean_store_data(store_details_df):
    
    df = store_details_df.copy()

    # Filter and include rows where 'lat' values are isnull
    # df = store_details_df[store_details_df['lat'].isnull()]
    
    # df = df.drop('lat', axis=1)

    # # Filter and exclude rows where 'store_code' values are isnull i.e. we want notnull rows
    # df = df[df['store_code'].notnull()]

    # Filter out letters from the 'staff_numbers'
    df['staff_numbers'] = df['staff_numbers'].str.replace(r'[^0-9]', '', regex=True)

    # Change datatype
    df['store_type'] = df['store_type'].astype('category')
    df['store_code'] = df['store_code'].astype('string')
    df['country_code'] = df['country_code'].astype('category')

    # Replace 'eeEurope': 'Europe', 'eeAmerica': 'America'
    df['continent'] = df['continent'].replace({'eeEurope': 'Europe', 'eeAmerica': 'America'})
    df['continent'] = df['continent'].astype('category')

    # Change datatype to string
    df['address'] = df['address'].astype('string')
    df['locality'] = df['locality'].astype('string')

    # Convert the 'opening_date' column to datetime format
    # df['opening_date'] = df['opening_date'].apply(parse)
    df['opening_date'] = df['opening_date'].combine_first(pd.to_datetime(df['opening_date'], errors='coerce', format='mixed'))
    df['opening_date'] = pd.to_datetime(df['opening_date'], format='mixed', errors='coerce')

    df = df.dropna(subset=['opening_date'])

    return df
    
##############################################################################################
headers = {
    'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'
}
retrieve_store_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/'
# retrieve data for all stores and save in a Pandas df
stores_df = retrieve_stores_data(retrieve_store_endpoint, headers)
print(len(stores_df))
cleaned_store_df = called_clean_store_data(stores_df)
print(len(cleaned_store_df))
# print(cleaned_store_df.head(5))
# print(cleaned_store_df, "\n")
