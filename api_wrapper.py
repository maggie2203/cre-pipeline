from flask import Flask, request, jsonify, send_from_directory
import os
import logging
from process_surveys import process_surveys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("api.log", mode="a"), logging.StreamHandler()]
)
logging.info("Starting the Flask application...")

# Flask app instance
app = Flask(__name__)

# Ensure output directory exists
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    """
    Default route to confirm the app is running.
    """
    return jsonify({"message": "CRE Pipeline API is running"}), 200

@app.route("/process", methods=["POST"])
def process():
    """
    Endpoint to process uploaded files.
    Accepts files via POST request and returns an output file link.
    """
    try:
        # Retrieve uploaded files
        files = request.files.getlist("files")
        if not files:
            return jsonify({"status": "error", "message": "No files uploaded."}), 400

        # Save and process each file
        file_paths = []
        for file in files:
            file_path = os.path.join(output_dir, file.filename)
            file.save(file_path)
            file_paths.append(file_path)

        # Run processing logic and generate output file
        output_excel = os.path.join(output_dir, "consolidated_properties.xlsx")
        process_surveys(file_paths, output_excel)

        # Return success response with download link
        return jsonify({
            "status": "success",
            "message": "Files processed successfully.",
            "output_file": f"/download/consolidated_properties.xlsx"
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

# Debugging paths
logging.info("Current working directory: " + os.getcwd())
logging.info("Files in current directory: " + str(os.listdir('.')))

# Main block to start the Flask server
if __name__ == "__main__":
    logging.info("Running Flask app on http://127.0.0.1:5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)

