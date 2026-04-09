def analyze_resume(text):
    text_lower = text.lower()
    words = text.split()
    word_count = len(words)

    # 🎯 SKILLS
    target_skills = [
        "python", "java", "c++", "html", "css", "javascript",
        "react", "node", "sql", "mongodb", "flask", "django"
    ]
    found_skills = [skill for skill in target_skills if skill in text_lower]

    # 📑 SECTIONS
    target_sections = [
        "education", "experience", "projects", "skills",
        "certification", "internship"
    ]
    found_sections = [sec for sec in target_sections if sec in text_lower]

    # 🏆 CERTIFICATIONS
    cert_keywords = ["certification", "certificate", "udemy", "coursera", "aws", "google"]
    certifications = []

    for line in text.split('\n'):
        if any(c in line.lower() for c in cert_keywords):
            certifications.append(line.strip())

    # 🧠 SCORING SYSTEM
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

    # 💡 SUGGESTIONS
    suggestions = []

    if len(found_skills) < 4:
        suggestions.append("📚 Add more relevant technical skills")

    if "projects" not in text_lower:
        suggestions.append("🚀 Add a projects section with real work")

    if word_count < 300:
        suggestions.append("📝 Increase resume content (too short)")
    elif word_count > 900:
        suggestions.append("✂️ Reduce resume length (too long)")

    if len(certifications) == 0:
        suggestions.append("🏆 Add certifications to boost credibility")

    if "experience" not in text_lower:
        suggestions.append("💼 Add experience or internships")

    # 🚀 PROJECT SUGGESTIONS
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