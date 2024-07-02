import pandas as pd
import pyexcel_ods3

# Existing ODS file
existing_file = '/home/hemanth/Desktop/Vehicle.ods'

# New data to append
new_data = {'Name': ['Bob'], 'Age': [28], 'Salary': [55000]}
df_new = pd.DataFrame(new_data)

# Read existing data
data_existing = pyexcel_ods3.get_data(existing_file)
sheet_name = list(data_existing.keys())[0]  # Assuming there's only one sheet
data_list = data_existing[sheet_name]

# Convert existing data to DataFrame
columns = data_list[0]
data_existing = pd.DataFrame(data_list[1:], columns=columns)

# Append new data using pd.concat
df_combined = pd.concat([data_existing, df_new], ignore_index=True)

# Save the combined data to ODS
data_combined = [df_combined.columns.tolist()] + df_combined.values.tolist()
pyexcel_ods3.save_data(existing_file, {sheet_name: data_combined})
