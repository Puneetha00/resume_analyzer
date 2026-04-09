document.querySelector("form").addEventListener("submit", async function(e) {
    e.preventDefault(); // 🚫 stops page reload

    const fileInput = document.querySelector('input[type="file"]');
    const file = fileInput.files[0];

    if (!file) {
        alert("Please upload a file");
        return;
    }

    const formData = new FormData();
    formData.append("resume", file);

    try {
        const res = await fetch("https://resume-analyzer-nocb.onrender.com/analyze", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        console.log(data); // 🔍 check in console first

        // 👉 DO NOT change UI here yet
        // just confirm backend works

    } catch (err) {
        console.error(err);
        alert("Error connecting to backend");
    }
});