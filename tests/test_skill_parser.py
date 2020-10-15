import unittest
import logging

import spacy

import dolphin.settings as cfg

from dolphin.job_parsing.skill_parser import technical_skills_parser, soft_skills_parser
from dolphin.datareader import prepare_text

class TestSkillParsing(unittest.TestCase):
    def testing_skill_parse(self):
        jd_content = prepare_text(r"C:\Users\zerad\Documents\Data Analyst 9.docx")
        self.assertIsNotNone(jd_content)


if __name__ ==  "__main__":
    unittest.main()
