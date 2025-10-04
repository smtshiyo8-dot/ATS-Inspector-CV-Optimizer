from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Upload page
@app.route("/upload")
def upload_page():
    return render_template("upload.html")

# API route to process CV (dummy response for now)
@app.route("/process-cv", methods=["POST"])
def process_cv():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    filename = file.filename

    # 🚀 Dummy response — replace later with ATS detection logic
    result = {
        "filename": filename,
        "ats_detected": "Greenhouse",
        "cv_score": "78%",
        "improvements": [
            "Add more role-specific keywords.",
            "Include a summary section.",
            "Optimize formatting for ATS parsing."
        ],
        "modified_cv_url": f"/static/optimized/{filename}_optimized.pdf"
    }

    return jsonify(result), 200

# Favicon handler (optional, prevents 404s in logs)
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

# Entry point (needed for local run & Render deployment)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
