import pandas as pd
import logging

def export_to_excel(df, photos, output_path, config):
    """
    Exports a DataFrame to an Excel file with optional formatting and a summary sheet.

    :param df: The DataFrame to export.
    :param photos: A dictionary of photo paths (optional, can be empty).
    :param output_path: The path to save the Excel file.
    :param config: Configuration dictionary for filters and settings.
    """
    try:
        with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
            # Write the main DataFrame to Excel
            df.to_excel(writer, sheet_name="Properties", index=False)

            # Access the workbook and worksheet for formatting
            workbook = writer.book
            worksheet = writer.sheets["Properties"]

            # Apply formatting
            header_format = workbook.add_format({"bold": True, "text_wrap": True, "valign": "center"})
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                worksheet.set_column(col_num, col_num, 20)  # Set column width to 20

            # Add a summary sheet
            summary_data = {
                "Statistic": ["Total Rows Processed", "Filters Applied", "Rows Excluded (Missing Address)"],
                "Value": [len(df), str(config.get("filters", {})), len(df[df["address"] == "Unknown"])]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name="Summary", index=False)

            # Format the summary sheet
            summary_worksheet = writer.sheets["Summary"]
            summary_worksheet.set_column(0, 0, 30)  # Adjust column width for readability
            summary_worksheet.set_column(1, 1, 50)

            logging.info(f"Excel file saved successfully: {output_path}")

    except Exception as e:
        logging.error(f"Error exporting to Excel: {e}", exc_info=True)
