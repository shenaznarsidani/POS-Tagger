import json
import collections
import sys

model_file = "hmmmodel.txt"
output_file =  "hmmoutput.txt"
 
# Opening JSON file
with open(model_file) as fp:
    model = json.load(fp)

transitions = model["transitions"]
emissions = model["emissions"]
word_count = model["word_count"]
tag_count = model["tag_count"]
tag_word_unique_count = model["tag_word_unique_count"]

avg_count= sum(tag_word_unique_count.values())/len(tag_word_unique_count)
#print("tag_word_unique_count ",tag_word_unique_count)
#print(avg_count, sum(tag_count.values()))

possible_tags_unique = collections.defaultdict()
    #if(count>=avg_count*1.5):
        #possible_tags_unique[tag]=count

possible_tags_unique = dict(sorted(tag_word_unique_count.items(), key = lambda x: x[1], reverse = True))
possible_tags_unique = {k: possible_tags_unique[k] for k in list(possible_tags_unique)[:4]}

sum_possible_count = sum(possible_tags_unique.values())
for tag in possible_tags_unique:
    count= possible_tags_unique[tag]
    possible_tags_unique[tag]=possible_tags_unique[tag]/sum_possible_count
#print("possible_tags_unique", possible_tags_unique)
num_tags=len(tag_count)
list_tags=list(tag_count.keys())
if("sol" in list_tags):
    list_tags.remove("sol")
if("eol" in list_tags):
    list_tags.remove("eol")
tags_eq_prob ={}
for tag in list_tags:
    tags_eq_prob[tag] = 1/num_tags ## all tags with equal probabilities

all_tags_prob={} 
total_occurrence=0

for tag in tag_count:
    total_occurrence += tag_count[tag]  
for tag in list_tags:
    all_tags_prob[tag]= tag_count[tag]/total_occurrence ## all tags with corresponding probabilities
testing_file = sys.argv[1]
with open(testing_file, encoding='utf-8') as f:
    test_lines = f.readlines()
    
outputLines=[] 
for line in test_lines:
#for l in range(10):
    #line=test_lines[l]
    
    output_prob = {}
    words = line.strip("\n").split()
    sol = words[0]
    #print(sol, sol in emissions.keys())
    output_prob[0]={"tags": collections.defaultdict(), "backpointer": ""}
    if(sol in emissions.keys()):
        possible_tags = emissions[sol]        
    else:
        possible_tags =  possible_tags_unique #all tags with equal probability
    
    for tag in possible_tags.keys():
        if sol in emissions.keys() and tag in emissions[sol].keys():
            emission_prob = emissions[sol][tag]
        else:
            emission_prob = 1 
        #print("emission_prob = ",emission_prob)
        output_prob[0]["tags"][tag] = emission_prob*transitions["sol"][tag]
        output_prob[0]["backpointer"] = "sol" 
    
    for i in range(1, len(words)):
        word=words[i]
        output_prob[i]={"tags": collections.defaultdict(), "backpointer": ""}
        if(word in emissions.keys()):
            possible_tags = emissions[word]
        
        else:
            possible_tags =  possible_tags_unique         #alltags woth equal probability
        for tag in possible_tags.keys():
            if word in emissions.keys():
                emission_prob = emissions[word][tag]
            else:
                emission_prob = 1
            max_prob=0
            previous_tag=""
            for lastwordtag in output_prob[i-1]["tags"]: 
                temp = output_prob[i-1]["tags"][lastwordtag]*emission_prob*transitions[lastwordtag][tag]
                if(temp>max_prob):
                    max_prob = temp
                    previous_tag = lastwordtag
        #output_prob[0]["tags"][tag] = emission_prob*transitions["sol"][tag]
            output_prob[i]["tags"][tag] = max_prob
            output_prob[i]["backpointer"] = previous_tag
    k=len(words)
    output_prob[k]={"tags": collections.defaultdict(), "backpointer": ""}
    #print(output_prob)
    
    max_prob=0
    previous_tag=""
    for lastwordtag in output_prob[k-1]["tags"]:
        #print( "k-1 tags",output_prob[k-1]["tags"], len(words))
        temp = output_prob[k-1]["tags"][lastwordtag]*transitions[lastwordtag]["eol"]
        #print("temp=",temp,lastwordtag )
        if(temp>max_prob):
            max_prob = temp
            previous_tag = lastwordtag
    #print(max_prob)
    output_prob[k]["tags"][tag] = max_prob
    output_prob[k]["backpointer"] = previous_tag
    #print("output_prob =",output_prob)
    output=words[0]+"/"+output_prob[1]["backpointer"]
    for i in range(1,len(words)):
        output = output +" "+ words[i]+"/"+output_prob[i+1]["backpointer"]
    outputLines.append(output)
fwrite = open(output_file, 'w', encoding = 'UTF-8')
for outputLine in outputLines:
    fwrite.write(outputLine + '\n')   