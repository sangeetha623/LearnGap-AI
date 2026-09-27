# LearnGap AI 🤖

LearnGap AI is an AI-powered personalized learning assistant that helps students identify the skills they are missing for their target career.

## Problem

Students often learn many technologies without knowing which skills are actually required for their desired career.

LearnGap AI solves this by comparing:

- Current Skills
- Target Career
- Experience Level

and generating a personalized learning roadmap.

## Features

### 1. Skill Gap Detection

Identifies skills that are missing for the selected career.

### 2. Personalized Roadmap

Creates a step-by-step learning plan.

### 3. Career Analysis

Analyzes the user's current skills against their target role.

### 4. AI Recommendations

Provides practical recommendations for learning and project building.

### 5. Modern Responsive UI

Works on:

- Laptop
- Desktop
- Mobile

## Tech Stack

Frontend:

- HTML
- CSS
- JavaScript

Backend:

- Python
- FastAPI

AI:

- Google Gemini API

## Folder Structure

LearnGap-AI/

    index.html
    style.css
    script.js

    backend/
        app.py
        ai_analyzer.py
        requirements.txt
        .env

    README.md

## Installation

Open terminal inside the backend folder.

Install dependencies:

    pip install -r requirements.txt

## Run Backend

Run:

    uvicorn app:app --reload

The backend will start at:

    http://127.0.0.1:8000

## API

Health check:

    GET /health

Learning analysis:

    POST /analyze

Example request:

    {
        "skills": "Python, HTML, CSS",
        "career": "Full Stack Developer",
        "level": "Beginner"
    }

## Example Output

The AI can return:

- Current skills
- Skill gaps
- Target role
- Career message
- Learning roadmap
- Recommendations

## Future Improvements

- Resume upload
- GitHub profile analysis
- Job description analysis
- Course recommendations
- Skill progress tracking
- AI interview preparation
- Learning progress dashboard
- Personalized project recommendations

## Team

LearnGap AI
AI-powered learning gap detection platform.