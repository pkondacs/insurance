
# Stratified sampling of large csv file to be able to store on github
import pandas as pd
from sqlalchemy import create_engine

# Replace these with your actual database credentials
db_username = 'postgres'
db_password = 'postgre'
db_host = 'localhost'
db_port = '5432'
db_name = 'insurance'

# 1. Create the SQLAlchemy engine
engine = create_engine(f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')

# 2. Retrieve the tables from the database
fct_covers_table = pd.read_sql_table('fct_covers_table', engine)
# fct_policies_table = pd.read_sql_table('fct_policies_table', engine)

files_loaded = {}
files_loaded['fct_covers_table'] = fct_covers_table
# files_loaded['fct_policies_table'] = fct_policies_table

# 3. Dictionary with the names of the dataframes and the field to be used for the dummy variable
dataframes = {
    'fct_covers_table': 'cover_premium'
    # 'fct_policies_table': 'policy_premium'
}

for df_name, field in dataframes.items():
    # fct_policies_table = files_loaded[df_name]
    fct_policies_table['premium_dummy'] = fct_policies_table[field].apply(lambda x: 0 if x == 0 else 1)

# 4. Display the results
fct_covers_table[fct_covers_table['premium_dummy'] > 0].head(100)
# fct_policies_table[fct_policies_table['policy_premium'] > 0].head(100)

# Assuming 'df' is your DataFrame and 'category_fields' is your list of fields for stratification
category_fields = ['cover_description','cover_status', 'object_type', 'premium_dummy']  # Replace with your actual field names

# Define the fraction of the sample you want
sample_fraction = 0.1  # For example, 10% of each group defined by unique combinations of category fields

# Calculate the number of samples for each group
grouped = fct_covers_table.groupby(category_fields)
sample_sizes = (grouped.size() * sample_fraction).apply(lambda x: max(1, int(x))).to_dict()

# Generate the stratified sample
stratified_sample = pd.DataFrame()

for group, size in sample_sizes.items():
    # 'group' is a tuple with values for each category field
    # 'size' is the number of samples to take from this group
    condition = (fct_covers_table[category_fields] == pd.Series(group, index=category_fields)).all(axis=1)
    group_sample = fct_covers_table[condition].sample(n=size, random_state=1)  # Use a random state for reproducibility
    stratified_sample = pd.concat([stratified_sample, group_sample])
# Now 'stratified_sample' contains your stratified sample with maintained distribution
    
# 5. Save the stratified sample to a CSV file
# Define the path where you want to save the CSV file
file_path = r'C:\insurance\data\fct_covers_table_small.csv'  # The 'r' before the string is to denote a raw string
# Save the DataFrame to a CSV file at the specified path
stratified_sample.to_csv(file_path, index=False)  # Set index=False if you don't want to write row indices

