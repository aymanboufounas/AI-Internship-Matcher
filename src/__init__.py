"""Core package for AI Internship Matcher."""

from .matcher import match_cv_to_job
from .skill_extractor import extract_skills

__all__ = ["match_cv_to_job", "extract_skills"]
