import os
import json
import pandas as pd
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("process_surveys.log", mode="a"), logging.StreamHandler()]
)

def process_surveys(file_paths, output_excel):
    """
    Processes uploaded CRE surveys and generates consolidated outputs.
    """
    consolidated_data = []

    # Extract data from uploaded files
    for file_path in file_paths:
        logging.info(f"Processing file: {file_path}")
        try:
            if file_path.endswith('.xlsx'):
                data = pd.read_excel(file_path)
            else:
                logging.warning(f"Unsupported file type: {file_path}")
                continue

            if isinstance(data, pd.DataFrame) and not data.empty:
                consolidated_data.append(data)
                logging.info(f"Successfully processed {file_path}, rows: {len(data)}")
            else:
                logging.warning(f"No valid data found in {file_path}")

        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}", exc_info=True)

    # Combine data
    if consolidated_data:
        df = pd.concat(consolidated_data, ignore_index=True)
        logging.info("Data combined successfully.")
    else:
        logging.error("No valid data extracted.")
        return

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    logging.info(f"Standardized columns: {df.columns.tolist()}")  # Log all column names

    # Debug missing columns
    if "building_class" not in df.columns:
        logging.warning("'building_class' column not found in the file. Adding default values.")
        df["building_class"] = "Unknown"  # Default value

    # Save to Excel
    try:
        df.to_excel(output_excel, index=False)
        logging.info(f"Output saved to {output_excel}")
    except Exception as e:
        logging.error(f"Failed to save output: {e}", exc_info=True)

# Example usage
if __name__ == "__main__":
    input_files = [
        "example_survey1.xlsx",
        "example_survey2.xlsx"
    ]

    output_file = os.path.join("output", f"consolidated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")

    os.makedirs("output", exist_ok=True)

    process_surveys(input_files, output_file)