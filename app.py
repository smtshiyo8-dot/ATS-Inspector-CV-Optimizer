from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/")
def home():
    return "Hello! ATS-Inspector is running. Ready to process CVs."

@app.route("/upload")
def upload_page():
    return render_template("upload.html")

@app.route("/process-cv", methods=["POST"])
def process_cv():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    filename = file.filename

    # Placeholder ATS logic
    result = {
        "filename": filename,
        "status": "Processed successfully",
        "message": "This is a placeholder result. Add your ATS logic here."
    }
    
    return jsonify(result), 200

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
