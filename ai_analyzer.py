import os
import json
import re

try:
    from google import genai
except ImportError:
    genai = None


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


CAREER_SKILLS = {

    "full stack developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Express",
        "SQL",
        "Git",
        "REST API"
    ],

    "frontend developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Git",
        "Responsive Design",
        "REST API"
    ],

    "backend developer": [
        "Python",
        "Node.js",
        "SQL",
        "REST API",
        "Git",
        "Authentication",
        "Database"
    ],

    "python developer": [
        "Python",
        "OOP",
        "SQL",
        "Git",
        "REST API",
        "Testing"
    ],

    "data scientist": [
        "Python",
        "SQL",
        "Statistics",
        "Pandas",
        "NumPy",
        "Machine Learning",
        "Data Visualization"
    ],

    "machine learning engineer": [
        "Python",
        "NumPy",
        "Pandas",
        "Machine Learning",
        "Deep Learning",
        "SQL",
        "Git",
        "APIs"
    ],

    "ai engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "LLMs",
        "APIs",
        "Git"
    ],

    "java developer": [
        "Java",
        "OOP",
        "Collections",
        "SQL",
        "Spring Boot",
        "REST API",
        "Git"
    ]
}


def normalize(text):

    return text.lower().strip()


def parse_skills(skill_text):

    raw_skills = re.split(
        r",|;|\n|\|",
        skill_text
    )

    skills = []

    for skill in raw_skills:

        skill = skill.strip()

        if skill:
            skills.append(skill)

    return skills


def find_required_skills(career):

    career_lower = normalize(career)

    for role, skills in CAREER_SKILLS.items():

        if role in career_lower:
            return skills

    if "developer" in career_lower:
        return [
            "Programming",
            "Git",
            "SQL",
            "APIs",
            "Problem Solving",
            "Projects"
        ]

    if "data" in career_lower:
        return [
            "Python",
            "SQL",
            "Statistics",
            "Data Analysis",
            "Machine Learning"
        ]

    if "ai" in career_lower:
        return [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "NLP",
            "APIs"
        ]

    return [
        "Programming",
        "Problem Solving",
        "Git",
        "SQL",
        "Projects"
    ]


def analyze_with_gemini(skills, career, level):

    if not genai or not GEMINI_API_KEY:
        return None

    try:

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        prompt = f"""
You are LearnGap AI, a career learning assistant.

Analyze the student's learning gap.

Current skills:
{skills}

Target career:
{career}

Experience level:
{level}

Return ONLY valid JSON using this structure:

{{
    "skill_gaps": [],
    "career_message": "",
    "roadmap": [
        {{
            "title": "",
            "description": ""
        }}
    ],
    "recommendations": []
}}

Identify practical missing skills.
Create a realistic beginner-friendly roadmap.
Do not invent certifications.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text

        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        return json.loads(text)

    except Exception:
        return None


def analyze_learning_gap(
    skill_text,
    career,
    level
):

    current_skills = parse_skills(skill_text)

    required_skills = find_required_skills(career)

    current_lower = [
        normalize(skill)
        for skill in current_skills
    ]

    gaps = []

    for required in required_skills:

        required_lower = normalize(required)

        found = False

        for current in current_lower:

            if (
                required_lower in current
                or current in required_lower
            ):
                found = True
                break

        if not found:
            gaps.append(required)

    ai_result = analyze_with_gemini(
        skill_text,
        career,
        level
    )

    if ai_result:

        return {
            "current_skills": current_skills,
            "skill_gaps": ai_result.get(
                "skill_gaps",
                gaps
            ),
            "target_role": career,
            "career_message": ai_result.get(
                "career_message",
                "Focus on the identified skill gaps."
            ),
            "roadmap": ai_result.get(
                "roadmap",
                []
            ),
            "recommendations": ai_result.get(
                "recommendations",
                []
            )
        }

    roadmap = create_roadmap(
        gaps,
        career
    )

    recommendations = create_recommendations(
        gaps,
        career
    )

    return {
        "current_skills": current_skills,
        "skill_gaps": gaps,
        "target_role": career,
        "career_message": (
            f"For a {career} role, focus on "
            f"building the missing skills step by step."
        ),
        "roadmap": roadmap,
        "recommendations": recommendations
    }


def create_roadmap(gaps, career):

    if not gaps:

        return [
            {
                "title": "Strengthen Your Existing Skills",
                "description":
                    "Practice advanced concepts and build real-world projects."
            },
            {
                "title": "Build Portfolio Projects",
                "description":
                    "Create projects related to your target career."
            },
            {
                "title": "Prepare for Interviews",
                "description":
                    "Practice coding, technical and behavioral interview questions."
            }
        ]

    roadmap = []

    for index, skill in enumerate(gaps[:5]):

        roadmap.append({
            "title": f"Learn {skill}",
            "description":
                f"Study the fundamentals of {skill} and practice "
                f"with small hands-on exercises."
        })

    roadmap.append({
        "title": "Build a Real Project",
        "description":
            f"Create a practical project that combines your new "
            f"skills with your existing knowledge for {career}."
    })

    roadmap.append({
        "title": "Practice & Prepare",
        "description":
            "Solve practical problems, improve your portfolio and "
            "prepare for technical interviews."
    })

    return roadmap


def create_recommendations(gaps, career):

    recommendations = []

    if gaps:

        recommendations.append(
            "Learn one major skill at a time instead of trying to learn everything together."
        )

        recommendations.append(
            "Build a small project immediately after learning each important skill."
        )

        recommendations.append(
            "Use GitHub to document and showcase your projects."
        )

        recommendations.append(
            f"Practice projects related specifically to {career}."
        )

    else:

        recommendations.append(
            "Your current skills cover the basic detected requirements."
        )

        recommendations.append(
            "Focus on advanced projects and real-world problem solving."
        )

    return recommendations