# Import necessary libraries
import pandas as pd
from ydata_profiling import ProfileReport
import argparse
import os

# Setup argument parser
parser = argparse.ArgumentParser(description="Generate a data profiling report using YData Profiling.")
parser.add_argument('file_path', type=str, help='The path to the CSV file to be profiled')

# Parse the arguments
args = parser.parse_args()

# Check if the file exists
if not os.path.exists(args.file_path):
    print(f"Error: The file {args.file_path} does not exist.")
    exit(1)

# Load the dataset
df = pd.read_csv(args.file_path)

# Generate the profiling report
profile = ProfileReport(df, title="Data Profiling Report", explorative=True)

# Create an output file name based on the input file name
output_file_name = os.path.splitext(os.path.basename(args.file_path))[0] + "_profiling_report.html"

# Save the report as an HTML file
profile.to_file(output_file_name)

print(f"Profiling report generated and saved as '{output_file_name}'.")
