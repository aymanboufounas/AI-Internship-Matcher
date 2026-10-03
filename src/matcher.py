from __future__ import annotations

import math
import re
from collections import Counter
from functools import lru_cache
from typing import Any

from .recommendations import build_recommendations
from .skill_extractor import extract_skills

TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9+#.-]{1,}")


def _tokens(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text or "")]


def lexical_cosine(text_a: str, text_b: str) -> float:
    a = Counter(_tokens(text_a))
    b = Counter(_tokens(text_b))
    if not a or not b:
        return 0.0
    dot = sum(value * b.get(token, 0) for token, value in a.items())
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


@lru_cache(maxsize=2)
def _load_model(model_name: str):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(model_name)


def semantic_similarity(
    text_a: str,
    text_b: str,
    model_name: str | None = "sentence-transformers/all-MiniLM-L6-v2",
) -> tuple[float, str]:
    if not text_a.strip() or not text_b.strip():
        return 0.0, "empty-input"

    if model_name:
        try:
            model = _load_model(model_name)
            embeddings = model.encode([text_a, text_b], normalize_embeddings=True)
            score = float(embeddings[0] @ embeddings[1])
            return max(0.0, min(1.0, score)), "sentence-transformers"
        except Exception:
            pass

    return lexical_cosine(text_a, text_b), "lexical-cosine"


def match_cv_to_job(
    cv_text: str,
    job_description: str,
    model_name: str | None = "sentence-transformers/all-MiniLM-L6-v2",
) -> dict[str, Any]:
    cv_skills = set(extract_skills(cv_text))
    required_skills = set(extract_skills(job_description))

    matched = sorted(cv_skills & required_skills, key=str.lower)
    missing = sorted(required_skills - cv_skills, key=str.lower)
    extra = sorted(cv_skills - required_skills, key=str.lower)

    semantic_score, engine = semantic_similarity(cv_text, job_description, model_name)
    skill_score = (len(matched) / len(required_skills)) if required_skills else semantic_score
    final_score = (0.70 * semantic_score) + (0.30 * skill_score)
    final_score = round(max(0.0, min(1.0, final_score)) * 100, 1)

    result: dict[str, Any] = {
        "match_score": final_score,
        "semantic_score": round(semantic_score * 100, 1),
        "skill_coverage": round(skill_score * 100, 1),
        "engine": engine,
        "matched_skills": matched,
        "missing_skills": missing,
        "additional_cv_skills": extra,
        "required_skills": sorted(required_skills, key=str.lower),
    }
    result["recommendations"] = build_recommendations(result)
    return result
