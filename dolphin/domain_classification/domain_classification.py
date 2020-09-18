import sys
sys.path.append("..")
# sys.path.append("/home/shushant/Desktop/dolphin_repos/DolphinV2/dolphin/job_parsing")
from collections import Counter
from datareader import prepare_text
import pandas as pd
from job_parsing.jd_parsing import SpacyNer
import settings as cfg


jd_parsing_obj = SpacyNer()


class DomainClassification:
    def __init__(self):
        self.domain_comparision_df = pd.read_csv(
            cfg.domain_class_data, sep="\t")

    def clean_classify_document(self,file_path):
        cleaned_document = prepare_text(file_path,dolower=False)
        classified_domain = self.classify(cleaned_document)
        json_data = {
            "DOMAIN":classified_domain
            }
        return json_data

    def classify(self, file_content):
        self.domain_comparision_df['designations'] = self.domain_comparision_df['designations'].str.lower()
        # print(self.domain_comparision_df.head(n=5))
        designations, organization, experience, education, location_ = jd_parsing_obj.parse(file_content)
        print("All--->",designations)
        designations = [item for sublist in designations for item in sublist]
        # desig = [desig.lower() for desig in designations]
        print("Designation extracted -->", designations)
        if designations:
            required_df = self.domain_comparision_df.loc[self.domain_comparision_df['designations'].isin(
                designations)]
            domains = required_df['domain'].tolist()
            most_common_domain = [word for word,
                                word_count in Counter(domains).most_common(1)]
        else:
            return "No Designation Found"

        return most_common_domain

    def classify_domain_from_designation(self,designations):
        """
        give the domain of the job when designations are given
        """
        self.domain_comparision_df['designations'] = self.domain_comparision_df['designations'].str.lower()
        required_df = self.domain_comparision_df.loc[self.domain_comparision_df['designations'].isin(
            designations)]
        domains = required_df['domain'].tolist()
        most_common_domain = [word for word,
                            word_count in Counter(domains).most_common(1)]
        return most_common_domain



# if __name__ == "__main__":
#     # sample_jd_text = prepare_text(
#     #     r"C:\Users\Aakash\Desktop\Python\Scraping\Projects\job_descriptions\Data Scientist.docx", dolower=False)
#     domain_classification_obj = DomainClassification()
#     sample_designations = ['Software Test Engineer']
#     sample_designations = [x.lower() for x in sample_designations]
#     most_common_domain = domain_classification_obj.classify_domain_from_designation(sample_designations)
#     print("Domain_classified-->", most_common_domain)
