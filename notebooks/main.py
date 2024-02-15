
from csv_loading import Loading, generate_metadata
from module2 import my_function

# Now you can use the imported classes and functions
if __name__ == "__main__":
    # Create an instance of MyClass and call its method
    my_class_instance = MyClass()
    my_class_instance.my_method()

    # Call the function from module2
    my_function()



# Create a class instance
insur_data_load = Loading('C:\insurance\data')
# The `files` will be a dictionary type with keys (=file names) and values (=DataFrames)
files = insur_data_load.load_all_files({
    'fct_covers_table_small.csv': 'csv_parse_custom',
    'fct_policies_table.csv': 'read_csv',
    'dim_products.csv': 'read_csv'
})

# Create dataframes by using the keys of the `files` dictionary 
fct_covers_table = files['fct_covers_table_small']
fct_policies_table = files['fct_policies_table']
dim_products = files['dim_products']

### Populate a metadata csv file including all dataframes and their column types 
metadata_df = generate_metadata(files)
metadata_df.to_csv(r"C:\insurance\data\metadata_out.csv", index=False)