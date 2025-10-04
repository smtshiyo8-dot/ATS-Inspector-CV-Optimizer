from utils import detect_ats, score_cv, modify_cv
from flask import Flask, render_template, request, jsonify
import os

# Initialize the Flask app
app = Flask(__name__)

# Home / Health Check route
@app.route("/")
def home():
    return "Hello! ATS-Inspector is running. Ready to process CVs."

# API route to process CVs
@app.route("/process-cv", methods=["POST"])
def process_cv():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    filename = file.filename
    
    # Call your functions from utils.py
    ats_result = detect_ats(file)
    score = score_cv(file)
    modified_cv = modify_cv(file)
    
    result = {
        "filename": filename,
        "ats_detected": ats_result,
        "cv_score": score,
        "modified_cv": modified_cv
    }
    
    return jsonify(result), 200

# Optional: route to serve favicon
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

# Main entry point
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
