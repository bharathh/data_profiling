# Data Quality Tools

This repository contains scripts for data profiling, data quality assessment, and synthetic data generation. The main components include:

1. **data_profile.py**: Generates a data profiling report using YData Profiling.
2. **data_quality.py**: Creates a data quality dashboard using Dash.
3. **create_data.py**: Generates synthetic datasets with options for introducing bad data to simulate real-world scenarios.
4. **config.properties**: Configuration file for setting bad data percentages for `create_data.py`.

## Prerequisites
Ensure you have python installed - https://www.python.org/downloads/


Ensure you have the required Python packages installed by installing those in the requirements file:

```bash pip install -r requirements.txt```

if you have pip3 installed

```bash pip3 install -r requirements.txt```

## Scripts Overview

1. create_data.py
This script generates synthetic datasets for various scenarios (ecommerce, medical, weather, cricket) and allows the introduction of bad data based on configurable percentages.

Usage
```bash python create_data.py <scenario> <number_of_records>```

- scenario: The type of data to generate (ecommerce, medical, weather, or cricket).
- number_of_records: The number of records to generate.

2. data_profile.py
This script generates a detailed data profiling report in HTML format.

Usage
```bash python data_profile.py <dataset_file_path>```

This command will produce an HTML file named <dataset>_profiling_report.html.


3. This script creates a data quality dashboard using Dash. It displays various data quality metrics such as completeness, duplicates, uniqueness, accuracy, timeliness, and validity.

```bash python data_quality.py <dataset_file_path> <config_path>```

- file_path: The path to the CSV file to be analyzed.
- config_path: The path to the configuration file (JSON) for service level objectives (SLOs).

Navigate to http://127.0.0.1:8050/ to view the dashboard.
