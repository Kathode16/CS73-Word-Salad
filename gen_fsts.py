"""program to create text files formatted for Carmel to run viterbi on inputed words
in order to output a similar-sounding phrase"""

import string
import sys

def read_dict(file):
    words = {}
    for line in open(file):
        key = line[0:line.index("[")]
        list = line[line.index("["):len(line)-1]
        line = list[list.index("["):list.index("]")+1] #take first list for cases of more than one pronunciation
        line = line.split(",")
        for item in line:
            index = line.index(item)
            item = item.rstrip("]")
            item = item.lstrip("[")
            item = item.lstrip("[")
            item = item.rstrip("'")
            item = item.lstrip(" '")
            
            line[index] = item
        words[key] = line 
        
    return words

def gen_words_phonemes(words):
    num = 0
    
    output = open("words_phonemes.fst", 'w')  
    output.write("0")
    output.write("\n")
    state = 1  
    for word in words:
        for i, phoneme in enumerate(words[word]):
            if i == 0:
                line = "(0 (" + str(state) + " \""+ word+ "\" \"" + phoneme.strip().strip(string.punctuation) + "\"))"
                state +=1
            elif i == len(words[word])-1:
                line = "(" + str(state-1) + " (0 *e* " + "\"" + phoneme.strip().strip(string.punctuation) + "\"))"
                state +=1
            else:
                line = "(" + str(state-1) + " (" + str(state) + " *e* " + "\"" + phoneme.strip().strip(string.punctuation) + "\"))"
                state += 1
            output.write(line)
            output.write("\n") 
            num +=1   
    output.close()
    
    return state

def gen_phonemes_words(words, state):
    output = open("phonemes_words.fst", 'w') 
    output.write("0")
    output.write("\n")
    for word in words:
        for i, phoneme in enumerate(words[word]):
            if len(words[word]) == 1:
                line = "(0 (0 " "\"" + phoneme.strip().strip(string.punctuation) + "\" \"" + word + "\"))"
            elif i == 0:
                line = "(0 (" +str(state) + " \"" + phoneme.strip().strip(string.punctuation) + "\" *e*))"
                
                state += 1
            elif i == len(words[word])-1:
                line = "(" + str(state-1) + " (0 \"" + phoneme.strip().strip(string.punctuation) +"\" \"" + word + "\"))"
                state += 1
            else:
                line = "(" + str(state-1) + " (" + str(state) + " \"" + phoneme.strip().strip(string.punctuation) + "\" *e*))"
                state += 1
    #         print line    
            output.write(line)
            output.write("\n")       
            
    output.close()

def gen_words(words):
    output = open("gen_words.fst", 'w') 
    output.write("0")
    output.write("\n")
    num = 0
    for word in words:
         line = "(0 (0 " + "*e*" + " \"" + word + "\"))"
         output.write(line)
         output.write("\n") 
          
    output.close()

def read_costs():
    costs = {}
    first = []
    file = "phonemes-confusion.txt" 
    for line in open(file):
        row = line.strip().split()
        if first == []:     #if we're on the first row
            first = row     #save its values except the empty space at the beginning
        else:
            i = 1           #keep track of index in letter
            for letter in first:
                costs[letter + " " + row[0]] = float(row[i])
                i += 1
                
    return costs

def gen_phon_phon(words, costs):
    output = open("phonemes_phonemes.fst", 'w')
    output.write("0")
    output.write("\n")
    for pair in costs:
        phonemes = pair.split()
        one = phonemes[0].strip().strip(string.punctuation)
        two = phonemes[1].strip().strip(string.punctuation)
        if one == "eps" and two != "eps":
            line = "(0 (0 *e* " + "\"" + two + "\" " + str(costs[pair]) + "))"
        elif two == "eps" and one != "eps":
            line = "(0 (0 " + "\"" + one + "\" *e* " + str(costs[pair]) + "))"
        elif one == two == "eps":
            line = "(0 (0 *e* *e* " + str(costs[pair]) + "))"
        else:
            line = "(0 (0 " + " \"" + one + "\" " + "\"" + two + "\" " + str(costs[pair]) + "))"
        output.write(line)
        output.write("\n")

    output.close()

if __name__=='__main__':
    file = sys.argv[-1] #"phoneme_output.txt" file created by gen_dictionaries.py
    words = read_dict(file)
    state = gen_words_phonemes(words)          
    gen_phonemes_words(words, state)
    gen_words(words)
    costs = read_costs()
    gen_phon_phon(words, costs)
    
    
