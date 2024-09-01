'''
Objective:
    To scrape toll plaza information from a web page, process it, and store it in an SQLite database.

Steps:
1. **Initialize Database Connection:**
    - Connect to SQLite database named 'nhai_info.db'
    - Create a cursor object to interact with the database

2. **Make Web Request:**
    - Send an HTTP GET request to the URL: 'https://tis.nhai.gov.in/TollInformation.aspx?TollPlazaID=5753'
    - Get the HTML response from the web request

3. **Parse HTML Content:**
    - Use BeautifulSoup to parse the HTML response

4. **Extract Plaza Name:**
    - Find the first HTML element with class 'PA15'
    - Within this element, find the first 'lable' tag
    - If 'lable' tag is found:
        - Extract and print its text content, removing leading/trailing whitespace
    - If 'lable' tag or 'PA15' element is not found:
        - Print appropriate error message

5. **Extract and Process Table Data:**
    - Find the first HTML table with class 'tollinfotbl'
    - Convert the HTML table to a string format
    - Read the HTML string into a pandas DataFrame
    - Drop rows where all values are NaN

6. **Add Metadata to DataFrame:**
    - Get the current date
    - Insert 'Date Scrapped' and 'Plaza Name' columns at the beginning of the DataFrame
    - Set 'Plaza Name' column with the extracted plaza name
    - Set 'Date Scrapped' column with the current date
    - Reorder columns to ensure 'Date Scrapped' and 'Plaza Name' are at the beginning

7. **Load Data into SQLite Database:**
    - Save the DataFrame to the SQLite database table 'nhai_toll_info'
    - Append data if the table already exists

8. **Close Database Connection:**
    - Close the database connection to save changes and release resources
End
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from datetime import date

conn = sqlite3.connect('nhai_info.db')
c = conn.cursor()

# Make the web request
web_request = requests.get('https://tis.nhai.gov.in/TollInformation.aspx?TollPlazaID=5753')
soup = BeautifulSoup(web_request.text, 'html.parser')

# Find the first 'lable' tag in the 'PA15' class
plaza_div = soup.find(class_='PA15')
if plaza_div:
    plaza_name = plaza_div.find('lable')
    if plaza_name:
        print(plaza_name.text.strip())  # Use .strip() to remove any leading/trailing whitespace
    else:
        print("No <lable> tag found")
else:
    print("No element with class 'PA15' found")

table = soup.find_all('table', class_='tollinfotbl')[0]
x = str(table)
y = pd.read_html(x)[0].dropna(axis=0, how='all')

cols = y.columns.tolist()
cols.insert(0, 'Date Scrapped')
cols.insert(1, 'Plaza Name')
y['Plaza Name'] = plaza_name.text
y['Date Scrapped'] = date.today()
y = y[cols]
y.to_sql('nhai_toll_info', conn, if_exists='append', index=False)









