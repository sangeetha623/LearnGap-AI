let selectedLevel = "Beginner";

const levelButtons = document.querySelectorAll(".level");

levelButtons.forEach(button => {

    button.addEventListener("click", () => {

        levelButtons.forEach(btn => {
            btn.classList.remove("active");
        });

        button.classList.add("active");

        selectedLevel = button.dataset.level;
    });

});

function scrollToAnalyzer() {
    document.getElementById("analyze").scrollIntoView({
        behavior: "smooth"
    });
}

function showDemo() {

    alert(
        "LearnGap AI works in 3 steps:\n\n" +
        "1. Enter your current skills\n" +
        "2. Select your target career\n" +
        "3. AI identifies your skill gaps and creates a roadmap."
    );
}

async function analyzeSkills() {

    const skills = document.getElementById("skills").value.trim();
    const career = document.getElementById("career").value.trim();

    if (!skills) {
        alert("Please enter your current skills.");
        return;
    }

    if (!career) {
        alert("Please enter your target career.");
        return;
    }

    const results = document.getElementById("results");
    const loading = document.getElementById("loading");
    const resultContent = document.getElementById("resultContent");

    results.style.display = "block";

    loading.style.display = "block";
    resultContent.style.display = "none";

    results.scrollIntoView({
        behavior: "smooth"
    });

    try {

        const response = await fetch("http://127.0.0.1:8000/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                skills: skills,
                career: career,
                level: selectedLevel
            })

        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        displayResults(data);

    } catch (error) {

        console.error(error);

        alert(
            "Unable to connect to LearnGap AI backend.\n\n" +
            "Make sure the FastAPI server is running."
        );

        results.style.display = "none";
    }

}

function displayResults(data) {

    document.getElementById("currentSkills").innerHTML =
        data.current_skills.map(skill =>
            `<span class="skill-tag">${skill}</span>`
        ).join("");

    document.getElementById("skillGaps").innerHTML =
        data.skill_gaps.map(skill =>
            `<span class="skill-tag">${skill}</span>`
        ).join("");

    document.getElementById("targetRole").textContent =
        data.target_role;

    document.getElementById("careerMessage").textContent =
        data.career_message;

    const roadmap = document.getElementById("roadmap");

    roadmap.innerHTML = data.roadmap.map((step, index) => {

        return `
            <div class="roadmap-step">

                <div class="step-number">
                    ${index + 1}
                </div>

                <div>
                    <h3>${step.title}</h3>
                    <p>${step.description}</p>
                </div>

            </div>
        `;

    }).join("");

    const recommendations =
        document.getElementById("recommendations");

    recommendations.innerHTML =
        data.recommendations.map(item => {

            return `
                <div class="recommendation">
                    💡 ${item}
                </div>
            `;

        }).join("");

    document.getElementById("loading").style.display = "none";

    document.getElementById("resultContent").style.display = "block";
}