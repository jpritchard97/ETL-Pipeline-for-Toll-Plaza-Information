'''
Objective:
    To create an ETL (Extract, Transform, Load) pipeline for scraping toll plaza information, processing it, and storing it in an SQLite database.

Class Definition: ETL

1. **Initialization (`__init__` method):**
    - Input: `plaza_id` (ID of the toll plaza), `sql_file_path` (path to the SQLite database file), `sql_table_name` (name of the SQLite table)
    - Set instance variables:
        - `self.plaza_id` to `plaza_id`
        - `self.sql_file_path` to `sql_file_path`
        - `self.sql_table_name` to `sql_table_name`
        - `self.url` to formatted URL using `plaza_id`
        - `self.soup` to an empty string (placeholder for BeautifulSoup object)
        - `self.df_info` to an empty DataFrame (placeholder for processed data)

2. **Extract (`extract` method):**
    - Make an HTTP GET request to `self.url`
    - Parse the response using BeautifulSoup
    - Check if an HTML element with class 'PA15' exists in the parsed content
    - If found, return `True`
    - If not found, return `False`

3. **Transform (`transform` method):**
    - Extract plaza name from the HTML element with class 'PA15'
        - Find the first `<p>` tag within this element
        - Find the first `<lable>` tag within the `<p>` tag
    - Find and convert the first HTML table with class 'tollinfotbl' to a pandas DataFrame
        - Drop rows where all values are NaN
    - Modify DataFrame:
        - Insert 'Date Scrapped', 'Plaza Name', and 'TollPlazaID' columns at the beginning
        - Set 'Plaza Name' column with the extracted plaza name
        - Set 'TollPlazaID' column with `self.plaza_id`
        - Set 'Date Scrapped' column with the current date
    - Update `self.df_info` with the transformed DataFrame, ensuring column order

4. **Load (`load` method):**
    - Connect to the SQLite database using `self.sql_file_path`
    - Load `self.df_info` DataFrame into the SQLite table named `self.sql_table_name`
        - Append data if the table already exists
    - Close the database connection

5. **Run ETL (`run_etl` method):**
    - Call the `extract` method:
        - If `extract` returns `True`:
            - Call the `transform` method
            - Call the `load` method
            - Print a message indicating successful ETL processing for the current `plaza_id`
        - If `extract` returns `False`:
            - Print a message indicating failure to extract data for the current `plaza_id`
End
'''
# Import necessary modules for data processing and web scraping
import pandas as pd  # Import pandas for data manipulation
import requests  # Import requests for making HTTP requests
from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML
from datetime import date  # Import date for date handling
import sqlite3  # Import sqlite3 for database interactions

# Define the ETL class to encapsulate the ETL process
class ETL:

    # Initialize the ETL object with necessary parameters
    def __init__(self, plaza_id, sql_file_path, sql_table_name):
        # Store the plaza ID for which ETL will be performed
        self.plaza_id = plaza_id
        # Path to the SQLite database file
        self.sql_file_path = sql_file_path
        # Name of the table in the database where data will be loaded
        self.sql_table_name = sql_table_name
        # URL for retrieving information specific to the plaza ID
        self.url = f'https://tis.nhai.gov.in/TollInformation.aspx?TollPlazaID={plaza_id}'
        # Initialize BeautifulSoup object (will be populated in extract method)
        self.soup = ''
        # Initialize an empty DataFrame for storing data
        self.df_info = pd.DataFrame()

    # Extract method to retrieve and parse web data
    def extract(self):
        # Make a GET request to the specified URL
        web_request = requests.get(self.url)
        # Parse the HTML content of the response using BeautifulSoup
        self.soup = BeautifulSoup(web_request.text, 'html.parser')
        # Check if the relevant element is found in the HTML
        if self.soup.find(class_='PA15'):
            # Return True if extraction is successful
            return True
        # Return False if extraction fails
        return False
    
    # Transform method to process and clean the extracted data
    def transform(self):
        # Find the plaza name in the parsed HTML
        plaza_name = self.soup.find(class_='PA15').find_all('p')[0].find('lable')
        # Extract the HTML of the table containing toll information
        table_html = str(self.soup.find_all('table', class_='tollinfotbl')[0])
        # Read the HTML table into a DataFrame and drop rows with all NaN values
        df_info = pd
