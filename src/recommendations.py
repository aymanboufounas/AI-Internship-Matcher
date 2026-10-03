from __future__ import annotations

from typing import Any


def build_recommendations(result: dict[str, Any]) -> list[str]:
    suggestions: list[str] = []
    missing = result.get("missing_skills", [])
    semantic = float(result.get("semantic_score", 0))
    coverage = float(result.get("skill_coverage", 0))

    if missing:
        shown = ", ".join(missing[:6])
        suggestions.append(
            f"If you genuinely have experience with them, make these job-relevant skills explicit on your CV: {shown}."
        )
    if coverage < 60:
        suggestions.append(
            "Move the most relevant technical skills and projects closer to the top of the CV so recruiters can verify fit quickly."
        )
    if semantic < 55:
        suggestions.append(
            "Rewrite project bullets using the role's terminology, while keeping every claim accurate and evidence-based."
        )
    suggestions.append(
        "Quantify impact where possible (dataset size, model metric, latency, users, time saved, or accuracy improvement)."
    )
    suggestions.append(
        "Add one concise project bullet that explains the problem, your technical contribution, and the measurable result."
    )
    return suggestions[:5]
