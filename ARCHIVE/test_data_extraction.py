from app.data_extraction import extract_from_excel, extract_from_pdf, extract_from_image

# Replace these with actual file paths
excel_file = "test_data.xlsx"  # Path to an Excel file (create a simple test file if needed)
pdf_file = "test_data.pdf"     # Path to a PDF file with text
image_file = "test_image.png"  # Path to an image with clear text

# Test Excel extraction
try:
    print("Testing Excel Extraction...")
    excel_data = extract_from_excel(excel_file)
    print("Extracted Excel Data:")
    print(excel_data)
except Exception as e:
    print(f"Excel Extraction Error: {e}")

# Test PDF extraction
try:
    print("\nTesting PDF Extraction...")
    pdf_text = extract_from_pdf(pdf_file)
    print("Extracted PDF Text:")
    print(pdf_text)
except Exception as e:
    print(f"PDF Extraction Error: {e}")

# Test Image extraction
try:
    print("\nTesting Image Extraction...")
    image_text = extract_from_image(image_file)
    print("Extracted Image Text:")
    print(image_text)
except Exception as e:
    print(f"Image Extraction Error: {e}")

if isinstance(data, pd.DataFrame) and not data.empty:
    logging.info(f"Extracted data from {file_path}: {data.head()}")
else:
    logging.warning(f"No data extracted from: {file_path}")

