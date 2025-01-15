import pytesseract

# Full path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\MargaretHawkins\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

import pandas as pd
import pdfplumber
from pytesseract import image_to_string
from PIL import Image
import logging
import re

def extract_from_excel(file_path, header=0):
    """
    Extracts data from an Excel file using pandas.

    :param file_path: The path to the Excel file.
    :param header: The row to use as the header (default is the first row, 0-indexed).
    :return: A pandas DataFrame with the extracted data.
    """
    try:
        df = pd.read_excel(file_path, header=header, engine='openpyxl')  # Specify the header row
        return df
    except Exception as e:
        print(f"Error extracting data from Excel file {file_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure

def extract_from_pdf(file_path):
    """
    Extracts data from a PDF file and maps it to the specified fields.

    :param file_path: Path to the PDF file.
    :return: A pandas DataFrame with parsed property data.
    """
    logging.info(f"Extracting data from PDF: {file_path}")
    parsed_data = []

    # Fields to extract
    fields = {
        "building_photo": None,
        "address": r"Address:\s*(.+)",
        "property_name": r"Property Name:\s*(.+)",
        "city": r"City:\s*(.+)",
        "zip_code": r"ZIP Code:\s*(\d+)",
        "total_building_sf": r"Total Building SF:\s*(\d+)",
        "sf_available": r"SF Available:\s*(\d+)",
        "monthly_asking_rent": r"Monthly Asking Rent \$/SF:\s*(\d+\.\d+)",
        "monthly_operating_expenses": r"Monthly Operating Expenses:\s*(\d+\.\d+)",
        "monthly_asking_gross": r"Monthly Asking Gross \$/SF:\s*(\d+\.\d+)",
        "annual_asking_gross": r"Annual Asking Gross \$/SF:\s*(\d+\.\d+)",
        "asking_monthly_rent": r"Asking Monthly Rent:\s*(\d+\.\d+)",
        "asking_annual_rent": r"Asking Annual Rent:\s*(\d+\.\d+)",
        "rent_type": r"Rent Type:\s*(.+)",
        "parking_ratio": r"Parking Ratio / 1,000 SF:\s*(\d+\.\d+)",
        "tia": r"TIA \(\$/SF/Yr\):\s*(\d+\.\d+)",
        "total_parking_spaces": r"Total # of Parking Spaces:\s*(\d+)",
        "building_class": r"Building Class:\s*(.+)",
        "year_built": r"Year Built:\s*(\d+)",
        "notes": r"Notes:\s*(.+)"
    }

    try:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                raw_text = page.extract_text()
                if raw_text:
                    # Extract data for each field
                    extracted_row = {}
                    for field, pattern in fields.items():
                        if pattern:
                            match = re.search(pattern, raw_text)
                            extracted_row[field] = match.group(1).strip() if match else "N/A"
                        else:
                            extracted_row[field] = "N/A"  # Placeholder for fields like photos
                    extracted_row["source_page"] = page_num + 1  # Optional: Track the page number
                    parsed_data.append(extracted_row)
                else:
                    logging.warning(f"No text found on page {page_num + 1} of {file_path}")

        if parsed_data:
            return pd.DataFrame(parsed_data)
        else:
            logging.warning(f"No data extracted from PDF: {file_path}")
            return pd.DataFrame()  # Return an empty DataFrame if no data was parsed

    except Exception as e:
        logging.error(f"Failed to extract data from PDF {file_path}: {e}", exc_info=True)
        return pd.DataFrame()  # Return an empty DataFrame if an error occurs

def extract_from_image(file_path):
    """
    Extracts text from an image file.
    :param file_path: Path to the image file.
    :return: Extracted text as a string.
    """
    img = Image.open(file_path)
    return image_to_string(img)
