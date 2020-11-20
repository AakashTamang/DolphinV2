import unittest
from dolphin.datareader import prepare_text,prepare_text_from_string,clean_text,pdf_to_text,docx_to_text


class TestReadingMethods(unittest.TestCase):

    def test_clean_text(self):
        cleaned_text = clean_text('How is it तपाई लाई कस्तो छ going on',False)
        self.assertEqual(cleaned_text,'How is it     going on')
                                              
    def test_pdf_to_text(self):
        extracted_text_from_pdf = pdf_to_text(r'C:\Users\zerad\Documents\SujanAdhikari_resume.pdf',False)
        self.assertIsNotNone(extracted_text_from_pdf)
    
    def test_docx_to_test(self):
        extracted_text_from_docx = docx_to_text(r'C:\Users\zerad\Documents\Data Analyst 9.docx',False)
        self.assertIsNotNone(extracted_text_from_docx)

    def test_prepare_text_from_string(self):
        result = prepare_text_from_string('This is the first sentence to be cleaned', dolower=True)
        self.assertEqual('this is the first sentence to be cleaned',result)
    
    def test_prepare_text(self):
        self.assertIsNotNone(prepare_text(r'C:\Users\zerad\Documents\SujanAdhikari_resume.pdf',False))
        self.assertIsNotNone(prepare_text(r'C:\Users\zerad\Documents\Data Analyst 9.docx',False))

if __name__ ==  "__main__":
    unittest.main()