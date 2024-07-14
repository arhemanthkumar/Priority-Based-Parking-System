from flask import Flask, render_template  # imports Flask class and render_template function from flask module
import pandas as pd  # imports pandas module for data operations inside Vehicle.ods file
import pyexcel_ods3  # imports pyexcel_ods3 module for reading ODS files, as the format is in ods instead of xls
import json  # imports json module for JSON operations
import plotly  # imports plotly module for creating interactive plots
import plotly.graph_objs as go  # imports graph objects from plotly for creating plot elements, which makes the graph interactive
from datetime import datetime  # Imports datetime module for date and time manipulation

app = Flask(__name__)  # Creates an instance of the Flask class

def read_vehicle_data():
    ods_file = 'Vehicle.ods'  # Path to the ODS file containing vehicle data
    data = pyexcel_ods3.get_data(ods_file)  # Reads data from the ODS file
    sheet_name = list(data.keys())[0]  # Gets the name of the first sheet, assuming it is the 1st sheet
    data_list = data[sheet_name]  # Extracts data from the first sheet
    columns = data_list[0]  # Extracts column names
    df = pd.DataFrame(data_list[1:], columns=columns)  # Creates a DataFrame with the data

    # Remove rows with empty 'Date' or 'Time' fields as the Json error may appear if these fields are empty
    df = df[df['Date'].str.strip().astype(bool) & df['Time'].str.strip().astype(bool)]

    # Convert 'Date' and 'Time' columns to a single 'Date_Time' column of datetime type
    df['Date_Time'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%y %I:%M %p', errors='coerce')

    # Remove rows where 'Date_Time' conversion failed (invalid date/time format)
    df = df.dropna(subset=['Date_Time'])

    return df  # Returns the cleaned DataFrame

def read_registered_vehicles():
    registered_file = 'registered_vehicles.ods'  # Path to the ODS file containing registered vehicle data
    registered_data = pyexcel_ods3.get_data(registered_file)  # Reads data from the ODS file
    registered_sheet_name = list(registered_data.keys())[0]  # Gets the name of the first sheet, assuming it is the 1st sheet
    registered_list = registered_data[registered_sheet_name]  # Extracts data from the first sheet
    return len(registered_list) - 1  # Subtracting 1 to exclude the header row

def create_line_graph(df):
    line_graph = go.Figure()  # Creates a new Plotly figure for the line graph
    # Adds a trace for occupied parking spaces
    line_graph.add_trace(
        go.Scatter(x=df['Date_Time'], y=df['Occupied'], mode='lines+markers', name='Occupied', line=dict(color='blue')))
    # Adds a trace for available parking spaces
    line_graph.add_trace(
        go.Scatter(x=df['Date_Time'], y=df['Available'], mode='lines+markers', name='Available', line=dict(color='orange')))
    # Updates layout of the graph with titles
    line_graph.update_layout(title={'text': 'Vehicle Movement Analysis', 'x': 0.5}, xaxis_title='Time', yaxis_title='Count')
    # Converts the graph to JSON format for rendering in the template
    graphJSON = json.dumps(line_graph, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON  # Returns the JSON-encoded graph

def create_pie_chart(df):
    vehicle_counts = df['Vehicle Class'].value_counts()  # Counts occurrences of each vehicle class
    # Creates a pie chart with the vehicle class distribution
    pie_chart = go.Figure(data=[go.Pie(labels=vehicle_counts.index, values=vehicle_counts.values)])
    # Updates layout of the pie chart with a title
    pie_chart.update_layout(title={'text': 'Vehicle Class Distribution', 'x': 0.5})
    # Converts the pie chart to JSON format for rendering in the template
    pie_chart_JSON = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)
    return pie_chart_JSON  # Returns the JSON-encoded pie chart

@app.route('/')  # Defines the route for the home page
def index():
    df = read_vehicle_data()  # Reads vehicle data from the ODS file
    line_graph = create_line_graph(df)  # Creates the line graph for parking space occupancy chart
    pie_chart = create_pie_chart(df)  # Creates the pie chart for vehicle class classification

    # Calculate the total vehicle count (currently parked vehicles)
    total_vehicle_count = df[df['Status'] == 'Entry'].shape[0] - df[df['Status'] == 'Exit'].shape[0]

    # Calculate the peak time (time when the occupied count was maximum)
    peak_time_row = df.loc[df['Occupied'].idxmax()]  # Finds the row with the maximum occupied count
    peak_time = peak_time_row['Date_Time']  # Extracts the peak time
    peak_occupied = peak_time_row['Occupied']  # Extracts the peak occupied count

    registered_vehicle_count = read_registered_vehicles()  # Reads the count of registered vehicles

    # Renders the index.html template with the generated graphs and statistics
    return render_template('index.html',
                           graphJSON=line_graph,
                           pie_chart_JSON=pie_chart,
                           total_vehicle_count=total_vehicle_count,
                           peak_time=peak_time,
                           peak_occupied=peak_occupied,
                           registered_vehicle_count=registered_vehicle_count)

if __name__ == '__main__':  # Ensures the app runs only if this script is executed directly
    app.run(debug=True)  # Runs the Flask app in debug mode
