import pandas as pd
from app.data_cleaning import deduplicate_data, standardize_columns, fill_missing_values

# Sample data for testing
data = {
    'Property Name': ['Building A', 'Building B', 'Building A', 'Building C'],
    'Address': ['123 Main St', '456 Elm St', '123 Main St', '789 Oak Ave'],
    'Square Feet': [5000, 3200, 5000, None]
}

# Create a DataFrame
df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)

# Test deduplication
df_deduplicated = deduplicate_data(df, 'Property Name')
print("\nDeduplicated DataFrame:")
print(df_deduplicated)

# Test column standardization
df_standardized = standardize_columns(df)
print("\nStandardized Columns DataFrame:")
print(df_standardized)

# Test filling missing values
column_defaults = {'Square Feet': 0}
df_filled = fill_missing_values(df_standardized, column_defaults)
print("\nFilled Missing Values DataFrame:")
print(df_filled)
