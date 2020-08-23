import sys
sys.path.append("..")
import pandas as pd
from find_job_titles import FinderAcora
from datareader import prepare_text
from collections import Counter




domain_comparision_df = pd.read_csv('domain_class_data.tsv', sep="\t")
domain_comparision_df['designations'] = domain_comparision_df['designations'].str.lower()


finder = FinderAcora()
sample_jd_text = prepare_text(
    "/home/shushant/Desktop/Job Description Collection/Data Scientist 7.docx", dolower=False)

designations = finder.findall(sample_jd_text)
designations_list = set([desig.match for desig in designations])
desig = [desig.lower() for desig in designations_list]
print(desig)
required_df = domain_comparision_df.loc[domain_comparision_df['designations'].isin(
    desig)]
domains = required_df['domain'].tolist()
most_common_domain= [word for word, word_count in Counter(domains).most_common(1)]
print(most_common_domain)
