
from flask import Flask, request, jsonify
import os
import logging
from process_surveys import process_surveys

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("api_wrapper.log", mode="a"), logging.StreamHandler()]
)

# Ensure temporary and output directories exist
temp_dir = "temp_uploads"
output_dir = "output"
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

@app.route("/process", methods=["POST"])
def process():
    """
    API endpoint to process uploaded files.
    Expects files to be sent as a POST request with the key 'files'.
    """
    try:
        # Log request for debugging
        logging.info("Received a request to /process")

        # Retrieve files from the request
        files = request.files.getlist("files")
        logging.info(f"Files in request: {[file.filename for file in files]}")

        if not files or all(file.filename == '' for file in files):
            logging.warning("No files uploaded or filenames are empty.")
            return jsonify({"status": "error", "message": "No files uploaded."}), 400

        # Save files to a temporary directory
        file_paths = []
        for file in files:
            if file and file.filename:  # Ensure file is valid
                temp_path = os.path.join(temp_dir, file.filename)
                file.save(temp_path)
                file_paths.append(temp_path)
                logging.info(f"Saved uploaded file to: {temp_path}")
            else:
                logging.warning(f"Skipped invalid or empty file: {file}")

        if not file_paths:
            return jsonify({"status": "error", "message": "No valid files uploaded."}), 400

        # Generate the output Excel file path
        output_excel = os.path.join(output_dir, "consolidated_properties.xlsx")

        # Run the pipeline
        process_surveys(file_paths, output_excel)

        # Return the result
        if os.path.exists(output_excel):
            logging.info(f"Output file created: {output_excel}")
            return jsonify({"status": "success", "output_file": output_excel}), 200
        else:
            logging.error("Output file not found after processing.")
            return jsonify({"status": "error", "message": "Processing failed. No output file created."}), 500

    except Exception as e:
        logging.error(f"Error in processing: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
