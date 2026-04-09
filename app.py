import os
import io
from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2

app = Flask(__name__)

# ✅ Allow all origins (Vercel frontend)
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
def suggest_projects(skills):
    suggestions = []

    if 'python' in skills:
        suggestions.append("Build a REST API using Flask")
        suggestions.append("Create an AI-based project")

    if 'javascript' in skills:
        suggestions.append("Build an interactive web app")

    if 'react' in skills:
        suggestions.append("Develop a full-stack MERN project")

    if 'sql' in skills:
        suggestions.append("Build a database-driven system")

    if not suggestions:
        suggestions.append("Start with a personal portfolio website")

    return suggestions[:5]


# 🧠 REAL ANALYSIS FUNCTION
def analyze_resume(text):
    text_lower = text.lower()
    words = text.split()
    word_count = len(words)

    # 🎯 Skills detection
    skills_db = [
        "python", "java", "c++", "javascript", "react",
        "node", "sql", "mongodb", "flask", "django",
        "machine learning", "data analysis"
    ]

    found_skills = list(set([s for s in skills_db if s in text_lower]))

    # 📑 Sections
    sections = ["education", "experience", "projects", "skills"]
    found_sections = [sec for sec in sections if sec in text_lower]

    # 🏆 Certifications
    cert_keywords = ["certification", "certificate", "udemy", "coursera", "aws", "google"]
    certifications = [
        line.strip() for line in text.split("\n")
        if any(c in line.lower() for c in cert_keywords)
    ]

    # 💼 Experience detection
    has_experience = "experience" in text_lower or "internship" in text_lower

    # ⚡ Action words (quality)
    action_words = [
        "developed", "built", "created", "designed",
        "implemented", "optimized", "led", "improved"
    ]
    action_count = sum(text_lower.count(word) for word in action_words)

    # 📊 Project depth
    project_lines = [line for line in text.split("\n") if "project" in line.lower()]
    project_depth = len(project_lines)

    # 🔥 SCORING (REALISTIC)
    score = 0

    # Skills (25)
    score += min(len(found_skills) * 4, 25)

    # Sections (20)
    score += len(found_sections) * 5

    # Word count (10)
    if 400 <= word_count <= 900:
        score += 10
    elif 250 <= word_count < 400 or 900 < word_count <= 1100:
        score += 7
    else:
        score += 4

    # Experience (15)
    if has_experience:
        score += 15

    # Projects (15)
    score += min(project_depth * 3, 15)

    # Action words (10)
    score += min(action_count * 2, 10)

    # Certifications (5)
    score += min(len(certifications), 5)

    # ❌ Penalty: keyword stuffing
    if len(found_skills) > 8 and action_count < 2:
        score -= 5

    # ❌ Penalty: very short resume
    if word_count < 200:
        score -= 10

    # Clamp score
    score = max(20, min(score, 100))

    # 💡 Suggestions
    suggestions = []

    if len(found_skills) < 4:
        suggestions.append("Add more relevant technical skills with examples")

    if project_depth < 2:
        suggestions.append("Add detailed project descriptions")

    if action_count < 3:
        suggestions.append("Use strong action verbs like 'Developed', 'Led'")

    if not has_experience:
        suggestions.append("Add internship or work experience")

    if len(certifications) == 0:
        suggestions.append("Add certifications to strengthen your resume")

    if word_count < 300:
        suggestions.append("Resume is too short — add more content")

    # 🚀 Projects suggestion
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


# 📤 Analyze API
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF and TXT files allowed"}), 400

    try:
        text = extract_text(file, file.filename)

        if not text.strip():
            return jsonify({"error": "File is empty or unreadable"}), 400

        result = analyze_resume(text)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🚀 Run (Render compatible)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)