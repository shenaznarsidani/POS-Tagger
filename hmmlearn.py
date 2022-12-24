import sys
import collections
import json


training_file = sys.argv[1]

model_file="hmmmodel.txt"

word_count = {}
tag_count = {}
tag_word_unique = collections.defaultdict()
emissions = collections.defaultdict(collections.Counter)
transitions = collections.defaultdict(collections.Counter)
f=open(training_file, encoding='utf-8')

with open(training_file, encoding='utf-8') as f:
    lines = f.readlines()
#print(len(lines))

# to maintain the count of words
for l in range(len(lines)):
    
    #print("line =>", lines[l])
    words_n_tags = lines[l].strip("\n").split()
    word , tag = words_n_tags[0].rsplit("/",1) 
    tag = tag.upper()
    transitions["sol"][tag] += 1
    emissions[word][tag] += 1
    word_count[word]=word_count.get(word,0)+1
    tag_count[tag]=tag_count.get(tag,0)+1
    tag_count["sol"]=tag_count.get("sol",0)+1
    if (tag in tag_word_unique):
        tag_word_unique[tag].add(word)
    else:
        tag_word_unique[tag]=set()
        tag_word_unique[tag].add(word)
    #print("line = ",l)
    for i in range(1,len(words_n_tags)) :
        
        #print(i)
        next_word , next_tag  = words_n_tags[i].rsplit("/",1) 
        next_tag = next_tag.upper()
        #print(t)
        emissions[next_word][next_tag]+=1
        transitions[tag][next_tag]+=1
        
        #print(words,word,tag)
        word_count[next_word]=word_count.get(next_word,0)+1
        tag_count[next_tag]=tag_count.get(next_tag,0)+1
        #tag_word_unique[next_tag].add(next_word)
        if (next_tag in tag_word_unique):
            tag_word_unique[next_tag].add(next_word)
        else:
            tag_word_unique[next_tag]=set()
            tag_word_unique[next_tag].add(next_word)
        #if(i==len(words_n_tags)-1):
            #transitions[next_tag]['eol']+=1
    
        tag = next_tag
    transitions[next_tag]['eol']+=1
    tag_count["eol"]=tag_count.get("eol",0)+1
        
        
#print(len(word_count))
               
tag_word_unique_count={} 
for tag in tag_word_unique:
    tag_word_unique_count[tag]=len(tag_word_unique[tag]) 
               
#print(tag_word_unique_count)
#print(tag_count)
#print("transitions = ",transitions)
#print("\nemissions = ", emissions)
#print("emissions[regionale][A] = ", emissions['regionale']['A'])
#print("transitions[BN][VM] = ", transitions["BN"]["VM"])
#print("transitions")    

for word in transitions:
    #print("==============================")
    #print("transitions of",word, " = ", transitions[word])
    cummulative= sum((transitions[word]).values()) 
    #print("cummulative = ",cummulative)
    transitions[word] = collections.Counter({key: value / cummulative for key, value in transitions[word].items()})
    #print("probabailities = ",transitions[word])
#print("emissions")
for word in emissions:
    #print("==============================")
    #print("emissions of",word, " = ", emissions[word])
    cummulative= sum((emissions[word]).values())
    #print(cummulative)
    emissions[word] = collections.Counter({key: value / cummulative for key, value in emissions[word].items()})
    #print("probabailities = ",emissions[word])
    
#print("\ntransitions = ",transitions)
#print("\nemissions = ", emissions)  
for prev_tag in transitions.keys():
    #print("\n previously ",transitions[prev_tag])
    if prev_tag=="eol":
        continue
    for next_tag in tag_count.keys():
        if next_tag=="sol":
            continue
        #print(prev_tag,"-", next_tag)
        if next_tag not in transitions[prev_tag]:
            #transitions[prev_tag][next_tag] = tag_count[prev_tag]*(1)/(tag_count[prev_tag]+(5*len(tag_count)-1))
            transitions[prev_tag][next_tag] = (1)/((len(tag_count)))
        else:
            #transitions[prev_tag][next_tag] = (transitions[prev_tag][next_tag]+1)*tag_count[prev_tag]/(tag_count[prev_tag]+(5*len(tag_count)-1))
            transitions[prev_tag][next_tag] = (transitions[prev_tag][next_tag]+1)/((len(tag_count)))
    #print("\n after smoothening ",transitions[prev_tag], len(transitions[prev_tag]) ) 
#print("transitions = \n",transitions, len(transitions))
model={"transitions":transitions,"word_count":word_count, "emissions":emissions, "tag_count":tag_count, "tag_word_unique_count": tag_word_unique_count} 
#for tag in transitions:
    #print(len(tag))
    
with open(model_file, 'w') as fp:
    json.dump(model, fp)
#print(len(emissions))