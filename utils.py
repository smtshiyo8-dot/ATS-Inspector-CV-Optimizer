import io
import re
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from docx import Document

# --- Extract text from CV ---
def extract_text_from_cv(file):
    text = ""
    file.stream.seek(0)  # Ensure we start at the beginning
    if file.filename.lower().endswith(".pdf"):
        pdf = PdfReader(file)
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    elif file.filename.lower().endswith(".docx"):
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        # fallback for text files
        text = file.read().decode(errors="ignore")
    return text.lower()

# --- Detect ATS (placeholder logic) ---
def detect_ats(file):
    return "Greenhouse"  # Replace with real detection logic if needed

# --- Score CV against job description ---
def score_cv(file, job_description=""):
    cv_text = extract_text_from_cv(file)

    # Extract keywords from job description (words with 5+ chars)
    if not job_description.strip():
        job_keywords = ["hr", "recruitment", "employee relations", "performance", "training", "compliance"]
    else:
        job_keywords = [w.lower() for w in re.findall(r"\b\w{5,}\b", job_description)]

    matched = [kw for kw in job_keywords if kw in cv_text]
    missing = [kw for kw in job_keywords if kw not in cv_text]

    score = int((len(matched) / len(job_keywords)) * 100) if job_keywords else 0

    improvements = []
    if missing:
        improvements.append(f"Missing important keywords: {', '.join(missing[:10])}...")
    if score < 80:
        improvements.append("Consider tailoring your CV more closely to the job description.")
    if "summary" not in cv_text:
        improvements.append("Add a professional summary section at the top.")

    # Return score, improvement suggestions, and missing keywords
    return score, improvements, missing

# --- Create Optimized PDF ---
def modify_cv_pdf(file, missing_keywords):
    file.stream.seek(0)
    original_text = extract_text_from_cv(file)

    optimized_text = original_text + "\n\n=== Optimized for Job Description ===\n"
    if missing_keywords:
        optimized_text += "Keywords Added: " + ", ".join(missing_keywords)
    else:
        optimized_text += "No additional keywords needed. CV already well optimized."

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    text_obj = c.beginText(40, 800)
    for line in optimized_text.split("\n"):
        text_obj.textLine(line)
    c.drawText(text_obj)
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer

# --- Create Optimized Word DOCX ---
def modify_cv_docx(file, missing_keywords):
    file.stream.seek(0)
    original_text = extract_text_from_cv(file)

    doc = Document()
    doc.add_heading("Optimized CV", 0)

    doc.add_paragraph(original_text)

    doc.add_heading("Optimized for Job Description", level=1)
    if missing_keywords:
        doc.add_paragraph("Keywords Added: " + ", ".join(missing_keywords))
    else:
        doc.add_paragraph("No additional keywords needed. CV already well optimized.")

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
