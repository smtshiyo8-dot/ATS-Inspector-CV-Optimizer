from flask import Flask, render_template, request, jsonify
import os

# Initialize the Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# Home / Health Check route
@app.route("/")
def home():
    return "Hello! ATS-Inspector is running. Ready to process CVs."

# Example API route to process CVs (placeholder)
@app.route("/process-cv", methods=["POST"])
def process_cv():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    filename = file.filename
    
    # Placeholder logic – replace with your CV processing code
    result = {
        "filename": filename,
        "status": "Processed successfully",
        "message": "This is a placeholder result. Add your ATS logic here."
    }
    
    return jsonify(result), 200

# Optional: route to serve favicon
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

# Main entry point
if __name__ == "__main__":
    # Debug=False for production; use environment variable PORT for Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
