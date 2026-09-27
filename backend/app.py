from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai_analyzer import analyze_learning_gap


app = FastAPI(
    title="LearnGap AI",
    description="AI-powered personalized learning gap analyzer",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class AnalysisRequest(BaseModel):
    skills: str
    career: str
    level: str = "Beginner"


@app.get("/")
def home():

    return {
        "message": "LearnGap AI API is running",
        "status": "online"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/analyze")
def analyze(request: AnalysisRequest):

    result = analyze_learning_gap(
        request.skills,
        request.career,
        request.level
    )

    return result