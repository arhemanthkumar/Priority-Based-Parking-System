import pandas as pd
import pyexcel_ods3
import json
import plotly
import plotly.graph_objs as go
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


def read_vehicle_data():
    ods_file = 'Vehicle.ods'
    data = pyexcel_ods3.get_data(ods_file)
    sheet_name = list(data.keys())[0]
    data_list = data[sheet_name]
    columns = data_list[0]
    df = pd.DataFrame(data_list[1:], columns=columns)
    df['Date_Time'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%y %I:%M %p')
    return df


def create_line_graph(df):
    line_graph = go.Figure()
    line_graph.add_trace(
        go.Scatter(x=df['Date_Time'], y=df['Occupied'], mode='lines+markers', name='Occupied', line=dict(color='blue')))
    line_graph.add_trace(go.Scatter(x=df['Date_Time'], y=df['Available'], mode='lines+markers', name='Available',
                                    line=dict(color='orange')))
    line_graph.update_layout(title={'text': 'Parking Space', 'x': 0.5}, xaxis_title='Time',
                             yaxis_title='Count')
    graphJSON = json.dumps(line_graph, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def create_pie_chart(df):
    vehicle_counts = df['Vehicle Class'].value_counts()
    pie_chart = go.Figure(data=[go.Pie(labels=vehicle_counts.index, values=vehicle_counts.values)])
    pie_chart.update_layout(title={'text': 'Vehicle Class Distribution', 'x': 0.5})
    pie_chart_JSON = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)
    return pie_chart_JSON


def find_peak_time(df):
    max_occupied_time = df.loc[df['Occupied'].idxmax()]['Date_Time']
    return max_occupied_time


@app.route('/')
def index():
    df = read_vehicle_data()
    line_graph = create_line_graph(df)
    pie_chart = create_pie_chart(df)

    # Calculate the total vehicle count (currently parked vehicles)
    total_vehicle_count = df[df['Status'] == 'Entry'].shape[0] - df[df['Status'] == 'Exit'].shape[0]

    # Find peak time for maximum occupied count
    peak_time = find_peak_time(df)

    return render_template('index.html', graphJSON=line_graph, pie_chart_JSON=pie_chart,
                           total_vehicle_count=total_vehicle_count,
                           peak_time=peak_time)


if __name__ == '__main__':
    app.run(debug=True)
