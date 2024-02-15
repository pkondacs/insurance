# Loading all three dataframes to postgreSQL
import pandas as pd
from sqlalchemy import create_engine

# Replace these with your actual database credentials
db_username = 'postgres'
db_password = 'postgre'
db_host = 'localhost'
db_port = '5432'
db_name = 'insurance'

# Create the SQLAlchemy engine
engine = create_engine(f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')
# Load the DataFrame into the PostgreSQL table
fct_covers_table.to_sql('fct_covers_table', engine, if_exists='replace', index=False)
fct_policies_table.to_sql('fct_policies_table', engine, if_exists='replace', index=False)
dim_products.to_sql('dim_products', engine, if_exists='replace', index=False)

