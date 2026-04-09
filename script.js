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

    // ✅ SHOW FILE NAME (fix disappearing issue)
    document.getElementById('file-name').textContent = `📄 ${file.name}`;

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

        let data;
        try {
            data = await response.json();
        } catch {
            throw new Error("Server error");
        }

        if (!response.ok) {
            throw new Error(data.error || 'Failed to analyze resume');
        }

        displayResults(data);
        resultsDiv.scrollIntoView({ behavior: 'smooth' });

    } catch (err) {
        errorDiv.textContent = `❌ ${err.message}`;
        errorDiv.classList.remove('hidden');
    } finally {
        loading.classList.add('hidden');
        btn.disabled = false;
        btn.textContent = '🚀 Analyze Resume';
    }
});