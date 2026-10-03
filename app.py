from __future__ import annotations

import streamlit as st

from src.cv_parser import extract_text_from_bytes
from src.matcher import match_cv_to_job

st.set_page_config(page_title="AI Internship Matcher", page_icon="🎯", layout="wide")

st.title("🎯 AI Internship Matcher")
st.caption("Compare a CV with an internship or job description using semantic AI + transparent skill coverage.")

with st.sidebar:
    st.header("Matching engine")
    engine = st.radio(
        "Choose mode",
        ["Semantic AI", "Fast local"],
        help="Semantic AI uses Sentence Transformers. Fast local uses deterministic lexical cosine similarity.",
    )
    st.info("No API key is required. The semantic model is downloaded on first use.")

left, right = st.columns(2)
with left:
    uploaded = st.file_uploader("Upload your CV", type=["pdf", "docx", "txt", "md"])
    cv_text_manual = st.text_area("Or paste CV text", height=280, placeholder="Paste CV text here...")
with right:
    job_description = st.text_area(
        "Internship / job description",
        height=355,
        placeholder="Paste the full role description, requirements, and responsibilities...",
    )

if st.button("Analyze match", type="primary", use_container_width=True):
    cv_text = cv_text_manual.strip()
    if uploaded is not None:
        try:
            cv_text = extract_text_from_bytes(uploaded.getvalue(), uploaded.name)
        except Exception as exc:
            st.error(f"Could not read CV: {exc}")
            st.stop()

    if not cv_text or not job_description.strip():
        st.warning("Please provide both a CV and a job description.")
        st.stop()

    model_name = "sentence-transformers/all-MiniLM-L6-v2" if engine == "Semantic AI" else None
    with st.spinner("Analyzing semantic fit and skills..."):
        result = match_cv_to_job(cv_text, job_description, model_name=model_name)

    score_col, semantic_col, coverage_col = st.columns(3)
    score_col.metric("Overall match", f"{result['match_score']}%")
    semantic_col.metric("Semantic similarity", f"{result['semantic_score']}%")
    coverage_col.metric("Skill coverage", f"{result['skill_coverage']}%")
    st.progress(int(result["match_score"]))
    st.caption(f"Engine used: {result['engine']}")

    overview, skills, advice = st.tabs(["Overview", "Skills", "Recommendations"])
    with overview:
        st.subheader("How the score works")
        st.write("70% semantic similarity + 30% explicit job-skill coverage. The score is guidance, not a hiring decision.")
        with st.expander("Extracted CV text"):
            st.text(cv_text[:10000])
    with skills:
        a, b = st.columns(2)
        with a:
            st.success("Matched skills")
            st.write(", ".join(result["matched_skills"]) or "No catalogued skills matched yet.")
        with b:
            st.warning("Missing from CV")
            st.write(", ".join(result["missing_skills"]) or "No catalogued required skills are missing.")
        st.info("Additional CV skills: " + (", ".join(result["additional_cv_skills"]) or "None detected"))
    with advice:
        for item in result["recommendations"]:
            st.write(f"- {item}")
