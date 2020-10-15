import unittest
import logging

import spacy

import dolphin.settings as cfg

from dolphin.job_parsing import SpacyNer
from dolphin.datareader import prepare_text

parsing_obj = SpacyNer()

class Test_Jd_Parsing(unittest.TestCase):
    def jdparsing(self):
        jd_content = prepare_text(r"C:\Users\zerad\Documents\Data Analyst 9.docx")
        parsed_jd = parsing_obj.format_segment(jd_content)
        self.assertIsNotNone(parsed_jd)


if __name__ ==  "__main__":
    unittest.main()