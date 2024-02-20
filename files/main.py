
from csv_loading import Loading, generate_metadata
import sys, pandas as pd, pytest as pt

# Now you can use the imported classes and functions
if __name__ == "__main__":

    # Create a class instance inserting the subfolder where the data is stored
    insur_data_load = Loading('data')
    # List out the key/value pairs as files/parsing type pairs
    # The `files` will be a dictionary type with keys (=file names) and values (=DataFrames)
    files = insur_data_load.load_all_files({
        'fct_covers_table_small.csv': 'csv_parse_custom',
        'fct_policies_table.csv': 'read_csv',
        'dim_products.csv': 'read_csv'})

    # Create dataframes by using the keys of the `files` dictionary 
    fct_covers_table = files['fct_covers_table_small']
    fct_policies_table = files['fct_policies_table']
    dim_products = files['dim_products']
    # Print out results
    print(fct_covers_table.head())
    print(f"Python Version: {sys.version}")
    print(f"Pandas Version: {pd.__version__}")
    print(f"Pytest Version: {pt.__version__}")

# Populate a metadata csv file including all dataframes and their column types 
# metadata_df = generate_metadata(files)
# metadata_df.to_csv(r"C:\insurance\data\metadata_out.csv", index=False)