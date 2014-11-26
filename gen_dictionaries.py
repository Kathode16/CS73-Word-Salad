from _collections import defaultdict
import math
import string
import random
import pickle
import sys

def formDictionary(file):
    """For creating a dictionary of word:phonemes from the CMU phoneme dictionary"""
    phoneme_dictionary = defaultdict()

    for line in open(file):
        if line[0].isalpha(): #This is where we start the dictionary, skipping over all punctuation and developer notes in the beginning.
            split = line.split() #Split is a list of the line item separated by whitespace
            for item in split: #item is each individual segment of the line
                if item[len(item)-1] == ")":#If word is duplicate and has a (1) or similar sequence after it, cut it out. There are multiple pronunciations for this word.
                    item = item[0:len(item)-3]
                    split[0] = item #First item in line is now edited word
                    #split[split.index(item)] = item[0:len(item)-3]
                if not item[len(item)-1].isalpha(): #if the item is not entirely letters, cut the last item off.
                    split[split.index(item)] = item[0:len(item)-1] 
 
            if split[0] in phoneme_dictionary.keys(): #if this word is already in dictionary, make a list out of it's existing list
                list = [phoneme_dictionary[split[0]], split[1:] ] #phoneme_dictionary[split[0]] = existing list for duplicate phonemes, next index is current list of phonemes
                phoneme_dictionary[split[0]] = list
            else: 
                phoneme_dictionary[split[0]] = split[1:]#dictionary of {word:[phoneme list]}
            #print split
            
    current_path = open("phoneme_output.txt", "w")
    for entry in phoneme_dictionary:
        current_path.write(entry + str(phoneme_dictionary.get(entry)) + "\n")
    
    current_path = open("phon_pickle.txt", "w")
    pickle.dump(phoneme_dictionary,current_path, pickle.HIGHEST_PROTOCOL)
    current_path.close()
    
    return phoneme_dictionary

def layered_dict(phoneme_dict):
    """for creating a dictionary of phoneme:words starting with that phoneme"""
    
    layered_dict = defaultdict()
    phonemes = ["AA", "AE", "AH", "AO", "AW", "AY","B", "CH", "D", "DH", "EH", "ER","EY", "F", "G", "HH", "IH", "IY", "JH", "K", "L", "M", "N", "NG", "OW", "OY", "P", "R", "S", "SH", "T", "TH", "UH", "V", "W", "Y", "Z", "ZH"]
    for phone in phonemes:
        layered_dict[phone] = []
    for word in iter(phoneme_dict):
        for phone in phonemes:
            if phoneme_dict[word][0] == phone:
                layered_dict[phone].append(word)
                 
    current_path = "layer_pickle.txt"
    current_path = open(current_path, "w")

    pickle.dump(layered_dict,current_path, pickle.HIGHEST_PROTOCOL)
    current_path.close()
    
if __name__=='__main__':
    file = sys.argv[-1] #should be "cmuDict.txt"
    phoneme_dict = formDictionary(file)
    layered_dict(phoneme_dict)

