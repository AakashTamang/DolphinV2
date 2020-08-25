import time
import glob
import cProfile, pstats, io
import os
import json
import concurrent.futures
import multiprocessing

import sys
sys.path.append("..")

from datareader import prepare_text,clean_text

from pipeline import NlpPipeline
# from word2vec import Word2VecScorer
import settings as cfg

# scorer = Word2VecScorer(cfg.word2vec_model)

java_path = r"C:\Program Files\Java\jdk-12.0.1\bin\java.exe"
os.environ['JAVAHOME'] = java_path

pr = cProfile.Profile()
pr.enable()

resume_content = prepare_text(r"C:\Users\Aakash\Desktop\Python\Scraping\Projects\Dolphwin_V2\dolphin\cvparser\datasets\resumes\Ananya Jain BA Pharma2.docx", dolower=False)
jd_content = prepare_text(r"C:\Users\Aakash\Desktop\Python\Scraping\Projects\Dolphwin_V2\dolphin\cvparser\datasets\jobs\Cyber Security.docx", dolower=False)
other_content = prepare_text(r"C:\Users\Aakash\Desktop\Python\Scraping\Projects\Dolphwin_V2\dolphin\cvparser\datasets\other\news.docx", dolower=False)

new_pipeline = NlpPipeline()

def test():
    new_pipeline.add_category_component()
    new_pipeline.add_segmentation_component()
    new_pipeline.add_profile_ner_parsing()
    new_pipeline.add_experience_academics_ner_parsing_component()
    new_pipeline.add_profile_pattern_matching()
    new_pipeline.add_skills_pattern_matching()
    new_pipeline.add_embedding_component()

    result = new_pipeline.process_text(resume_content)
    # result2 = new_pipeline.process_text(jd_content)
    # result3 = new_pipeline.process_text(other_content)

if __name__ == '__main__':
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.submit(test)
        # result = new_pipeline.process_text(resume_content)
        # result2 = new_pipeline.process_text(jd_content)
        # result3 = new_pipeline.process_text(other_content)


# new_pipeline.add_category_component()
# new_pipeline.add_segmentation_component()
# new_pipeline.add_profile_ner_parsing()
# new_pipeline.add_experience_academics_ner_parsing_component()
# new_pipeline.add_profile_pattern_matching()
# new_pipeline.add_skills_pattern_matching()
# new_pipeline.add_embedding_component()

# result = new_pipeline.process_text(resume_content)
# result2 = new_pipeline.process_text(jd_content)
# result3 = new_pipeline.process_text(other_content)

pr.disable()
s = io.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
with open(r'with_multi_processing_2.txt','w') as f:
    f.write(s.getvalue())

