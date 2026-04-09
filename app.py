import os
import io
from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2

app = Flask(__name__)

# ✅ Allow Vercel frontend
CORS(app, resources={r"/*": {"origins": "*"}})

ALLOWED_EXTENSIONS = {'txt', 'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 📄 Extract text from file
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
        suggestions.append("🐍 Create an AI Resume Analyzer")

    if 'javascript' in skills_found:
        suggestions.append("⚡ Build a dynamic To-Do App")

    if 'react' in skills_found:
        suggestions.append("⚛️ Build a full-stack MERN project")

    if 'sql' in skills_found:
        suggestions.append("🗄️ Build a Student Database System")

    if not suggestions:
        suggestions.append("💡 Start with a portfolio website")

    return suggestions[:5]


# 🧠 SMART ANALYSIS
def analyze_resume(text):
    text_lower = text.lower()
    words = text.split()
    word_count = len(words)

    # 🎯 Skills
    strong_skills = [
        "python", "java", "c++", "javascript", "react",
        "node", "sql", "mongodb", "flask", "django"
    ]
    basic_skills = ["html", "css"]

    found_strong = [s for s in strong_skills if s in text_lower]
    found_basic = [s for s in basic_skills if s in text_lower]
    found_skills = found_strong + found_basic

    # 📑 Sections
    sections = ["education", "experience", "projects", "skills"]
    found_sections = [sec for sec in sections if sec in text_lower]

    # 🏆 Certifications
    cert_keywords = ["certification", "certificate", "udemy", "coursera", "aws", "google"]
    certifications = [
        line.strip() for line in text.split("\n")
        if any(c in line.lower() for c in cert_keywords)
    ]

    # 💼 Experience
    has_experience = "experience" in text_lower or "internship" in text_lower

    # ⚡ Impact words
    impact_words = ["developed", "built", "created", "designed", "implemented", "optimized"]
    impact_score = sum(1 for w in impact_words if w in text_lower)

    # 🔥 SCORING
    score = 0

    # Strong skills (40)
    score += min(len(found_strong) * 6, 40)

    # Basic skills (10)
    score += min(len(found_basic) * 2, 10)

    # Sections (20)
    score += len(found_sections) * 5

    # Word count (10)
    if 400 <= word_count <= 900:
        score += 10
    elif 250 <= word_count < 400:
        score += 7
    else:
        score += 4

    # Certifications (10)
    score += min(len(certifications) * 2, 10)

    # Experience (10)
    if has_experience:
        score += 10

    # Impact words (10)
    score += min(impact_score * 2, 10)

    # 🚀 Boost (important for realistic 80–90 scores)
    if score >= 75:
        score += 10
    elif score >= 60:
        score += 5

    score = min(score, 100)

    # 💡 Suggestions
    suggestions = []

    if len(found_strong) < 3:
        suggestions.append("📚 Add more strong technical skills")

    if "projects" not in text_lower:
        suggestions.append("🚀 Add 2–3 solid projects")

    if not has_experience:
        suggestions.append("💼 Add internship or real experience")

    if impact_score < 3:
        suggestions.append("⚡ Use action words like Developed, Built")

    if len(certifications) == 0:
        suggestions.append("🏆 Add certifications")

    if word_count < 300:
        suggestions.append("📝 Resume is too short")

    # 🚀 Projects
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


# 🏠 Home route
@app.route('/')
def home():
    return "Backend is running!"


# 📤 Analyze route
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


# 🚀 Render run
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)