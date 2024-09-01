'''
Objective:
    To retrieve all toll plaza IDs from a specified web service using HTTP requests and regular expressions.

Function: `get_all_plaza_ids`

1. **Initialize Session:**
    - Create an HTTP session using `requests.Session()`

2. **Set Up Cookies and Headers:**
    - Define cookies (if any) to be used in the HTTP request
    - Define headers for the HTTP request, including:
        - 'Content-Type': 'application/json; charset=utf-8'
        - 'Accept': 'application/json, text/javascript, */*; q=0.01'
        - 'X-Requested-With': 'XMLHttpRequest'

3. **Prepare Data Payload:**
    - Define the data payload to be sent with the POST request:
        - Data: '{"TollName":""}'

4. **Make HTTP POST Request:**
    - Send a POST request to the URL: 'https://tis.nhai.gov.in/TollPlazaService.asmx/GetTollPlazaInfoGrid'
    - Use the defined cookies, headers, and data payload

5. **Check Response Status:**
    - If the response status code is 200 (successful):
        - Extract the response text
        - Use regular expressions to find all occurrences of 'javascript:TollPlazaPopup(\d+)' in the response text
        - Extract the numeric IDs from the matched strings
        - Convert extracted IDs to integers
        - Return the list of IDs
    - If the response status code is not 200:
        - Print an error message indicating the failure
        - Return an empty list

6. **Main Execution:**
    - Call the `get_all_plaza_ids` function
    - Print the list of plaza IDs
End
'''
# Import necessary modules for web scraping and data processing
from requests_html import HTMLSession  # Import HTMLSession for making HTTP requests
from requests import session  # Import session for managing HTTP requests
from requests import cookies  # Import cookies for handling session cookies
import re  # Import re for regular expression operations
import json  # Import json for handling JSON data
from lxml.html.clean import Cleaner  # Import Cleaner for cleaning HTML content

# Define the function to retrieve all plaza IDs
def get_all_plaza_ids():
    # Create an HTML session to manage the request
    with HTMLSession() as session:
        # Define cookies to be used in the request (example session ID provided)
        cookies = {
            'ASP.NET_SessionId': 'yrssr4bvbpomdtp5keikyths',
        }

        # Define headers for the request to mimic a real browser request
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

        # Define the data payload to be sent with the POST request
        data = '{"TollName":""}'  # Use JSON format for the data payload

        # Make the POST request to the specified URL
        response = session.post(
            'https://tis.nhai.gov.in/TollPlazaService.asmx/GetTollPlazaInfoGrid',
            cookies=cookies,
            headers=headers,
            data=data
        )

        # Check if the response was successful (status code 200)
        if response.status_code == 200:
            # Extract IDs from the response text using regex
            lresponse = re.findall(r'javascript:TollPlazaPopup\(\d+\)', response.text)
            # Convert extracted ID strings to integers
            ids = [int(re.findall(r'\d+', str_)[0]) for str_ in lresponse]
            # Return the list of IDs
            return ids
        else:
            # Print error message if the request failed
            print(f"Request failed with status code: {response.status_code}")
            # Return an empty list in case of failure
            return []

# Main execution block
if __name__ == "__main__":
    # Call the function to get all plaza IDs
    plaza_ids = get_all_plaza_ids()
    # Print the retrieved plaza IDs for verification
    print(plaza_ids)
