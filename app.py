from flask import Flask, request, jsonify, render_template
import os

# Import your ATS processing functions
from utils import detect_ats, score_cv, modify_cv  # make sure utils.py exists

app = Flask(__name__)

# Home / Upload page
@app.route("/")
@app.route("/upload")
def upload_page():
    return render_template("upload.html")

# API route to process CV
@app.route("/process-cv", methods=["POST"])
def process_cv():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    filename = file.filename

    # ✅ Call your real ATS processing functions
    ats_result = detect_ats(file)        # detect ATS
    score = score_cv(file)               # calculate CV score
    modified_cv = modify_cv(file)        # generate optimized CV

    # Save modified CV to static/optimized/
    output_folder = os.path.join("static", "optimized")
    os.makedirs(output_folder, exist_ok=True)
    modified_path = os.path.join(output_folder, f"{filename}_optimized.pdf")
    modified_cv.save(modified_path)      # assuming modified_cv is a file-like object

    # Return JSON result
    result = {
        "filename": filename,
        "ats_detected": ats_result,
        "cv_score": score,
        "improvements": ["Add role-specific keywords", "Improve formatting"],  # customize
        "modified_cv_url": f"/static/optimized/{filename}_optimized.pdf"
    }

    return jsonify(result), 200

# Favicon handler (optional)
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

# Entry point
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
