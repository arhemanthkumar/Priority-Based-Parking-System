from datetime import datetime

# Define two time strings in AM/PM format
time_str1 = '08:34 AM'
time_str2 = '12:11 PM'

# Convert time strings to datetime objects
time_format = '%I:%M %p'
time1 = datetime.strptime(time_str1, time_format)
time2 = datetime.strptime(time_str2, time_format)

# Calculate the difference
time_difference = time2 - time1

# Output the difference
print('Time Difference:', time_difference)
print('Total seconds:', time_difference.total_seconds())
