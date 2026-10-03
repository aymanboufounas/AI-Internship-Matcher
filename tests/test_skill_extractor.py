import unittest

from src.skill_extractor import extract_skills


class SkillExtractorTests(unittest.TestCase):
    def test_aliases_and_boundaries(self):
        text = "Built ML models with Python, sklearn, PostgreSQL and OpenCV."
        skills = extract_skills(text)
        self.assertIn("Python", skills)
        self.assertIn("Machine Learning", skills)
        self.assertIn("Scikit-learn", skills)
        self.assertIn("SQL", skills)
        self.assertIn("Computer Vision", skills)


if __name__ == "__main__":
    unittest.main()
