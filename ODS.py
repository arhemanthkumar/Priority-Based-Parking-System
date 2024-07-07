import pandas as pd
import pyexcel_ods3
from datetime import datetime
import os
import Character_Recognition
from main import Yolov4

date = ""
time = ""

# Global variables for parking space
total_parking_space = 120

def ods(vehicle_class, vehicle_no):
    global date
    global time
    global total_parking_space

    # Existing ODS files
    existing_file = 'Vehicle.ods'
    registered_file = 'registered_vehicles.ods'

    # Function to initialize the ODS file if it doesn't exist or is empty
    def initialize_ods_file(file_path):
        initial_data = {
            'Sheet1': [
                ['Date', 'Vehicle Class', 'License Plate', 'Registered', 'Status', 'Time', 'Occupied', 'Available']
            ]
        }
        pyexcel_ods3.save_data(file_path, initial_data)

    # Check if the ODS file exists and has data
    if not os.path.exists(existing_file) or not pyexcel_ods3.get_data(existing_file):
        initialize_ods_file(existing_file)

    # Read existing data
    try:
        data_existing = pyexcel_ods3.get_data(existing_file)
        sheet_name = list(data_existing.keys())[0]  # Assuming there's only one sheet
        data_list = data_existing[sheet_name]

        # Ensure there's data in the ODS file
        if len(data_list) == 0:
            # Initialize with header if no data is present
            columns = ['Date', 'Vehicle Class', 'License Plate', 'Registered', 'Status', 'Time', 'Occupied', 'Available']
            data_existing = pd.DataFrame(columns=columns)
        else:
            # Convert existing data to DataFrame
            columns = data_list[0]
            data_existing = pd.DataFrame(data_list[1:], columns=columns)

    except ValueError as e:
        print(f"Error loading data: {e}")
        # Handle the error as needed

    # Read registered vehicles data
    try:
        registered_data = pyexcel_ods3.get_data(registered_file)
        registered_sheet_name = list(registered_data.keys())[0]  # Assuming there's only one sheet
        registered_list = registered_data[registered_sheet_name]

        # Flatten the list if it's nested
        registered_vehicles = [item for sublist in registered_list for item in sublist]

    except ValueError as e:
        print(f"Error loading registered vehicles data: {e}")
        registered_vehicles = []

    # Initialize occupied and available spaces
    if data_existing.empty:
        occupied_spaces = 0
    else:
        occupied_spaces = int(data_existing.iloc[-1]['Occupied'])

    # New data to append
    new_data_template = {
        'Date': Character_Recognition.fetch_date_and_time()[0],
        'Vehicle Class': vehicle_class,
        'License Plate': vehicle_no,
        'Registered': 'Yes or No',
        'Status': 'Entry / Exit',
        'Time': Character_Recognition.fetch_date_and_time()[1],
        'Occupied': occupied_spaces,
        'Available': total_parking_space - occupied_spaces
    }

    # Function to search for a particular name in the License Plate column and update DataFrame
    def search_and_update(license_plate, df, new_data_template, registered_vehicles):
        nonlocal occupied_spaces  # Ensure we update the outer occupied_spaces variable
        new_data = new_data_template.copy()
        new_data['License Plate'] = license_plate
        new_data['Time'] = Character_Recognition.fetch_date_and_time()[1]

        # Update the 'Registered' column based on the registered vehicles list
        if license_plate in registered_vehicles:
            new_data['Registered'] = 'Yes'
        else:
            new_data['Registered'] = 'No'

        # Debugging: Print columns to verify column names
        # print("Columns:", df.columns.tolist())

        if isinstance(df, pd.DataFrame) and 'License Plate' in df.columns:  # Check if 'License Plate' is in columns
            if license_plate in df['License Plate'].values:
                # Get the last status for this license plate
                last_status = df[df['License Plate'] == license_plate].iloc[-1]['Status']
                if last_status == 'Exit':
                    new_data['Status'] = 'Entry'
                    occupied_spaces += 1
                    print(f"{license_plate} last status was 'Exit'. Adding data with status 'Entry'.")
                else:
                    new_data['Status'] = 'Exit'
                    occupied_spaces -= 1
                    print(f"{license_plate} last status was 'Entry'. Adding data with status 'Exit'.")
            else:
                new_data['Status'] = 'Entry'
                occupied_spaces += 1
                print(f"{license_plate} not found. Adding new data with status 'Entry'.")
        else:
            print("'License Plate' column not found in DataFrame.")
            # Handle this situation based on your application logic

        # Ensure occupied and available are within valid limits
        if occupied_spaces < 0:
            occupied_spaces = 0
        elif occupied_spaces > total_parking_space:
            occupied_spaces = total_parking_space

        new_data['Occupied'] = occupied_spaces
        new_data['Available'] = total_parking_space - occupied_spaces

        # Append new data
        new_row = pd.DataFrame([new_data])
        df = pd.concat([df, new_row], ignore_index=True)

        return df

    def print_last_row(df):
        if not df.empty:
            # print("\nLast row of the DataFrame:")
            print(df.iloc[-1])
        else:
            print("The DataFrame is empty.")

    # Example usage
    license_plate_to_search = vehicle_no
    data_existing = search_and_update(license_plate_to_search, data_existing, new_data_template, registered_vehicles)

    # Save the updated data to ODS
    data_combined = [data_existing.columns.tolist()] + data_existing.values.tolist()
    pyexcel_ods3.save_data(existing_file, {sheet_name: data_combined})
    print_last_row(data_existing)

if __name__ == '__main__':
    ods('Sedan', 'XYZ123')
