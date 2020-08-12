import unittest
import logging

import spacy


import dolphin.settings as cfg

from dolphin.document_categorization.identify_resume import categorize_document
from dolphin.datareader import prepare_text

class Testing(unittest.TestCase):

    def test_resume_document(self):
        #testing resume
        content_resume = prepare_text("/home/shushant/Desktop/data_resume/Aakriti_QA.docx")
        category = categorize_document(content_resume)
        self.assertEqual('resume',category)

    def test_job_description_document(self):
        # testing job description
        content_job_description = prepare_text("/home/shushant/Desktop/jd2/Cyber Security 14.docx")
        category = categorize_document(content_job_description)
        self.assertEqual("job_description",category)
    
    def test_other_files_document(self):
        # testing other files
        content_other_files = prepare_text("/home/shushant/Desktop/NLP Syllabus.docx")
        category = categorize_document(content_other_files)
        self.assertEqual("others",category)



if __name__ ==  "__main__":
    unittest.main()