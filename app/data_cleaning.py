import pandas as pd

def deduplicate_data(dataframe, key_column):
    """
    Removes duplicate rows from the DataFrame based on a specific column.
    :param dataframe: The pandas DataFrame to deduplicate.
    :param key_column: The column to check for duplicates.
    :return: A deduplicated pandas DataFrame.
    """
    return dataframe.drop_duplicates(subset=[key_column])

def standardize_columns(dataframe):
    """
    Standardizes column names by converting them to lowercase and replacing spaces with underscores.
    :param dataframe: The pandas DataFrame to standardize.
    :return: A DataFrame with standardized column names.
    """
    dataframe.columns = dataframe.columns.str.lower().str.replace(' ', '_')
    return dataframe

def fill_missing_values(dataframe, column_defaults):
    """
    Fills missing values in the specified columns with default values.
    :param dataframe: The pandas DataFrame to process.
    :param column_defaults: A dictionary with column names as keys and default values as values.
    :return: A DataFrame with missing values filled.
    """
    for column, default in column_defaults.items():
        if column in dataframe.columns:
            dataframe[column] = dataframe[column].fillna(default)
    return dataframe
