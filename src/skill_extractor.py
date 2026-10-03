from __future__ import annotations

import csv
import re
from functools import lru_cache
from pathlib import Path

DEFAULT_CATALOG = Path(__file__).resolve().parents[1] / "data" / "skills.csv"

FALLBACK_SKILLS = {
    "Python": ["python"],
    "Java": ["java"],
    "SQL": ["sql", "mysql", "postgresql", "sqlite"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning", "neural network", "neural networks"],
    "NLP": ["nlp", "natural language processing"],
    "Computer Vision": ["computer vision", "opencv"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "PyTorch": ["pytorch", "torch"],
    "TensorFlow": ["tensorflow", "keras"],
    "FastAPI": ["fastapi"],
    "Docker": ["docker"],
    "Git": ["git", "github"],
    "AWS": ["aws", "amazon web services"],
}


def _alias_pattern(alias: str) -> re.Pattern[str]:
    escaped = re.escape(alias.lower())
    return re.compile(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", re.IGNORECASE)


@lru_cache(maxsize=8)
def load_skill_catalog(path: str | None = None) -> dict[str, list[str]]:
    catalog_path = Path(path) if path else DEFAULT_CATALOG
    if not catalog_path.exists():
        return FALLBACK_SKILLS.copy()

    catalog: dict[str, list[str]] = {}
    with catalog_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            canonical = (row.get("canonical") or "").strip()
            aliases = [a.strip() for a in (row.get("aliases") or "").split("|") if a.strip()]
            if canonical:
                catalog[canonical] = aliases or [canonical]
    return catalog or FALLBACK_SKILLS.copy()


def extract_skills(text: str, catalog_path: str | None = None) -> list[str]:
    if not text:
        return []
    haystack = text.lower()
    found: list[str] = []
    for canonical, aliases in load_skill_catalog(catalog_path).items():
        candidates = {canonical, *aliases}
        if any(_alias_pattern(alias).search(haystack) for alias in candidates):
            found.append(canonical)
    return sorted(found, key=str.lower)
