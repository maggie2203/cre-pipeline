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
        # Retrieve files from the request
        files = request.files.getlist("files")
        if not files:
            return jsonify({"status": "error", "message": "No files uploaded."}), 400

        # Save files to a temporary directory
        file_paths = []
        for file in files:
            temp_path = os.path.join(temp_dir, file.filename)
            file.save(temp_path)
            file_paths.append(temp_path)

        # Generate the output Excel file path
        output_excel = os.path.join(output_dir, "consolidated_properties.xlsx")

        # Run the pipeline
        process_surveys(file_paths, output_excel)

        # Return the result
        return jsonify({"status": "success", "output_file": output_excel}), 200

    except Exception as e:
        logging.error(f"Error in processing: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
