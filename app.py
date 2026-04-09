import os
import io
from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2

app = Flask(__name__)

# ✅ Allow frontend (Vercel) to connect
CORS(app, resources={r"/*": {"origins": "*"}})

ALLOWED_EXTENSIONS = {'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 📄 Extract text
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


# 🚀 Project Suggestions
def suggest_projects(skills_found):
    suggestions = []

    if 'python' in skills_found:
        suggestions.append("🐍 Build a REST API using Flask")
        suggestions.append("🐍 Create a Resume Analyzer with AI")

    if 'javascript' in skills_found:
        suggestions.append("⚡ Build a dynamic To-Do App")
        suggestions.append("⚡ Create a Portfolio Website")

    if 'react' in skills_found:
        suggestions.append("⚛️ Build a full-stack MERN project")

    if 'sql' in skills_found:
        suggestions.append("🗄️ Build a Student Database System")

    if not suggestions:
        suggestions.append("💡 Start with a personal portfolio website")

    return suggestions[:5]


# 🧠 MAIN ANALYSIS
def analyze_resume(text):
    text_lower = text.lower()
    words = text.split()
    word_count = len(words)

    # 🎯 Skills
    target_skills = [
        "python", "java", "c++", "html", "css", "javascript",
        "react", "node", "sql", "mongodb", "flask", "django"
    ]
    found_skills = [skill for skill in target_skills if skill in text_lower]

    # 📑 Sections
    target_sections = [
        "education", "experience", "projects",
        "skills", "certification", "internship"
    ]
    found_sections = [sec for sec in target_sections if sec in text_lower]

    # 🏆 Certifications
    cert_keywords = ["certification", "certificate", "udemy", "coursera", "aws", "google"]
    certifications = []

    for line in text.split('\n'):
        if any(c in line.lower() for c in cert_keywords):
            certifications.append(line.strip())

    # 🔥 SMART SCORING (100 total)
    score = 0

    # Skills (30)
    score += min(len(found_skills) * 5, 30)

    # Sections (25)
    score += min(len(found_sections) * 5, 25)

    # Word count (15)
    if 300 <= word_count <= 800:
        score += 15
    elif 200 <= word_count < 300 or 800 < word_count <= 1000:
        score += 10
    else:
        score += 5

    # Certifications (10)
    score += min(len(certifications) * 2, 10)

    # Projects (20)
    if "projects" in text_lower:
        score += 20
    else:
        score += 5

    # 💡 Suggestions
    suggestions = []

    if len(found_skills) < 4:
        suggestions.append("📚 Add more relevant technical skills")

    if "projects" not in text_lower:
        suggestions.append("🚀 Add a projects section with real work")

    if word_count < 300:
        suggestions.append("📝 Resume is too short, add more content")
    elif word_count > 900:
        suggestions.append("✂️ Resume is too long, keep it concise")

    if len(certifications) == 0:
        suggestions.append("🏆 Add certifications to improve credibility")

    if "experience" not in text_lower:
        suggestions.append("💼 Add experience or internships")

    # 🚀 Project ideas
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


# 🏠 Test route
@app.route('/')
def home():
    return "Backend is running!"


# 📤 Analyze API
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
            return jsonify({"error": "Empty or unreadable file"}), 400

        result = analyze_resume(text)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🚀 Render entry
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)