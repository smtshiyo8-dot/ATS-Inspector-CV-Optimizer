from flask import Flask, request, jsonify, render_template
import os
from utils import detect_ats, score_cv, modify_cv_pdf, modify_cv_docx

app = Flask(__name__)

@app.route("/upload")
def upload_page():
    return render_template("upload.html")

@app.route("/process-cv", methods=["POST"])
def process_cv():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    filename = os.path.splitext(file.filename)[0]  # strip extension

    job_description = request.form.get("job_description", "")
    output_format = request.form.get("output_format", "pdf")

    ats_result = detect_ats(file)
    score, improvements, missing_keywords = score_cv(file, job_description)

    output_folder = os.path.join("static", "optimized")
    os.makedirs(output_folder, exist_ok=True)

    if output_format == "docx":
        modified_cv = modify_cv_docx(file, missing_keywords)
        modified_path = os.path.join(output_folder, f"{filename}_optimized.docx")
    else:
        modified_cv = modify_cv_pdf(file, missing_keywords)
        modified_path = os.path.join(output_folder, f"{filename}_optimized.pdf")

    with open(modified_path, "wb") as f:
        f.write(modified_cv.read())

    result = {
        "filename": f"{filename}.{output_format}",
        "ats_detected": ats_result,
        "cv_score": score,
        "improvements": improvements,
        "modified_cv_url": f"/static/optimized/{os.path.basename(modified_path)}"
    }

    return jsonify(result), 200

@app.route("/")
def home():
    return render_template("upload.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
