import unittest

from src.matcher import lexical_cosine, match_cv_to_job


class MatcherTests(unittest.TestCase):
    def test_identical_text_has_high_similarity(self):
        text = "python machine learning sql fastapi"
        self.assertAlmostEqual(lexical_cosine(text, text), 1.0, places=6)

    def test_match_returns_skill_gap(self):
        cv = "Python developer with SQL and Git experience."
        job = "Looking for Python, SQL, Git and Docker for a machine learning internship."
        result = match_cv_to_job(cv, job, model_name=None)
        self.assertIn("Docker", result["missing_skills"])
        self.assertIn("Python", result["matched_skills"])
        self.assertGreater(result["match_score"], 0)


if __name__ == "__main__":
    unittest.main()
