# %pip install pandas sqlalchemy
import re
import pandas as pd

# Create a loading class with different types of methods for loading
class Loading:
    def __init__(self, subfolder):
        self.subfolder = subfolder

    def csv_parse_custom(self, file_path):
        data = []
        pattern = re.compile(r',(?![ ])')
        with open(file_path, 'r') as file:
            header_line = file.readline().strip()
            headers = pattern.split(header_line)
            for line in file:
                parts = pattern.split(line.strip())
                data.append(parts)
        return pd.DataFrame(data, columns=headers)

    def load_file(self, file_name, method):
        if method == 'read_csv':
            return pd.read_csv(f'{self.subfolder}/{file_name}')
        elif method == 'csv_parse_custom':
            return self.csv_parse_custom(f'{self.subfolder}/{file_name}')
        else:
            raise ValueError("Unknown method specified for loading file.")

    def load_all_files(self, files_to_methods):
        loaded_files = {}
        for file_name, method in files_to_methods.items():
            # Remove the '.csv' extension from the file name before using it as a key
            file_key = file_name[:-4] if file_name.lower().endswith('.csv') else file_name
            loaded_files[file_key] = self.load_file(file_name, method)
        return loaded_files
    
# Populate a metadata csv file including all dataframes and their column types 
def generate_metadata(files):
    data = []
    for file_name, df in files.items():
        columns = df.columns.tolist()
        types = df.dtypes.tolist()
        for column, data_type in zip(columns, types):
            data.append([file_name, column, str(data_type)])
    return pd.DataFrame(data, columns=['file', 'columns', 'type'])
