'''
Objective:
    To concurrently process toll plaza IDs using the ETL class, by creating ETL objects and running them in parallel threads.

1. **Import Modules and Functions:**
    - Import `ETL` class from `ETL.py`
    - Import `date` from `datetime`
    - Import `get_all_plaza_ids` function from `fetch_plaza_ids.py`
    - Import `concurrent.futures` for multithreading
    - Import `partial` from `functools` to fix some arguments in functions

2. **Define Function `create_etl_object_and_run`:**
    - Input: `plaza_id`, `db_file_path`, `db_table_name`
    - Create an instance of `ETL` class with the given `plaza_id`, `db_file_path`, and `db_table_name`
    - Call the `run_etl` method on the ETL instance to execute the ETL process

3. **Main Execution Block:**
    - Set `db_file_path` to 'nhai_info.db'
    - Set `db_table_name` to 'nhai_toll_info_' followed by today's date
    - Call `get_all_plaza_ids` function to retrieve a list of plaza IDs
    - Print the retrieved IDs for debugging purposes

4. **Prepare for Multithreading:**
    - Use `functools.partial` to create a partially-applied function (`partial_etl_function`) that pre-fills `db_file_path` and `db_table_name` arguments for `create_etl_object_and_run`

5. **Run ETL Processes Concurrently:**
    - Create a `ThreadPoolExecutor` with a maximum of 10 worker threads
    - Use the executor to map `partial_etl_function` across all plaza IDs
        - Each thread will run `create_etl_object_and_run` with the current plaza ID, `db_file_path`, and `db_table_name`
    - This will process all IDs concurrently
End
'''

# Import the ETL class from the ETL module
from ETL import ETL  # Ensure ETL.py is in the same directory or accessible path

# Import date for date handling
from datetime import date

# Import function to fetch all plaza IDs from fetch_plaza_ids module
from fetch_plaza_ids import get_all_plaza_ids

# Import modules for concurrent execution and partial function application
import concurrent.futures
from functools import partial

# Define a function to create an ETL object and run its ETL process
def create_etl_object_and_run(plaza_id, db_file_path, db_table_name):
    # Instantiate the ETL object with the given plaza ID, database file path, and table name
    plaza_etl = ETL(plaza_id, db_file_path, db_table_name)
    
    # Run the ETL process for the given plaza ID
    plaza_etl.run_etl()

# Main execution block
if __name__ == "__main__":
    # Define the path to the SQLite database file
    db_file_path = 'nhai_info.db'
    
    # Define the table name using today's date for uniqueness
    db_table_name = f'nhai_toll_info_{date.today()}'
    
    # Fetch all toll plaza IDs using the imported function
    ids = get_all_plaza_ids()
    
    # Print the retrieved IDs for debugging and verification
    print(f"IDs to process: {ids}")  # Debugging print

    # Create a partial function with fixed arguments for the ETL process
    # This helps in applying the same database path and table name to each ETL process
    partial_etl_function = partial(create_etl_object_and_run, db_file_path=db_file_path, db_table_name=db_table_name)
    
    # Use a ThreadPoolExecutor to run ETL processes concurrently
    # Set maximum number of worker threads to 10 for parallel processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Map the partial ETL function to all plaza IDs
        # Each ID will be processed concurrently by the worker threads
        executor.map(partial_etl_function, ids)



