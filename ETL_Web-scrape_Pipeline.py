'''
Objective:
    To create an ETL pipeline to scrape toll plaza information from a website, process it, and load it into a database.

Tools to use:
- Python
    requests, request-html
    beautifulsoup
    concurrent
    sqlite3
    pandas
    re module
    VSCode IDE
- Multithreading
- OOPs
- SQL

Design Architecture:
    1. Define an ETL class that encapsulates the ETL logic for a single page.
    2. Use multithreading to run ETL processes for multiple pages concurrently.
    3. Implement functions for data extraction, transformation, and loading.
    4. Store the final processed data into a SQL database (SQLite in this case).

Learning from this Exercise:
    - Web scraping and website inspection
    - Multithreading
    - Building ETL pipelines
    - Object-Oriented Programming (OOP)
    - Using functools' partial functions
    - Storing data into a Relational Database Management System (RDBMS)
    - Basics of Regular Expressions (Regex)

Steps:
1. Define and initialize cookies and headers for the HTTP request.
2. Send a POST request to the API endpoint to retrieve toll plaza information.
3. Parse the response to extract relevant data (toll plaza IDs).
4. Implement error handling for the request.
5. Save extracted data to a JSON file.
6. Define a class for the ETL pipeline:
    - Extract: Fetch and parse data from the API.
    - Transform: Clean and structure the data.
    - Load: Insert the data into an SQLite database.
7. Implement multithreading to handle multiple ETL processes concurrently.
8. Test and validate the entire ETL pipeline.

Python Script:
'''

import requests
import re
import json

# Define cookies and headers
cookies = {
    'ASP.NET_SessionId': 'yrssr4bvbpomdtp5keikyths',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8',
    'Origin': 'https://tis.nhai.gov.in',
    'Referer': 'https://tis.nhai.gov.in/tollplazasataglance.aspx?language=en',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

# Define the data payload
data = json.dumps({'TollName': ''})

# Make the POST request
response = requests.post(
    'https://tis.nhai.gov.in/TollPlazaService.asmx/GetTollPlazaInfoGrid',
    cookies=cookies,
    headers=headers,
    data=data,
)

# Check for successful response
if response.status_code == 200:
    # Extract strings that match the pattern
    lresponse = re.findall(r'javascript:TollPlazaPopup\((\d+)\)', response.text)
    
    # Convert extracted strings to integers
    ids = [int(id) for id in lresponse]

    # Print the raw response for debugging
    print("Raw response text:")
    print(response.text)

    # Print extracted IDs as integers
    print("Extracted IDs as integers:")
    print(ids)

    # Optionally, save to JSON file
    output_file_path = 'table_data.json'
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(ids, json_file, indent=4)
else:
    print(f"Error: Failed to retrieve data. Status code: {response.status_code}")