"""
Resume Analyzer - Enhanced Version
Now detects certifications, courses, and suggests projects!
"""
import os
import io
from flask import Flask, request, jsonify, render_template
import PyPDF2

app = Flask(__name__)

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

def suggest_projects(skills_found):
    """Suggest projects based on skills detected"""
    suggestions = []
    
    # Python projects
    if 'python' in skills_found:
        if 'sql' in skills_found:
            suggestions.append("🐍 Python + SQL: Build a Student Database Management System")
            suggestions.append("🐍 Python + SQL: Create a Library Book Tracking App")
        if 'html' in skills_found or 'css' in skills_found:
            suggestions.append("🐍 Python Web: Build a Personal Portfolio Website with Flask/Django")
            suggestions.append("🐍 Python Web: Create a Blog Platform with User Authentication")
        if 'javascript' in skills_found:
            suggestions.append("🐍 Full Stack: Build a Task Management App (Python backend + JS frontend)")
        suggestions.append("🐍 Python: Create a Weather CLI Tool using APIs")
        suggestions.append("🐍 Python: Build an Automated File Organizer")
    
    # JavaScript projects
    if 'javascript' in skills_found:
        if 'html' in skills_found and 'css' in skills_found:
            suggestions.append("⚡ JavaScript: Build an Interactive To-Do List App")
            suggestions.append("⚡ JavaScript: Create a Calculator with Modern UI")
            suggestions.append("⚡ JavaScript: Build a Weather Dashboard")
        if 'sql' in skills_found:
            suggestions.append("⚡ JavaScript + SQL: Create a Note-Taking Web App")
    
    # Java projects
    if 'java' in skills_found:
        suggestions.append("☕ Java: Build a Banking Management System")
        suggestions.append("☕ Java: Create a Student Grade Calculator")
        if 'sql' in skills_found:
            suggestions.append("☕ Java + SQL: Develop an Inventory Management System")
    
    # Web Development projects
    if 'html' in skills_found and 'css' in skills_found:
        if 'javascript' not in skills_found:
            suggestions.append("🎨 HTML/CSS: Create a Responsive Restaurant Landing Page")
            suggestions.append("🎨 HTML/CSS: Build a Personal Resume/CV Website")
    
    # SQL projects
    if 'sql' in skills_found:
        if 'python' not in skills_found and 'java' not in skills_found:
            suggestions.append("📊 SQL: Design a Database for an E-commerce Platform")
            suggestions.append("📊 SQL: Create Queries for a Hospital Management System")
    
    # Default suggestions if no skills found
    if not skills_found:
        suggestions.append("💡 Start with: Personal Portfolio Website (HTML/CSS)")
        suggestions.append("💡 Beginner Project: Simple Calculator")
        suggestions.append("💡 Learn Python: Build a Number Guessing Game")
    
    return suggestions[:5]  # Return top 5 suggestions

def analyze_resume(text):
    # Skills Detection
    target_skills = ["python", "java", "html", "css", "javascript", "sql"]
    text_lower = text.lower()
    found_skills = [skill for skill in target_skills if skill in text_lower]
    
    # Word Count
    word_count = len(text.split())
    
    # Section Detection
    target_sections = ["education", "experience", "projects"]
    found_sections = [sec for sec in target_sections if sec in text_lower]
    
    # Certification & Course Detection
    cert_keywords = [
        "certification", "certificate", "certified", "credential",
        "udemy", "coursera", "edx", "udacity", "linkedin learning",
        "aws certified", "google certificate", "microsoft certified",
        "oracle certified", "cisco certified", "comptia"
    ]
    course_keywords = [
        "course", "courses", "training", "workshop", "bootcamp",
        "completed", "enrolled", "learning", "studied"
    ]
    
    certifications = []
    courses = []
    
    # Simple detection: look for lines containing these keywords
    lines = text.split('\n')
    for line in lines:
        line_lower = line.lower().strip()
        if any(cert in line_lower for cert in cert_keywords):
            certifications.append(line.strip())
        if any(course in line_lower for course in course_keywords):
            if line.strip() not in certifications:  # Avoid duplicates
                courses.append(line.strip())
    
    # Scoring (Skills: 30pts, Length: 20pts, Sections: 20pts, Certs: 15pts, Projects: 15pts)
    skill_score = min(len(found_skills) * 7.5, 30)
    
    if 300 <= word_count <= 800:
        length_score = 20
    elif word_count < 300:
        length_score = max(0, int((word_count / 300) * 20))
    else:
        length_score = max(0, 20 - int((word_count - 800) / 200) * 5)
    
    section_score = min(len(found_sections) * 6.7, 20)
    
    cert_score = min(len(certifications) * 7.5, 15)
    project_score = min(15 if "projects" in text_lower else 0, 15)
    
    total_score = min(int(skill_score + length_score + section_score + cert_score + project_score), 100)
    
    # Generate Suggestions
    suggestions = []
    
    if len(found_skills) < 3:
        suggestions.append("📚 Add more technical skills like Python, JavaScript, or SQL to stand out.")
    
    if word_count < 300:
        suggestions.append("📝 Your resume is too short. Aim for 300-800 words.")
    elif word_count > 800:
        suggestions.append("📄 Your resume is too long. Keep it 300-800 words.")
    
    if "education" not in text_lower:
        suggestions.append("🎓 Include an 'Education' section.")
    
    if "experience" not in text_lower:
        suggestions.append("💼 Add an 'Experience' section.")
    
    if "projects" not in text_lower:
        suggestions.append("🚀 Include a 'Projects' section to showcase your work.")
    
    if len(certifications) == 0:
        suggestions.append("🏆 Add certifications (Udemy, Coursera, AWS, Google, etc.) to boost credibility.")
    
    if len(found_skills) >= 2 and "projects" not in text_lower:
        suggestions.append("💡 Add projects that use your skills: " + ", ".join(found_skills).title())
    
    if not suggestions:
        suggestions.append("✅ Excellent! Your resume is well-structured and comprehensive.")
    
    # Get project suggestions based on skills
    project_suggestions = suggest_projects(found_skills)
    
    return {
        "score": total_score,
        "skills_found": found_skills,
        "word_count": word_count,
        "sections_found": found_sections,
        "certifications": certifications[:5],  # Limit to 5
        "courses": courses[:5],  # Limit to 5
        "suggestions": suggestions,
        "project_suggestions": project_suggestions
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Upload PDF or TXT."}), 400

    try:
        text = extract_text(file, file.filename)
        if not text.strip():
            return jsonify({"error": "Could not extract text from file."}), 400
            
        result = analyze_resume(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)