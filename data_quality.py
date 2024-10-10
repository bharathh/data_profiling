import pandas as pd
import json
from dash import Dash, html, dcc
import plotly.graph_objs as go
import argparse
import os
from datetime import datetime

# Function to calculate completeness (percentage of non-missing values)
def calculate_completeness(df):
    missing_data_percentage = df.isnull().sum() * 100 / len(df)
    completeness = 100 - missing_data_percentage.mean()  # Average completeness across all columns
    return completeness

# Function to calculate duplicates (percentage of duplicate rows)
def calculate_duplicates(df):
    num_duplicates = df.duplicated().sum()
    duplicates_percentage = (num_duplicates / len(df)) * 100
    return duplicates_percentage

# Function to calculate uniqueness (percentage of unique rows)
def calculate_uniqueness(df):
    num_unique_rows = df.drop_duplicates().shape[0]
    uniqueness_percentage = (num_unique_rows / len(df)) * 100
    return uniqueness_percentage

# Placeholder function for accuracy (to be defined based on dataset specifics)
def calculate_accuracy(df):
    # This is dataset-specific, you would calculate it based on known correct values.
    # Placeholder: assuming 98% accuracy for this example
    accuracy_percentage = 98
    return accuracy_percentage

# Function to check timeliness (assume there's a date column named 'timestamp')
def check_timeliness(df, slo_config):
    if 'timestamp' in df.columns:
        current_date = datetime.now()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        max_delay = slo_config['timeliness']['max_delay']
        max_timestamp = df['timestamp'].max()
        delay_in_days = (current_date - max_timestamp).days
        return delay_in_days <= max_delay
    return True

# Placeholder function for validity (to be defined based on dataset-specific rules)
def calculate_validity(df):
    # Placeholder validity calculation: assume 90% validity
    validity_percentage = 90
    return validity_percentage

# Setup argument parser
parser = argparse.ArgumentParser(description="Generate a data quality dashboard using Dash.")
parser.add_argument('file_path', type=str, help='The path to the CSV file to be profiled')
parser.add_argument('config_path', type=str, help='The path to the configuration file (JSON) for SLOs')

# Parse the arguments
args = parser.parse_args()

# Check if the file exists
if not os.path.exists(args.file_path):
    print(f"Error: The file {args.file_path} does not exist.")
    exit(1)

# Load the dataset
df = pd.read_csv(args.file_path)

# Load the SLO configuration file
with open(args.config_path, 'r') as config_file:
    slo_config = json.load(config_file)

# Calculate the metrics
completeness = calculate_completeness(df)
duplicates = calculate_duplicates(df)
uniqueness = calculate_uniqueness(df)
accuracy = calculate_accuracy(df)
timeliness = check_timeliness(df, slo_config)
validity = calculate_validity(df)

# Compare with SLOs
completeness_warning = completeness < slo_config['completeness']['min_threshold']
duplicates_warning = duplicates > slo_config['duplicates']['max_threshold']
uniqueness_warning = uniqueness < slo_config['uniqueness']['min_threshold']
timeliness_warning = not timeliness
accuracy_warning = accuracy < slo_config['accuracy']['min_threshold']
validity_warning = validity < slo_config['validity']['min_threshold']

# Prepare the dashboard
app = Dash(__name__)

# Define data for indicators
indicators = [
    {
        'metric': 'Completeness',
        'value': completeness,
        'threshold': slo_config['completeness']['min_threshold'],
        'warning': completeness_warning
    },
    {
        'metric': 'Duplicates',
        'value': duplicates,
        'threshold': slo_config['duplicates']['max_threshold'],
        'warning': duplicates_warning
    },
    {
        'metric': 'Uniqueness',
        'value': uniqueness,
        'threshold': slo_config['uniqueness']['min_threshold'],
        'warning': uniqueness_warning
    },
    {
        'metric': 'Timeliness',
        'value': "OK" if timeliness else "Exceeded",
        'threshold': slo_config['timeliness']['max_delay'],
        'warning': timeliness_warning
    },
    {
        'metric': 'Accuracy',
        'value': accuracy,
        'threshold': slo_config['accuracy']['min_threshold'],
        'warning': accuracy_warning
    },
    {
        'metric': 'Validity',
        'value': validity,
        'threshold': slo_config['validity']['min_threshold'],
        'warning': validity_warning
    }
]

# Dashboard layout
app.layout = html.Div(children=[
    html.H1(children='Data Quality Dashboard'),
    html.Div(children=[
        html.Div(
            dcc.Graph(
                id=f'{item["metric"].lower()}-gauge',
                figure=go.Figure(
                    go.Indicator(
                        mode="gauge+number+delta",
                        value=item['value'] if isinstance(item['value'], (int, float)) else 0,
                        title={'text': item['metric']},
                        delta={'reference': item['threshold'], 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
                        gauge={
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "red" if item['warning'] else "green"},
                            'steps': [
                                {'range': [0, item['threshold']], 'color': "lightgray"},
                                {'range': [item['threshold'], 100], 'color': "lightgreen"}
                            ],
                        }
                    )
                )
            ),
            style={'width': '32%', 'display': 'inline-block'}
        )
        for item in indicators
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
