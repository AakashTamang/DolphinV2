import unittest

from dolphin.segmentation.segmentresume import ResumeSegmentCreator
from dolphin.datareader import prepare_text

segmentation_obj = ResumeSegmentCreator()

class TestSegmentation(unittest.TestCase):

    def test_segmentation_resume(self):
        resume_content = prepare_text("/home/shushant/Desktop/data_resume/Aakriti_QA.docx")
        segmented_content = segmentation_obj.format_segment(resume_content)
        self.assertIsNotNone(segmented_content)

if __name__ ==  "__main__":
    unittest.main()