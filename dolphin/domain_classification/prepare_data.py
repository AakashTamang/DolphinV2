import sys
sys.path.append("..")
from os import walk
import os
from find_job_titles import FinderAcora
from datareader import prepare_text


finder = FinderAcora()

job_descriptions_data_path = "/home/shushant/Desktop/Job Description Collection/"
jd_files = [filenames for (dirpath, dirnames, filenames)
            in walk(job_descriptions_data_path)][0]
jd_files_path = [job_descriptions_data_path +
                 '/' + filename for filename in jd_files]

with open("designation.txt", "w") as file:
    for jd in jd_files_path:
        sample_jd_text = prepare_text(jd, dolower=False)
        try:
            designations = finder.findall(sample_jd_text)
        except:
            print(sample_jd_text)
            pass
        # print(designations)
        # print(type(designations))
        designations_list = set([desig.match for desig in designations])
        # print(designations_list)
        for desig in designations_list:
            file.write(desig + "\n")
