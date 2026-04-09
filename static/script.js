document.getElementById('upload-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const fileInput = document.getElementById('resume-file');
    const file = fileInput.files[0];
    
    document.getElementById('error').classList.add('hidden');
    document.getElementById('results').classList.add('hidden');

    if (!file) {
        document.getElementById('error').textContent = "⚠️ Please select a file first!";
        document.getElementById('error').classList.remove('hidden');
        return;
    }

    const formData = new FormData();
    formData.append('resume', file);

    const btn = document.getElementById('analyze-btn');
    const loading = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    const resultsDiv = document.getElementById('results');

    loading.classList.remove('hidden');
    btn.disabled = true;
    btn.textContent = 'Processing...';

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to analyze resume');
        }

        displayResults(data);
        
        // Scroll to results AFTER displaying them
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
    // Score with color coding
    const scoreElement = document.getElementById('score-value');
    scoreElement.textContent = `${data.score}/100`;
    
    // Add color class based on score
    scoreElement.className = 'score';
    if (data.score >= 80) {
        scoreElement.classList.add('score-excellent');
        document.getElementById('score-message').textContent = '🌟 Excellent! Your resume is strong!';
    } else if (data.score >= 60) {
        scoreElement.classList.add('score-good');
        document.getElementById('score-message').textContent = '👍 Good! A few improvements needed.';
    } else if (data.score >= 40) {
        scoreElement.classList.add('score-average');
        document.getElementById('score-message').textContent = '⚠️ Average. Needs significant work.';
    } else {
        scoreElement.classList.add('score-poor');
        document.getElementById('score-message').textContent = '❌ Needs major improvements.';
    }

    // Word count
    document.getElementById('word-count').innerHTML = 
        `<strong style="font-size: 1.5rem; color: var(--primary);">${data.word_count}</strong> words`;

    // Skills with badges
    const skillsContainer = document.getElementById('skills-container');
    if (data.skills_found.length > 0) {
        skillsContainer.innerHTML = data.skills_found
            .map(skill => `<span class="badge">${skill.toUpperCase()}</span>`)
            .join('');
    } else {
        skillsContainer.innerHTML = '<p class="empty-state">No target skills detected</p>';
    }

    // Sections
    const sectionsList = document.getElementById('sections-list');
    if (data.sections_found.length > 0) {
        sectionsList.innerHTML = data.sections_found
            .map(section => `<li>✅ ${section.charAt(0).toUpperCase() + section.slice(1)}</li>`)
            .join('');
    } else {
        sectionsList.innerHTML = '<li class="empty-state">No key sections found</li>';
    }

    // Certifications
    const certContainer = document.getElementById('certifications-container');
    if (data.certifications && data.certifications.length > 0) {
        certContainer.innerHTML = '<ul>' + 
            data.certifications.map(cert => `<li style="padding: 0.5rem 0; border-bottom: 1px solid var(--border);">🏆 ${cert}</li>`).join('') +
            '</ul>';
    } else {
        certContainer.innerHTML = '<p class="empty-state">No certifications detected<br><small>Add certifications from Udemy, Coursera, AWS, etc.</small></p>';
    }

    // Suggestions
    const suggestionsList = document.getElementById('suggestions-list');
    suggestionsList.innerHTML = data.suggestions
        .map(suggestion => `<li>${suggestion}</li>`)
        .join('');

    // Project suggestions
    const projectsList = document.getElementById('projects-list');
    if (data.project_suggestions && data.project_suggestions.length > 0) {
        projectsList.innerHTML = data.project_suggestions
            .map(project => `<li>💻 ${project}</li>`)
            .join('');
    } else {
        projectsList.innerHTML = '<li class="empty-state">Add skills to get personalized project suggestions!</li>';
    }

    // Show results
    document.getElementById('results').classList.remove('hidden');
}