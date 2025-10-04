from werkzeug.datastructures import FileStorage

def detect_ats(file: FileStorage) -> str:
    # Placeholder: pretend we detect ATS from job ad or file content
    return "Greenhouse"

def score_cv(file: FileStorage) -> str:
    # Placeholder: calculate a dummy score
    return "78%"

def modify_cv(file: FileStorage) -> FileStorage:
    # Placeholder: return the same file as "optimized"
    # In real logic, you would modify CV here
    return file
