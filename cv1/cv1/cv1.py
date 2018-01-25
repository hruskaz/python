import re
import operator

authourCounts = {}
centuryCounts = {}

ccount = 0;
#if you find C minro in title use this to skip 'Key:' line search
skip = 0;

file = open("scorelib.txt", "r", encoding="utf-8") 
line = file.readline()
while line: 
    #authors
    match = re.search(r"Composer: (.*)", line)
    if(match):
       authors = match.group(1).strip()
       singleNames = authors.split(";")
       for name in singleNames:
           name = name.strip()
           parMatch = re.search(r"(\(.*\));?", name)
           if parMatch:
               name = name.replace(parMatch.group(1), "")
           name = name.strip()
           if name in authourCounts:
               authourCounts[name] += 1
           else:
               authourCounts[name] = 1    

    #centuries
    match = re.search(r"Composition Year: (.*)", line)
    if(match):
       date = match.group(1).strip()
       yearMatch = re.search(r"([0-9]{3,4})", date)
       if yearMatch:
           century = int(yearMatch.group(1)) // 100
           if century in centuryCounts:
               centuryCounts[century] += 1
           else:
               centuryCounts[century] = 1 
       
    #was C minor alredy found in this title
    if(skip > 0):
        skip -= 1
    else:
        #keys
        match = re.search(r"key:(.*) c mi(.*)", line.lower())
        if(match):
            ccount += 1
        else:
            match = re.search(r"title:(.*) c mi(.*)", line.lower())
            if(match):
                ccount += 1
                #do not check next 5 lines for C minor
                skip = 5

    line = file.readline()

print("Authors:")
sortedAuthorsCounts = sorted(authourCounts.items(), key=operator.itemgetter(1), reverse=True)
for tpl in sortedAuthorsCounts:
    if(tpl[0] != ""):
        print("%s: %d" % (tpl[0], tpl[1]))
print("\n")
print("Centuries:")
sortedCenturiesCounts = sorted(centuryCounts.items(), key=operator.itemgetter(0))
for tpl in sortedCenturiesCounts:
    print("%sth century: %d" % (tpl[0], tpl[1]))
print("\n")
print("C minor was used %d times" % ccount)