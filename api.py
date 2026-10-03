from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.matcher import match_cv_to_job

app = FastAPI(
    title="AI Internship Matcher API",
    version="1.0.0",
    description="Semantic CV-to-job matching with transparent skill-gap analysis.",
)


class MatchRequest(BaseModel):
    cv_text: str = Field(min_length=20)
    job_description: str = Field(min_length=20)
    use_transformer: bool = True


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/match")
def match(payload: MatchRequest) -> dict:
    model_name = "sentence-transformers/all-MiniLM-L6-v2" if payload.use_transformer else None
    return match_cv_to_job(payload.cv_text, payload.job_description, model_name=model_name)
