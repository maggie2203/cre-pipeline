import os
import json
import pandas as pd
import logging
from datetime import datetime
from app.data_extraction import extract_from_excel, extract_from_pdf, extract_from_image
from app.data_cleaning import deduplicate_data, fill_missing_values
from app.data_export import export_to_excel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("process_surveys.log", mode="a"), logging.StreamHandler()]
)

# Load configuration
try:
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    logging.critical("Configuration file 'config.json' not found. Please ensure it is in the correct directory.")
    exit(1)
except json.JSONDecodeError as e:
    logging.critical(f"Error decoding 'config.json': {e}")
    exit(1)

photo_folder = config["photo_folder"]
output_folder = config["output_folder"]
column_defaults = config["default_values"]
supported_formats = config["supported_formats"]

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

def apply_filters(df, filters):
    """
    Filters the DataFrame based on the criteria in filters.

    :param df: The consolidated DataFrame.
    :param filters: A dictionary of filtering criteria.
    :return: Filtered DataFrame.
    """
    logging.info("Applying filters to the data...")

    if "city" in filters and filters["city"]:
        df = df[df["city"].isin(filters["city"])]

    if "building_class" in filters and filters["building_class"]:
        df = df[df["building_class"].isin(filters["building_class"])]

    if "monthly_rent_min" in filters:
        df = df[df["asking_monthly_rent"] >= filters["monthly_rent_min"]]

    if "monthly_rent_max" in filters:
        df = df[df["asking_monthly_rent"] <= filters["monthly_rent_max"]]

    logging.info(f"Filtered data contains {len(df)} rows after applying filters.")
    return df

def process_surveys(file_paths, output_excel):
    """
    Processes uploaded CRE surveys and generates consolidated outputs.

    :param file_paths: List of file paths for uploaded surveys.
    :param output_excel: Path for the output Excel file.
    """
    consolidated_data = []

    # Step 1: Extract Data
    for file_path in file_paths:
        logging.info(f"Starting processing for file: {file_path}")
        try:
            if any(file_path.endswith(ext) for ext in supported_formats):
                if file_path.endswith('.xlsx'):
                    data = extract_from_excel(file_path, header=0)
                elif file_path.endswith('.pdf'):
                    data = extract_from_pdf(file_path)
                elif file_path.endswith(('.png', '.jpg', '.jpeg')):
                    data = extract_from_image(file_path)
                else:
                    logging.warning(f"Skipping unsupported file format: {file_path}")
                    continue

                if isinstance(data, pd.DataFrame) and not data.empty:
                    consolidated_data.append(data)
                    logging.info(f"Successfully extracted data from {file_path}: {len(data)} rows.")
                else:
                    logging.warning(f"No data extracted from: {file_path}")
            else:
                logging.warning(f"Skipping unsupported file format: {file_path}")
        except Exception as e:
            logging.error(f"Error processing file {file_path}: {e}", exc_info=True)

    # Combine all extracted data into a single DataFrame
    if consolidated_data:
        df = pd.concat(consolidated_data, ignore_index=True)
        logging.info(f"Total rows in combined DataFrame: {len(df)}")
    else:
        logging.error("No valid data extracted from the provided files.")
        return

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    logging.info(f"Standardized Column Names: {df.columns.tolist()}")

    # Handle missing 'asking_monthly_rent' column
    if "asking_monthly_rent" not in df.columns:
        logging.warning("'asking_monthly_rent' column not found. Adding default values.")
        df["asking_monthly_rent"] = 0  # Default value

    # Sample data for debugging
    logging.info(f"Sample data:\n{df.head()}")

    # Step 2: Deduplicate Data
    if 'address' in df.columns:
        df = deduplicate_data(df, 'address')
        logging.info("Deduplicated data based on the 'address' column.")
    else:
        logging.warning("'address' column not found. Skipping deduplication.")

    # Step 3: Fill Missing Values
    df = fill_missing_values(df, column_defaults)
    logging.info("Filled missing values with default data.")

    # Step 4: Remove Rows with 'Unknown'
    if "address" in df.columns:
        initial_row_count = len(df)
        df = df[df["address"] != "Unknown"]
        removed_rows = initial_row_count - len(df)
        logging.info(f"Removed {removed_rows} rows with missing addresses.")

    if "city" in df.columns:
        initial_row_count = len(df)
        df = df[df["city"] != "Unknown"]
        removed_rows = initial_row_count - len(df)
        logging.info(f"Removed {removed_rows} rows with missing cities.")

    # Step 5: Apply Filters
    df = apply_filters(df, config.get("filters", {}))

    # Step 6: Export to Excel
    try:
        export_to_excel(df, {}, output_excel, config)
        if os.path.exists(output_excel) and os.path.getsize(output_excel) > 0:
            logging.info(f"Output file {output_excel} created successfully.")
        else:
            logging.error(f"Output file {output_excel} is empty or missing!")
    except Exception as e:
        logging.error(f"Failed to export data to Excel: {e}", exc_info=True)

# Example usage
if __name__ == "__main__":
    survey_files = [
        "example_survey1.xlsx",
        "example_survey2.pdf",
        "example_image1.png"
    ]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_excel = os.path.join(output_folder, f"consolidated_properties_{timestamp}.xlsx")

    try:
        process_surveys(
            file_paths=survey_files,
            output_excel=output_excel
        )
    except Exception as e:
        logging.critical(f"Critical error occurred: {e}", exc_info=True)



