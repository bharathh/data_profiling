import pandas as pd
import random
from faker import Faker
import sys
import configparser

# Initialize Faker and set seed for reproducibility
fake = Faker()
Faker.seed(0)
random.seed(0)

# Read configuration from properties file
config = configparser.ConfigParser()
config.read('config.properties')

# Default bad data percentages
default_bad_data_percentage = {
    "freshness": 10,
    "completeness": 10,
    "duplicates": 10,
    "invalidity": 10,
    "consistency": 10,
    "accuracy": 10
}

# Load bad data percentages from configuration file
bad_data_percentage = {key: int(config.get('DEFAULT', key, fallback=default_bad_data_percentage[key]))
                       for key in default_bad_data_percentage}

# Function to introduce bad data based on the percentage
def introduce_bad_data(data, bad_type, percentage):
    num_bad_rows = int(len(data) * percentage / 100)
    if bad_type == "freshness":
        # Introduce some old dates to simulate stale data
        old_date = fake.date_between(start_date="-3y", end_date="-1y")
        data.loc[data.sample(num_bad_rows).index, 'Date_Created'] = old_date
    elif bad_type == "completeness":
        # Remove random fields to simulate missing data
        for col in data.columns:
            if col != 'Ticket_ID':  # Avoid changing primary key
                data.loc[data.sample(num_bad_rows).index, col] = None
    elif bad_type == "duplicates":
        # Introduce duplicate records
        duplicates = data.sample(num_bad_rows)
        data = pd.concat([data, duplicates])
        data.reset_index(drop=True, inplace=True)  # Reset index after adding duplicates
    elif bad_type == "invalidity":
        # Introduce random invalid data
        data.loc[data.sample(num_bad_rows).index, 'Priority'] = "Invalid"
    elif bad_type == "consistency":
        # Change formats or introduce inconsistency (e.g., date formats)
        inconsistent_date = fake.date_between(start_date="-3y", end_date="today").strftime('%d-%m-%Y')
        data.loc[data.sample(num_bad_rows).index, 'Date_Created'] = inconsistent_date
    elif bad_type == "accuracy":
        # Change data types or introduce wrong values
        data.loc[data.sample(num_bad_rows).index, 'Resolution_Time'] = fake.text()

    return data

# Function to generate different types of datasets
def generate_scenario_data(scenario, num_records):
    data = []

    if scenario == "ecommerce":
        for _ in range(num_records):
            data.append({
                "Transaction_ID": fake.uuid4(),
                "Customer_Name": fake.name(),
                "Item": random.choice(['Laptop', 'Phone', 'Tablet', 'Headphones']),
                "Amount": round(random.uniform(50.5, 999.99), 2),
                "Date_Created": fake.date_between(start_date="-1y", end_date="today"),
                "Status": random.choice(['Completed', 'Pending', 'Cancelled']),
                "Priority": random.choice(['Low', 'Medium', 'High']),
                "Resolution_Time": f"{random.randint(1, 10)} days"
            })

    elif scenario == "medical":
        for _ in range(num_records):
            data.append({
                "Patient_ID": fake.uuid4(),
                "Name": fake.name(),
                "Age": random.randint(1, 100),
                "Diagnosis": random.choice(['Flu', 'Covid-19', 'Diabetes', 'Hypertension']),
                "Date_Created": fake.date_between(start_date="-1y", end_date="today"),
                "Doctor": fake.name(),
                "Status": random.choice(['Treated', 'Ongoing', 'Discharged']),
                "Priority": random.choice(['Low', 'Medium', 'High']),
                "Resolution_Time": f"{random.randint(1, 20)} days"
            })

    elif scenario == "weather":
        for _ in range(num_records):
            data.append({
                "Record_ID": fake.uuid4(),
                "Location": fake.city(),
                "Temperature": round(random.uniform(-30, 50), 2),
                "Humidity": random.randint(10, 100),
                "Date_Created": fake.date_between(start_date="-1y", end_date="today"),
                "Condition": random.choice(['Sunny', 'Rainy', 'Snowy', 'Cloudy']),
                "Status": random.choice(['Reported', 'Forecast']),
                "Priority": random.choice(['Low', 'Medium', 'High']),
                "Resolution_Time": f"{random.randint(1, 3)} days"
            })

    elif scenario == "cricket":
        for _ in range(num_records):
            data.append({
                "Player_ID": fake.uuid4(),
                "Name": fake.name(),
                "Matches": random.randint(1, 200),
                "Runs": random.randint(0, 15000),
                "Date_Created": fake.date_between(start_date="-20y", end_date="today"),
                "Team": random.choice(['India', 'Australia', 'England', 'South Africa']),
                "Status": random.choice(['Active', 'Retired']),
                "Priority": random.choice(['Low', 'Medium', 'High']),
                "Resolution_Time": f"{random.randint(1, 5)} hours"
            })

    df = pd.DataFrame(data)

    # Introduce bad data as per configurations
    for bad_type, percentage in bad_data_percentage.items():
        df = introduce_bad_data(df, bad_type, percentage)

    return df

if __name__ == "__main__":
    # Read scenario and number of records from command line argument
    if len(sys.argv) < 3:
        print("Usage: python generate_test_data.py <scenario> <number_of_records>")
        sys.exit(1)

    scenario = sys.argv[1]
    try:
        num_records = int(sys.argv[2])
    except ValueError:
        print("Please enter a valid integer for the number of records.")
        sys.exit(1)

    # Validate scenario
    valid_scenarios = ["ecommerce", "medical", "weather", "cricket"]
    if scenario not in valid_scenarios:
        print(f"Invalid scenario! Choose from {valid_scenarios}")
        sys.exit(1)

    # Generate data based on the scenario
    df_scenario_data = generate_scenario_data(scenario, num_records)

    # Save the dataset to a CSV file
    output_file = f'{scenario}_data.csv'
    df_scenario_data.to_csv(output_file, index=False)
    print(f"Generated {scenario} dataset with {num_records} records and saved to '{output_file}'.")
