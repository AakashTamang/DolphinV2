# list_of_lists = ["Python Developer",[],["testing","debugging","Python"],"Experience in Python Developer","Koteshwor","Bagmati","Nepal"]

# flattened  = [val for sublist in list_of_lists for val in sublist] 

# print(flattened)

req_technical_skills = ["test", "is", "happening"]
req_soft_skills = []
dad = ['google',"seven"]
sad = ["hat"]
b="wau"
c="range"

# tech_skills = ", ".join( repr(e) for e in req_technical_skills)
# tech_skills = str(req_technical_skills)[1:-1]
# tech_skills = str(req_technical_skills).replace('[','').replace(']','')
mylist = [b,c]
[mylist.append(i) for i in req_technical_skills]
[mylist.append(i) for i in req_soft_skills]
[mylist.append(i) for i in dad]
[mylist.append(i) for i in sad]

print(mylist)