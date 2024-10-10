import pandas as pd
import sys
import great_expectations as ge

# Function to generate data profiling report using ydata-profiling
def define_expectations(gedf):
    
    gedf.expect_column_values_to_not_be_null('')
    gedf.expect_column_to_exist('')
    gedf.expect_column_values_to_be_between('col_name', min, max)
    gedf.expect_column_values_to_match_regex('col_name', 'regex')
    gedf.expect_column_values_to_be_in_set('col_name', ['col_value1', 'col_value2'])

    return gedf

# Function to display a Streamlit dashboard
def create_dashboard(validation_results, df):
    st.title("Data Quality Dashboard")
    
    # Display data summary
    st.header("Dataset Overview")
    st.write(df.head())

    # Display validation results from Great Expectations
    st.header("Data Quality Validation")
    for result in validation_results['results']:
        st.write(f"Expectation: {result['expectation_config']['expectation_type']}")
        st.write(f"Success: {result['success']}")
        st.write(f"Details: {result['result']}")

# Main script logic
def main():
    if len(sys.argv) < 2:
        print("Usage: python data_quality_dashboard.py <data_file>")
        sys.exit(1)

    data_file = sys.argv[1]

    # Load dataset
    df = pd.read_csv(data_file)

    context = ge.get_context()
    

    # Set data expecations
    gedf = define_expectations(ge.dataset.PandasDataset(df))

    # Perform data validation
    validation_results = gedf.validate()

    # Create and display dashboard
    create_dashboard(validation_results, df)

if __name__ == "__main__":
    main()
