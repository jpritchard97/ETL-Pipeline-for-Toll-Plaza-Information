# ETL Pipeline for Toll Plaza Information

## Project Overview

This project implements an ETL (Extract, Transform, Load) pipeline designed to scrape toll plaza information from the National Highways Authority of India (NHAI) website, process the data, and store it into an SQLite database. The project leverages web scraping techniques to collect toll plaza details and then processes this data to be loaded into a relational database for further analysis and reporting.

## Project Components

1. **`fetch_plaza_ids.py`**: This module contains the function `get_all_plaza_ids`, which sends an HTTP POST request to the NHAI API to retrieve all toll plaza IDs.

2. **`ETL.py`**: Defines the `ETL` class responsible for the ETL process. It includes methods for extracting toll plaza details, transforming the data into a suitable format, and loading it into an SQLite database.

3. **`main.py`**: This script orchestrates the ETL process. It retrieves all plaza IDs, creates an `ETL` object for each ID, and runs the ETL process concurrently using multithreading.

## Installation

To set up this project on your local machine, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository

2. **Create and Activate a Virtual Environment**

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

3. **Install Required Dependencies**

Create a requirements.txt file with the following content:

requests==2.28.1
beautifulsoup4==4.12.0
pandas==2.0.3
requests-html==0.10.0
lxml==4.9.2

Then, install the dependencies:

pip install -r requirements.txt

4. **Usage**

    1. **Run the ETL Pipeline**

Execute the main.py script to start the ETL process. This script will:

- Retrieve all toll plaza IDs.
- Create an ETL object for each ID.
- Run the ETL process concurrently using a thread pool.

python main.py

    2. **Check the Output**

After running the script, the data will be saved into an SQLite database file named nhai_info.db. The table for storing the toll plaza data will be named nhai_toll_info_<date>, where <date> corresponds to the date when the data was scraped.

To interact with the SQLite database, you can use any SQLite client or the command-line interface.
