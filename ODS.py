import pandas as pd  # imports pandas libraby to handle vehicle data
import pyexcel_ods3  # imports pyexcel_ods3 because we are handling files of format .ods instead of .xsl
from datetime import datetime  # imports time and date module
import os  # imports os module to get current directory information and allows us to change directory on demand
import Character_Recognition  # This is another .py file imported to get information of vehicles, status along with date and time

date = ""  # date variable to store date
time = ""  # time variable to store time

# Global variables for parking space
total_parking_space = 100  # declares total available parking space in total


def ods(vehicle_class, vehicle_no):  # ods function gets the info such as vehicle_class and vehicle_no from main.py
    global date  # declaring date as global so that we can access it outside the function
    global time  # declaring time as global so that we can access it outside the function
    global total_parking_space  # declaring total_parking_space as global for global access

    # Existing ODS files
    existing_file = 'Vehicle.ods'  # Store the name of the ods file which we want to output the vehicle information in the existing_file variable
    registered_file = 'registered_vehicles.ods'  # Store the name of the ods file which contains the list of registered vehicles in the registered_file variable

    # Function to initialize the ODS file if it doesn't exist or is empty
    def initialize_ods_file(file_path):
        initial_data = {
            'Sheet1': [
                ['Date', 'Vehicle Class', 'License Plate', 'Registered', 'Status', 'Time', 'Occupied', 'Available']
            ]
        }
        pyexcel_ods3.save_data(file_path, initial_data)  # This saves the file with initial data as the column headings

    # Check if the ODS file exists and has data
    if not os.path.exists(existing_file) or not pyexcel_ods3.get_data(existing_file):
        initialize_ods_file(existing_file)

    # Read existing data
    try:
        data_existing = pyexcel_ods3.get_data(existing_file)  # Reads the file
        sheet_name = list(data_existing.keys())[0]  # Assuming there's only one sheet
        data_list = data_existing[sheet_name]  # Creates the data list of the 1st sheet of the file

        # Ensure there's data in the ODS file
        if len(data_list) == 0:
            # Initialize with header if no data is present
            columns = ['Date', 'Vehicle Class', 'License Plate', 'Registered', 'Status', 'Time', 'Occupied',
                       'Available']
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
        registered_data = pyexcel_ods3.get_data(registered_file)  # Perform the same for the registered_vehicles.ods
        registered_sheet_name = list(registered_data.keys())[0]  # Assuming there's only one sheet
        registered_list = registered_data[registered_sheet_name]

        # Flatten the list if it's nested
        registered_vehicles = [item for sublist in registered_list for item in sublist]

    except ValueError as e:
        print(f"Error loading registered vehicles data: {e}")
        registered_vehicles = []

    # Initialize occupied and available spaces
    if data_existing.empty:
        occupied_spaces = 0  # Initially, if the data is empty, it initializes occupied_spaces to 0, because there are 0 vehicles at this point
    else:
        occupied_spaces = int(
            data_existing.iloc[-1]['Occupied'])  # If not, fetch the last updated value from "Occupied" column

    # New data to append
    new_data_template = {
        'Date': Character_Recognition.fetch_date_and_time()[0],
        # Stores the data which is fetched from Character_Recognition.py file
        'Vehicle Class': vehicle_class,  # Stores the Vehicle class whether it is 2-wheeler or 4-wheeler
        'License Plate': vehicle_no,  # Stores the License plate info
        'Registered': 'Yes or No',
        # Checks the status whether the license plate is registered in the "registered_vehicles".ods file or not
        'Status': 'Entry / Exit',  # Checks if the vehicle is entering or exiting
        'Time': Character_Recognition.fetch_date_and_time()[1],
        # Fetches and stores the Time when the vehicle entered or exited
        'Occupied': occupied_spaces,  # Stores parking space occupied count
        'Available': total_parking_space - occupied_spaces  # Stores parking space available count
    }

    # Function to search for a particular name in the License Plate column and update DataFrame
    def search_and_update(license_plate, df, new_data_template, registered_vehicles):
        nonlocal occupied_spaces  # Ensure we update the outer occupied_spaces variable
        new_data = new_data_template.copy()  # Creates the template copy
        new_data[
            'License Plate'] = license_plate  # Stores the License plate info the "License Plate" column in Vehicle.ods file
        new_data['Time'] = Character_Recognition.fetch_date_and_time()[
            1]  # Stores the time logged, fetched from Character_Recognition.py file

        # Update the 'Registered' column based on the registered vehicles list
        if license_plate in registered_vehicles:
            new_data[
                'Registered'] = 'Yes'  # Status is "Yes" if License plate info is present inside "registered_vehicles.ods" file
        else:
            new_data[
                'Registered'] = 'No'  # Status is "No" if License plate info is not present inside "registered_vehicles.ods" file

        # Debugging: Print columns to verify column names
        # print("Columns:", df.columns.tolist())

        '''
        So, another edge case to handle is that the same vehicle can enter multiple times in the same day
        To handle that, first the license plate is checked if it is already present in the column and we get the corresponding status
        If the status fetched is entry, then we updated the current status with exit
        If the status is exit, then we update the current status to entry, indicating the re-entry of the vehicle
        If the vehicle license plate info is not present in the column already, then it must be entry of the vehicle, we update the status to entry
        In all the cases, parking space "available" and "occupied" count is calculated and updated
        The same logic is reflected below in isinstance() function
        '''
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

        # Occupied_spaces and available parking spaces cannot go under 0 or above total_parking_space
        # Ensure occupied and available are within valid limits
        if occupied_spaces < 0:
            occupied_spaces = 0  # If occupied_spaces is less than 0, make it 0
        elif occupied_spaces > total_parking_space:
            occupied_spaces = total_parking_space  # If occupied_spaces is greater than total_parking_space, make it the same
            print("Parking Space is Full")  # If the parking space is fully occupied, then print the same

        # Update both occupied and avialable variable
        new_data['Occupied'] = occupied_spaces
        new_data['Available'] = total_parking_space - occupied_spaces

        # Append new data
        new_row = pd.DataFrame([new_data])
        df = pd.concat([df, new_row], ignore_index=True)

        return df

    def print_last_row(df):  # Checks if the last row is present with the data or it is empty
        if not df.empty:
            # print("\nLast row of the DataFrame:")
            print(df.iloc[-1])
        else:
            print("The DataFrame is empty.")

    # Example usage (helpful to run the file as standalone program)
    license_plate_to_search = vehicle_no
    data_existing = search_and_update(license_plate_to_search, data_existing, new_data_template, registered_vehicles)

    # Save the updated data to ODS
    data_combined = [
                        data_existing.columns.tolist()] + data_existing.values.tolist()  # New row is appended to previous row
    pyexcel_ods3.save_data(existing_file, {sheet_name: data_combined})  # File is saved and closed
    print_last_row(data_existing)  # We print the last data on the screen


if __name__ == '__main__':
    ods('Sedan', 'XYZ123')
# Helpful to run the program alone without using it as an import module for other program files
