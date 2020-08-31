import sys
sys.path.append("..")
sys.path.append("/home/shushant/Desktop/dolphin_repos/DolphinV2/dolphin/job_parsing")
from collections import Counter
from datareader import prepare_text
import pandas as pd
from job_parsing.jd_parsing import SpacyNer



jd_parsing_obj = SpacyNer()


class DomainClassification:
    def __init__(self):
        self.domain_comparision_df = pd.read_csv(
            'domain_class_data.tsv', sep="\t")

    def classify(self, file_content):
        self.domain_comparision_df['designations'] = self.domain_comparision_df['designations'].str.lower(
        )
        print(self.domain_comparision_df.head(n=5))
        designations, organization, experience, education, location_ = jd_parsing_obj.parse(file_content)
        print("Alll--->",designations)
        designations = [item for sublist in designations for item in sublist]
        desig = [desig.lower() for desig in designations]
        print("Designation extracted -->", desig)
        required_df = self.domain_comparision_df.loc[self.domain_comparision_df['designations'].isin(
            desig)]
        print(required_df.head())
        domains = required_df['domain'].tolist()
        print("Domans",domains)
        most_common_domain = [word for word,
                              word_count in Counter(domains).most_common(1)]

        return most_common_domain


if __name__ == "__main__":
    sample_jd_text = prepare_text(
        "/home/shushant/Desktop/Job Description Collection/Network Engineer Job Description 15.docx", dolower=False)
    domain_classification_obj = DomainClassification()
    most_common_domain = domain_classification_obj.classify(sample_jd_text)
    print("Domain_classified-->", most_common_domain)
