import pandas as pd
import pyexcel_ods3

# File containing the list of registered cars
registered_file = 'registered_vehicles.ods'

# Read registered cars data
data_registered = pyexcel_ods3.get_data(registered_file)
sheet_name = list(data_registered.keys())[0]  # Assuming there's only one sheet
data_list = data_registered[sheet_name]

# Convert registered cars data to DataFrame
columns = data_list[0]
df_registered = pd.DataFrame(data_list[1:], columns=columns)

# Function to check if a car is registered
def is_car_registered(car_name, df):
    if car_name in df.iloc[:, 0].values:
        print(f"{car_name} is present in the registered database.")
        return True
    else:
        print(f"{car_name} is not present in the registered database.")
        return False

# Example usage
car_to_search = 'Benz'
is_registered = is_car_registered(car_to_search, df_registered)

# Return the status
print(is_registered)