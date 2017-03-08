dict2 = {}




conflictList = []

listing = ["one", "two", "noConflict", "three", "four", "five", "noConflict_2"]

"""
for i in range(len(listing)):
        for j in range(i + 1, len(listing)):
        	print(listing[i], " : ", listing[j])
        	# want to put one and two into C1 in dict and 3,4 & 5 into C2 in dict. The others.. in the other parts of dict?
        	if listing[i]=="one" or listing[i] == "two"  or listing[i]=="three" or listing[i] == "four" or listing[i] == "five":
        		if listing[i] not in conflictList:
        			conflictList.append(listing[i])
        			if 'C1' not in dict2:
        				dict2['C1'] = [listing[i]]
        			else:
        				dict2['C1'].append(listing[i])
        	if listing[i] == "noConflict" or listing[i] == "noConflict_2":
        		if 'noCons' not in dict2:
        			dict2['noCons'] = [listing[i]]
        		else:
        			dict2['noCons'].append(listing[i])



for k, v in dict2.items():
	    print(k,v)
"""

d = {}


for i in range(len(listing)):
	d[i] = [listing[i]]

for k, v in d.items():
	    print(k,v)