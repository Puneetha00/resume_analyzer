const form = document.getElementById("upload-form");

form.addEventListener("submit", async function(e) {
    e.preventDefault();

    const fileInput = document.getElementById("resume-file");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please upload a file");
        return;
    }

    const formData = new FormData();
    formData.append("resume", file);

    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("results").classList.add("hidden");
    document.getElementById("error").classList.add("hidden");

    try {
        const res = await fetch("https://resume-analyzer-nocb.onrender.com/analyze", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        document.getElementById("loading").classList.add("hidden");

        if (data.error) {
            document.getElementById("error").innerText = data.error;
            document.getElementById("error").classList.remove("hidden");
            return;
        }

        // ✅ SHOW RESULTS
        document.getElementById("results").classList.remove("hidden");

        document.getElementById("score-value").innerText = data.score;
        document.getElementById("word-count").innerText = data.word_count;

        // Skills
        const skillsDiv = document.getElementById("skills-container");
        skillsDiv.innerHTML = data.skills_found.length
            ? data.skills_found.map(s => `<span class="badge">${s}</span>`).join("")
            : "<p>No skills found</p>";

        // Sections
        const sectionsList = document.getElementById("sections-list");
        sectionsList.innerHTML = data.sections_found.length
            ? data.sections_found.map(s => `<li>${s}</li>`).join("")
            : "<li>No sections detected</li>";

        // Certifications
        const certDiv = document.getElementById("certifications-container");
        certDiv.innerHTML = data.certifications.length
            ? data.certifications.map(c => `<p>${c}</p>`).join("")
            : "<p>No certifications found</p>";

        // Suggestions
        const suggList = document.getElementById("suggestions-list");
        suggList.innerHTML = data.suggestions.length
            ? data.suggestions.map(s => `<li>${s}</li>`).join("")
            : "<li>No suggestions</li>";

        // Projects
        const projList = document.getElementById("projects-list");
        projList.innerHTML = data.project_suggestions.length
            ? data.project_suggestions.map(p => `<li>${p}</li>`).join("")
            : "<li>No project ideas</li>";

    } catch (err) {
        console.error(err);
        document.getElementById("loading").classList.add("hidden");

        document.getElementById("error").innerText = "Error connecting to backend";
        document.getElementById("error").classList.remove("hidden");
    }
});