document.getElementById('upload-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const fileInput = document.getElementById('resume-file');
    const file = fileInput.files[0];
    
    const errorDiv = document.getElementById('error');
    const resultsDiv = document.getElementById('results');

    errorDiv.classList.add('hidden');
    resultsDiv.classList.add('hidden');

    if (!file) {
        errorDiv.textContent = "⚠️ Please select a file first!";
        errorDiv.classList.remove('hidden');
        return;
    }

    const formData = new FormData();
    formData.append('resume', file);

    const btn = document.getElementById('analyze-btn');
    const loading = document.getElementById('loading');

    loading.classList.remove('hidden');
    btn.disabled = true;
    btn.textContent = 'Processing...';

    try {
        const response = await fetch('https://resume-analyzer-nocb.onrender.com/analyze', {
            method: 'POST',
            body: formData
        });

        // 🔥 Handle non-JSON errors safely
        let data;
        try {
            data = await response.json();
        } catch {
            throw new Error("Server error or invalid response");
        }

        if (!response.ok) {
            throw new Error(data.error || 'Failed to analyze resume');
        }

        displayResults(data);

        // Smooth scroll
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (err) {
        errorDiv.textContent = `❌ ${err.message}`;
        errorDiv.classList.remove('hidden');
    } finally {
        loading.classList.add('hidden');
        btn.disabled = false;
        btn.textContent = '🚀 Analyze Resume';
    }
});

function displayResults(data) {

    // ✅ Safe fallback (avoid crashes if backend misses fields)
    const score = data.score || 0;
    const wordCount = data.word_count || 0;
    const skills = data.skills_found || [];
    const sections = data.sections_found || [];
    const certifications = data.certifications || [];
    const suggestions = data.suggestions || [];
    const projects = data.project_suggestions || [];

    // Score
    const scoreElement = document.getElementById('score-value');
    scoreElement.textContent = `${score}/100`;
    
    scoreElement.className = 'score';

    if (score >= 80) {
        scoreElement.classList.add('score-excellent');
        document.getElementById('score-message').textContent = '🌟 Excellent! Your resume is strong!';
    } else if (score >= 60) {
        scoreElement.classList.add('score-good');
        document.getElementById('score-message').textContent = '👍 Good! A few improvements needed.';
    } else if (score >= 40) {
        scoreElement.classList.add('score-average');
        document.getElementById('score-message').textContent = '⚠️ Average. Needs significant work.';
    } else {
        scoreElement.classList.add('score-poor');
        document.getElementById('score-message').textContent = '❌ Needs major improvements.';
    }

    // Word count
    document.getElementById('word-count').innerHTML = 
        `<strong style="font-size: 1.5rem; color: var(--primary);">${wordCount}</strong> words`;

    // Skills
    const skillsContainer = document.getElementById('skills-container');
    skillsContainer.innerHTML = skills.length > 0
        ? skills.map(skill => `<span class="badge">${skill.toUpperCase()}</span>`).join('')
        : '<p class="empty-state">No target skills detected</p>';

    // Sections
    const sectionsList = document.getElementById('sections-list');
    sectionsList.innerHTML = sections.length > 0
        ? sections.map(section => `<li>✅ ${section.charAt(0).toUpperCase() + section.slice(1)}</li>`).join('')
        : '<li class="empty-state">No key sections found</li>';

    // Certifications
    const certContainer = document.getElementById('certifications-container');
    certContainer.innerHTML = certifications.length > 0
        ? '<ul>' + certifications.map(cert => 
            `<li style="padding: 0.5rem 0; border-bottom: 1px solid var(--border);">🏆 ${cert}</li>`
          ).join('') + '</ul>'
        : '<p class="empty-state">No certifications detected<br><small>Add certifications from Udemy, Coursera, AWS, etc.</small></p>';

    // Suggestions
    const suggestionsList = document.getElementById('suggestions-list');
    suggestionsList.innerHTML = suggestions.map(s => `<li>${s}</li>`).join('');

    // Projects
    const projectsList = document.getElementById('projects-list');
    projectsList.innerHTML = projects.length > 0
        ? projects.map(p => `<li>💻 ${p}</li>`).join('')
        : '<li class="empty-state">Add skills to get personalized project suggestions!</li>';

    // Show results
    document.getElementById('results').classList.remove('hidden');
}