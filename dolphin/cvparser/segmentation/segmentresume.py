import pickle
# import sys
# sys.path.append("..")
from settings import ResumeSegmentationModelPath

class ResumeSegmentCreator:
    """
    Class to segment resume details
    """
    def __init__(self):
        '''
        Initializes major attributes for segmentation
        '''
        self.personal_info = set("profile: profile information personal information additional information information: informations: introduction introduction:".split(' '))
        self.objective = set("summary career summary goal goal: summary: Summary: summary career objective objective: motivation motivation:".split(' '))
        self.skills = set("technical skills key mainfiles professional practical skill"
                          " skill: skills skills skills:"
                          " competencies competencies:".split(' '))
        self.experiences = set("work job projects summary jobs practical"
                               " responsibilities responsibilities: employment "
                               "professional career experience experience: "
                               "experiences experiences: profile Work Experience"
                               " profile: profiles profiles:".split(' '))
        self.projects = set("training training: trainings trainings: college projects "
                            "projects: training trainings: attended attended:".split(' '))
        self.academics = set("education certificate certificates certifications certification education: educational academic qualification"
                             " qualification: qualifications qualifications:".split(' '))
        self.rewards = set("certification certification: certifications "
                           "certifications rewards rewards:License License"
                           " honours awards Licenses Licenses:".split(' '))
        self.languages = set("language language: languages languages:".split(' '))
        self.references = set("reference reference: references references:".split(' '))

        self.links = set('links links: link link:'.split(' '))

        self.possible_title_keywords = self.personal_info | self.objective | self.experiences |\
                                       self.skills | self.projects | self.academics | self.rewards |\
                                       self.languages | self.references | self.links

        with open(ResumeSegmentationModelPath ,'rb') as pkl:
            self.gaussian = pickle.load(pkl)


    def unique_index_headings(self):
        '''
        This method uses the whole document and exract the possible title headings form it.

        :returns: headings along with its index
        '''
        # Split text for heading extraction
        sent_lines = self.text.splitlines()
        list_of_headings_with_repeated_index = []
        # get sentence and its sentence index in resume document.
        for index, sent in enumerate(sent_lines):
            sent = sent.split(" ")
            sent = [x.strip() for x in sent if x.strip()]
            if len(sent) < 4:
              
                for word in sent:
                    
                    features = [word.istitle() | word.isupper(), word.islower(), word.isupper(), word.endswith(":"),
                                len(word) <= 3, word.lower() in self.possible_title_keywords]

                    features = [[int(elem) for elem in features]]
                    #                 predict if word with above features is heading
                    
                    if self.gaussian.predict(features) == 1:
                        list_of_headings_with_repeated_index.append({index: word})
        
        # from repeating index heading, join heading words with same sentence index
        
        uniquekeys = set()
        unique_indx_headings = dict()
        # titles_with_repeated_indices = predict_repeating_index_headings(input_text)
      
        for t in list_of_headings_with_repeated_index:
            for key, value in t.items():
                if key not in uniquekeys:
                    unique_indx_headings[key] = value
                    uniquekeys.add(key)
                else:
                    unique_indx_headings[key] = unique_indx_headings[key] + ' ' + value
        
        return unique_indx_headings

    def sliced_resume_text(self):
        '''
        This method uses the headings and its indexes to extract the information and store on those headings.

        :returns: A dictionary with the headings and its respective information
        '''
        #resume_text = self.text
    	
        sent_lines = self.text.splitlines()

        # index of last line of the resume
        end_index = len(sent_lines)
        sliced_text = {}
        unique_index_heading_title = self.unique_index_headings()
        #list of indices of heading titles, will be used for slicing of resume text
        list_of_title_indices = list(unique_index_heading_title)
       
        # add last index of sentence splited resume to slice the last section of resume
        list_of_title_indices.append(end_index)
        
        # i=0 initialization is required to slice resume text from index-0 to first heading index of resume
        # which is in most cases, the personal information of the candidate
        i = 0
        sliced_text["profile information"] = sent_lines[0:list_of_title_indices[0]]
        for key, value in unique_index_heading_title.items():
            #for i in range(len(list_of_title_indices)-1):
            # sliced_text["profile information"] = sent_lines[0:list_of_title_indices[0]]
            sliced = sent_lines[list_of_title_indices[i] + 1:list_of_title_indices[i + 1]]
            if value in sliced_text.keys():
                sliced_text[value].append('\n'.join(sliced))
            else:
                sliced_text[value] = sliced
            #sliced_text.append(value: sliced)
            i += 1
        
        return sliced_text

    def format_segment(self,text):
        '''
        This method uses the document and segments it onto different parts like profile information, experience, academics etc.

        :param text: A cleaned document
        :returns: A dictionary containing the segmented result
        '''
        self.text = text
        Profile = []
        Objectives = []
        Experiences = []
        Skills = []
        Projects = []
        Educations = []
        Rewards = []
        Languages = []
        References = []
        Links = []

        pharsed_info = self.sliced_resume_text()

        for k, v in pharsed_info.items():
            if len(set(k.lower().split())) == len(self.personal_info.intersection(set(k.lower().split()))):
                Profile.extend(v)
            elif len(set(k.lower().split())) == len(self.objective.intersection(set(k.lower().split()))):
                Objectives.extend(v)
            elif len(set(k.lower().split())) == len(self.skills.intersection(set(k.lower().split()))):
                Skills.extend(v)
            elif len(set(k.lower().split())) == len(self.experiences.intersection(set(k.lower().split()))):
                Experiences.extend(v)
            elif len(set(k.lower().split())) == len(self.languages.intersection(set(k.lower().split()))):
                Languages.extend(v)
            elif len(set(k.lower().split())) == len(self.projects.intersection(set(k.lower().split()))):
                Projects.extend(v)
            elif len(set(k.lower().split())) == len(self.academics.intersection(set(k.lower().split()))):
                Educations.extend(v)
            elif len(set(k.lower().split())) == len(self.rewards.intersection(set(k.lower().split()))):
                Rewards.extend(v)
            elif len(set(k.lower().split())) == len(self.references.intersection(set(k.lower().split()))):
                References.extend(v)
            elif len(set(k.lower().split())) == len(self.links.intersection(set(k.lower().split()))):
                Links.extend(v)
            else:
                pass

        resume_info_extracted = {'profile':' '.join(Profile),
                                 'objectives':' '.join(Objectives),
                                 'experiences':'\n'.join(Experiences),
                                 'skills':' '.join(Skills),
                                 'projects':' '.join(Projects),
                                 'academics':'\n'.join(Educations),
                                 'rewards': ' '.join(Rewards),
                                 'languages':' '.join(Languages),
                                 'references':' '.join(References),
                                 'links':' '.join(Links),
                                 }
      

        return resume_info_extracted



