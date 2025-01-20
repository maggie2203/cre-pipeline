from flask import Flask, request, jsonify, send_from_directory
import os
import logging
from process_surveys import process_surveys  # Assuming this handles Excel and other data extraction logic
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader  # For PDF processing (install via pip if needed)
import mimetypes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("api.log", mode="a"), logging.StreamHandler()]
)

# Flask app instance
app = Flask(__name__)

# Ensure output directory exists
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png', 'pdf', 'doc', 'docx', 'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def home():
    """Default route to confirm the app is running."""
    return jsonify({"message": "CRE Pipeline API is running"}), 200

@app.route("/process", methods=["POST"])
def process():
    """
    Endpoint to process uploaded files.
    Accepts files via POST request and returns an output file link.
    """
    try:
        # Log request headers
        logging.info(f"Request Headers: {request.headers}")

        # Retrieve uploaded files
        files = request.files.getlist("files")
        if not files:
            logging.error("No files were uploaded. Check if the 'files' field is missing or empty.")
            return jsonify({"status": "error", "message": "No files uploaded."}), 400

        # Log received files
        logging.info(f"Received Files: {[file.filename for file in files]}")

        processed_files = []

        for file in files:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(output_dir, filename)
                file.save(file_path)
                logging.info(f"Saved file: {filename}")

                # Handle file-specific processing
                ext = filename.rsplit('.', 1)[1].lower()
                if ext in {'xls', 'xlsx'}:
                    processed_files.append(f"Excel file processed: {filename}")
                elif ext in {'pdf'}:
                    pdf_reader = PdfReader(file_path)
                    pdf_text = " ".join([page.extract_text() for page in pdf_reader.pages])
                    processed_files.append(f"PDF file processed: {filename}, content extracted")
                elif ext in {'jpeg', 'jpg', 'png'}:
                    processed_files.append(f"Image file saved: {filename}")
                elif ext in {'doc', 'docx'}:
                    # Add Word file processing logic here if needed
                    processed_files.append(f"Word document saved: {filename}")
                else:
                    logging.warning(f"Unsupported file type: {filename}")
            else:
                logging.warning(f"File not allowed: {file.filename}")
                return jsonify({"status": "error", "message": f"Unsupported file type: {file.filename}"}), 400

        # Example consolidation logic for output
        output_excel = os.path.join(output_dir, "consolidated_properties.xlsx")
        process_surveys([os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.xlsx')], output_excel)

        # Return success response with download link
        return jsonify({
            "status": "success",
            "message": f"Processed {len(processed_files)} files.",
            "output_file": f"/download/consolidated_properties.xlsx",
            "processed_files": processed_files
        }), 200

    except Exception as e:
        logging.error(f"Error in /process: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    """
    Endpoint to download a file from the output directory.
    """
    try:
        return send_from_directory(output_dir, filename, as_attachment=True)
    except Exception as e:
        logging.error(f"Error in /download: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/ai-plugin.json", methods=["GET"])
def serve_ai_plugin():
    """
    Serve the ChatGPT plugin manifest file.
    """
    try:
        return send_from_directory('.', 'ai-plugin.json', as_attachment=False)
    except Exception as e:
        logging.error(f"Error serving ai-plugin.json: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/openapi.json", methods=["GET"])
def serve_openapi():
    """
    Serve the OpenAPI specification file.
    """
    try:
        return send_from_directory('.', 'openapi.json', as_attachment=False)
    except Exception as e:
        logging.error(f"Error serving openapi.json: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

# Main block to start the Flask server
if __name__ == "__main__":
    logging.info("Running Flask app on http://127.0.0.1:5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)
