import nltk
from .formatdata import formatEducationalinfo,formatExperienceinfo,cleandata

def gather_ner(tagged_tuples,ner='DESIG'):
    temp_container = list()
    all_entities = list()
    for word, tag in tagged_tuples:
        if tag == ner:
            temp_container.append(word)
        else:
            if temp_container:
                all_entities.append(' '.join(temp_container))
                temp_container = list()
    if temp_container:
        all_entities.append(' '.join(temp_container))
    return all_entities



class StanfordNER:

    ###----<NER model that chooses the particular model and parser>----###
    @staticmethod
    def ner_parser(model,text,mode):
        words = nltk.word_tokenize(text)
        parser = {
                'profile':StanfordNER.personal_info_parser,
                'academics':StanfordNER.education_parser,
                'experience':StanfordNER.experience_parser,
                'experience_academics':StanfordNER.experience_academics_parser,
                }

        tagged_tuples = model.tag(words)
        return parser[mode](tagged_tuples,text)


    @staticmethod
    def experience_academics_parser(tagged_tuples,text):
        
        alldegree = []
        alllocations = []
        alldate = []
        alluniversity = []
        deg_container = []
        loc_container = []
        date_container = []
        university_container = []
        for word,tag in tagged_tuples:
            if tag == 'DEG':
                deg_container.append(word)
            else:
                if deg_container:
                    degree = ' '.join(deg_container)
                    alldegree.append(degree)
                    deg_container = []
            if tag == 'LOC':
                loc_container.append(word)
            else:
                if loc_container:
                    location = ' '.join(loc_container)
                    loc_container = []
                    alllocations.append(location)
            if tag == 'DATE':
                date_container.append(word)
            else:
                if date_container:
                    date = ' '.join(date_container)
                    alldate.append(date)
                    date_container = []
            if tag == 'UNI':
                university_container.append(word)
            else:
                if university_container:
                    university = ' '.join(university_container)
                    university_container = []
                    alluniversity.append(university)

        if loc_container:
            alllocations.append(' '.join(loc_container))

        if date_container:
            alldate.append(' '.join(date_container))

        if university_container:
            alluniversity.append(' '.join(university_container))

        if deg_container:
            alldegree.append(' '.join(deg_container))

        sent_tokens = text.split('\n')
        sent2indx = {}
        item_tracker = {}
        for index, sentence in enumerate(sent_tokens):
            cleaned_sentence = cleandata(sentence)
            if cleaned_sentence not in sent2indx:
                sent2indx.update({cleaned_sentence: index})
                item_tracker.update({cleaned_sentence: 1})

            else:

                sent2indx.update({cleaned_sentence + '{}'.format(item_tracker[cleaned_sentence]): index})
                item_tracker[cleaned_sentence] += 1
        academics = formatEducationalinfo(
                                          sent_tokens, sent2indx, alldegree,
                                          alluniversity, alldate, alllocations
                                          )

        
        # EXPERIENCE
        i = 0
        o_counter = 0
        all_unformatted_information =[]
        desig_container = []
        date_container = []
        org_container = []
        loc_container = []
        formatted_data={}

        for word,tag in tagged_tuples:

            if tag == "DESIG":
                desig_container.append(word)
            else:
                if desig_container:
                    designation =' '.join(desig_container)
                    all_unformatted_information.append((designation,'DESIG'))
                    desig_container=[]

            if tag == "DATE":
                date_container.append(word)
            else:
                if date_container:
                    date = ' '.join(date_container)
                    all_unformatted_information.append((date,"DATE"))
                    date_container=[]

            if tag == "ORG":
                org_container.append(word)
            else:
                if org_container:
                    org = ' '.join(org_container)
                    all_unformatted_information.append((org,'ORG'))
                    org_container = []


            if tag == "LOC":
                loc_container.append(word)
            else:
                if loc_container:
                    loc = ' '.join(loc_container)
                    all_unformatted_information.append((loc,"LOC"))
                    loc_container = []
        if desig_container:
            all_unformatted_information.append((' '.join(desig_container),'DESIG'))
        if date_container:
            all_unformatted_information.append((' '.join(date_container),'DATE'))
        if loc_container:
            all_unformatted_information.append((' '.join(loc_container),'LOC'))
        if org_container:
            all_unformatted_information.append((' '.join(org_container),'ORG'))

        i = 0
        formatted_data ={}
        temp_dict_container = {}
        discovered_tag = []
        tag_selector ={'DESIG':'Designation',
                       'LOC':'location',
                       'ORG':'Company'}
        for value,tag in all_unformatted_information:
            if tag not in discovered_tag:
                discovered_tag.append(tag)
                if tag!="DATE":
                    temp_dict_container[tag_selector[tag]]=value
                else:
                    temp_dict_container['entry_date'] = value
                if (value,tag) == all_unformatted_information[-1]:
                    i += 1
                    discovered_tag = []
                    formatted_data.update({f"Exp{i}":temp_dict_container})
            else:
                if tag =="DATE":
                    temp_dict_container['exit_value']=value
                else:
                    i+=1
                    discovered_tag = []
                    formatted_data.update({'Exp{}'.format(i):temp_dict_container})
                    temp_dict_container={}
                    discovered_tag.append(tag)
                    # discovered_tag.append(tag_selector[tag])
                    temp_dict_container[tag_selector[tag]]=value


        return formatted_data, academics

    @staticmethod
    def experience_parser(tagged_tuples,text):
        i = 0
        o_counter = 0
        all_unformatted_information =[]
        desig_container = []
        date_container = []
        org_container = []
        loc_container = []
        formatted_data={}

        for word,tag in tagged_tuples:

            if tag == "DESIG":
                desig_container.append(word)
            else:
                if desig_container:
                    designation =' '.join(desig_container)
                    all_unformatted_information.append((designation,'DESIG'))
                    desig_container=[]

            if tag == "DATE":
                date_container.append(word)
            else:
                if date_container:
                    date = ' '.join(date_container)
                    all_unformatted_information.append((date,"DATE"))
                    date_container=[]

            if tag == "ORG":
                org_container.append(word)
            else:
                if org_container:
                    org = ' '.join(org_container)
                    all_unformatted_information.append((org,'ORG'))
                    org_container = []


            if tag == "LOC":
                loc_container.append(word)
            else:
                if loc_container:
                    loc = ' '.join(loc_container)
                    all_unformatted_information.append((loc,"LOC"))
                    loc_container = []
        if desig_container:
            all_unformatted_information.append((' '.join(desig_container),'DESIG'))
        if date_container:
            all_unformatted_information.append((' '.join(date_container),'DATE'))
        if loc_container:
            all_unformatted_information.append((' '.join(loc_container),'LOC'))
        if org_container:
            all_unformatted_information.append((' '.join(org_container),'ORG'))

        i = 0
        formatted_data ={}
        temp_dict_container = {}
        discovered_tag = []
        tag_selector ={'DESIG':'Designation',
                       'LOC':'location',
                       'ORG':'Company'}
        for value,tag in all_unformatted_information:
            if tag not in discovered_tag:
                discovered_tag.append(tag)
                if tag!="DATE":
                    temp_dict_container[tag_selector[tag]]=value
                else:
                    temp_dict_container['entry_date'] = value
                if (value,tag) == all_unformatted_information[-1]:
                    i += 1
                    discovered_tag = []
                    formatted_data.update({f"Exp{i}":temp_dict_container})
            else:
                if tag =="DATE":
                    temp_dict_container['exit_value']=value
                else:
                    i+=1
                    discovered_tag = []
                    formatted_data.update({'Exp{}'.format(i):temp_dict_container})
                    temp_dict_container={}
                    discovered_tag.append(tag)
                    # discovered_tag.append(tag_selector[tag])
                    temp_dict_container[tag_selector[tag]]=value


        # alldesignation = gather_ner(tagged_tuples,ner="DESIG")
        # allcompany = gather_ner(tagged_tuples,ner="ORG")
        # alldate = gather_ner(tagged_tuples,ner="DATE")
        # alllocations = gather_ner(tagged_tuples,ner="LOC")
        # allroles =[]
        # roles_container = []
        # for word,tag in tagged_tuples:
        #     if tag == 'O':
        #         o_counter += 1
        #         roles_container.append(word)
        #     else:
        #         if o_counter > 10:
        #             role = ' '.join(roles_container[1:])
        #             roles_container = []
        #             o_counter = 0
        #             allroles.append(role)
        # sent_tokens = text.split('\n')
        # sent2indx = {}
        # item_tracker = {}

        # for index,sentence in enumerate(sent_tokens):
        #     cleaned_sentence = cleandata(sentence)
        #     if cleaned_sentence not in sent2indx:
        #         sent2indx.update({cleaned_sentence:index})
        #         item_tracker.update({cleaned_sentence:1})

        #     else:

        #         sent2indx.update({cleaned_sentence+'{}'.format(item_tracker[cleaned_sentence]):index})
        #         item_tracker[cleaned_sentence] += 1


        
        # experiences = formatExperienceinfo(sent_tokens,sent2indx,alldesignation,
        #                                   allcompany,alldate,alllocations,allroles)
        return formatted_data



    @staticmethod
    def education_parser(tagged_tuples,text):
        alldegree = []
        alllocations = []
        alldate = []
        alluniversity = []
        deg_container = []
        loc_container = []
        date_container = []
        university_container = []
        for word,tag in tagged_tuples:
            if tag == 'DEG':
                deg_container.append(word)
            else:
                if deg_container:
                    degree = ' '.join(deg_container)
                    alldegree.append(degree)
                    deg_container = []
            if tag == 'LOC':
                loc_container.append(word)
            else:
                if loc_container:
                    location = ' '.join(loc_container)
                    loc_container = []
                    alllocations.append(location)
            if tag == 'DATE':
                date_container.append(word)
            else:
                if date_container:
                    date = ' '.join(date_container)
                    alldate.append(date)
                    date_container = []
            if tag == 'UNI':
                university_container.append(word)
            else:
                if university_container:
                    university = ' '.join(university_container)
                    university_container = []
                    alluniversity.append(university)

        if loc_container:
            alllocations.append(' '.join(loc_container))

        if date_container:
            alldate.append(' '.join(date_container))

        if university_container:
            alluniversity.append(' '.join(university_container))

        if deg_container:
            alldegree.append(' '.join(deg_container))

        sent_tokens = text.split('\n')
        sent2indx = {}
        item_tracker = {}
        for index, sentence in enumerate(sent_tokens):
            cleaned_sentence = cleandata(sentence)
            if cleaned_sentence not in sent2indx:
                sent2indx.update({cleaned_sentence: index})
                item_tracker.update({cleaned_sentence: 1})

            else:

                sent2indx.update({cleaned_sentence + '{}'.format(item_tracker[cleaned_sentence]): index})
                item_tracker[cleaned_sentence] += 1
        academics = formatEducationalinfo(
                                          sent_tokens, sent2indx, alldegree,
                                          alluniversity, alldate, alllocations
                                          )
        return academics




    @staticmethod
    def personal_info_parser(tagged_tuples,text):
        name = 'Anonymous'
        address = []
        possible_name = []
        possible_address = []

        for word, tag in tagged_tuples:
            if tag == "PER":
                possible_name.append(word)
            else:
                if possible_name:
                    name = (" ".join(possible_name)).lower()
                    possible_name = []

            if tag == "LOC":
                possible_address.append(word)
            else:
                if possible_address:
                    address.append(" ".join(possible_address))
                    possible_address = []
        final_address = list(set(address))
        formatted_name = name.title()
        return formatted_name, final_address
