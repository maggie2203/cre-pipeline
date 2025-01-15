import pandas as pd
from app.data_export import export_to_excel

# Step 1: Create the DataFrame with all required columns
data = {
    "City": ["City A", "City B", "City C"],
    "Zip Code": ["12345", "67890", "54321"],
    "Total Building SF": [10000, 20000, 15000],
    "SF Available": [5000, 10000, 7500],
    "Monthly Asking Rent $/SF": [2.5, 2.0, 2.8],
    "Monthly Operating Expenses": [1.0, 1.2, 1.1],
    "Monthly Asking Gross $/SF": [3.5, 3.2, 3.9],
    "Annual Asking Gross $/SF": [42.0, 38.4, 46.8],
    "Asking Monthly Rent": [12500, 20000, 21000],
    "Asking Annual Rent": [150000, 240000, 252000],
    "Rent Type": ["NNN", "Gross", "NNN"],
    "Parking Ratio / 1,000 SF": [4, 3, 5],
    "TIA ($/SF/Yr)": [10.0, 12.0, 8.0],
    "Total # of Parking Spaces": [40, 60, 75],
    "Build Class": ["A", "B", "C"],
    "Year Built": [1990, 2000, 1985],
    "Notes": ["Prime location", "Newly renovated", "Great visibility"],
    "Photo Path": ["photo1.png", "photo2.png", "photo3.png"] 
}

# Create the DataFrame
df = pd.DataFrame(data)

# Step 2: Generate the photos dictionary
# This maps the row index to the corresponding photo path
photos = {index: row["Photo Path"] for index, row in df.iterrows()}

# Step 3: Export the DataFrame to Excel (excluding the "Photo Path" column)
output_path = "test_output_with_full_columns.xlsx"
export_to_excel(df.drop(columns=["Photo Path"]), photos, output_path)

print(f"Excel file created: {output_path}")
