import copy


class matcher():

    def __init__(self,oneJD_MultipleRes_Score,oneRes_MultipleJD_Score):
        self.oneJD_MultipleRes_Score = oneJD_MultipleRes_Score
        self.oneRes_MultipleJD_Score = oneRes_MultipleJD_Score
    
    def prefs(self,scores):
        preferences = {}
        for i in range(len(scores.keys())): 
            id = list(scores.keys())[i]
            listValues = list(scores.values())[i]
            preferences[id] = [k for k, v in sorted(listValues.items(), key=lambda item: item[1])][::-1]
        return preferences
    
    def matchmaker(self):

        employerPrefs = self.prefs(self.oneJD_MultipleRes_Score)
        candidatePrefs = self.prefs(self.oneRes_MultipleJD_Score)

        employer = sorted(employerPrefs.keys())
        # candidate = sorted(candidatePrefs.keys())
        jobCompany = employer[:]
        hired  = {}
        employerPrefs2 = copy.deepcopy(employerPrefs)
        candidatePrefs2 = copy.deepcopy(candidatePrefs)
        while jobCompany:
            emp = jobCompany.pop(0)
            emplist = employerPrefs2[emp]
            candi = emplist.pop(0)
            most_preferred = hired.get(candi)
            if not most_preferred:
                # if candidate is free
                hired[candi] = emp
                # print("  %s prefers %s" % (emp, candi))
            else:
                candilist = candidatePrefs2[candi]
                if candilist.index(most_preferred) > candilist.index(emp):
                    # candidate prefers new emp
                    hired[candi] = emp
                    if employerPrefs2[most_preferred]:
                        # employer has more candidate to try
                        jobCompany.append(most_preferred)
                else:
                    # candidate still wants most_prefered
                    if emplist:
                        # Look again
                        jobCompany.append(emp)
        return hired