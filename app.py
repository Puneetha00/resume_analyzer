"""
Resume Analyzer - Enhanced Version
Now detects certifications, courses, and suggests projects!
"""

import os
import io
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import PyPDF2

app = Flask(__name__)

# ✅ IMPORTANT: Enable CORS (for Vercel frontend)
CORS(app, resources={r"/*": {"origins": "*"}})

ALLOWED_EXTENSIONS = {'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(file, filename):
    ext = filename.rsplit('.', 1)[1].lower()
    
    if ext == 'txt':
        return file.read().decode('utf-8', errors='ignore')
    
    elif ext == 'pdf':
        pdf_bytes = io.BytesIO(file.read())
        reader = PyPDF2.PdfReader(pdf_bytes)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    
    return ""

# 🔥 PROJECT SUGGESTIONS
def suggest_projects(skills_found):
    suggestions = []

    if 'python' in skills_found:
        if 'sql' in skills_found:
            suggestions.append("🐍 Python + SQL: Build a Student Database Management System")
        suggestions.append("🐍 Python: Create a Weather CLI Tool using APIs")

    if 'javascript' in skills_found:
        suggestions.append("⚡ JavaScript: Build a To-Do List App")

    if not skills_found:
        suggestions.append("💡 Start with: Portfolio Website")

    return suggestions[:5]

# 🔍 ANALYSIS
def analyze_resume(text):
    target_skills = ["python", "java", "html", "css", "javascript", "sql"]
    text_lower = text.lower()

    found_skills = [skill for skill in target_skills if skill in text_lower]
    word_count = len(text.split())

    target_sections = ["education", "experience", "projects"]
    found_sections = [sec for sec in target_sections if sec in text_lower]

    # Certifications
    cert_keywords = ["certification", "certificate", "udemy", "coursera", "aws"]
    certifications = []

    for line in text.split('\n'):
        if any(c in line.lower() for c in cert_keywords):
            certifications.append(line.strip())

    # Score
    score = min(len(found_skills) * 10, 100)

    suggestions = []
    if len(found_skills) < 2:
        suggestions.append("📚 Add more skills")

    if "projects" not in text_lower:
        suggestions.append("🚀 Add projects section")

    project_suggestions = suggest_projects(found_skills)

    return {
        "score": score,
        "skills_found": found_skills,
        "word_count": word_count,
        "sections_found": found_sections,
        "certifications": certifications[:5],
        "suggestions": suggestions,
        "project_suggestions": project_suggestions
    }

# 🏠 HOME ROUTE (for testing)
@app.route('/')
def home():
    return "Backend is running!"

# 📤 ANALYZE ROUTE
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['resume']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    try:
        text = extract_text(file, file.filename)

        if not text.strip():
            return jsonify({"error": "Empty file"}), 400

        result = analyze_resume(text)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🚀 IMPORTANT FOR RENDER
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)