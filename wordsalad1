#!/usr/bin/env python

import subprocess
import math
import commands
from _collections import defaultdict
import cgi
import os
import re
import random
import string
import pickle
import cgitb; cgitb.enable()

def build_costs_matrix(file):
    """reads in costs file and return a dictionary associating phoneme pairs with
    their respective cost"""
    costs = {}
    first = []
    for line in open(file):
        row = line.strip(string.punctuation).split()
        if first == []:     #if we're on the first row
            first = row     #save its values except the empty space at the beginning
        else:
            i = 1           #keep track of index in letter
            for letter in first:
                if letter in costs:
                    costs[letter][row[0]] = float(row[i])
                else:
                    costs[letter] = {row[0]: float(row[i])}
                i += 1
    return costs

def calc_dist(w, c):
    """finds edit_distance between observed phoneme sequence w and potential 
    "hidden" sequence c"""
    
    #build edit_dist matrix
    matrix = [0] * (len(c)+1)
    for i in range(len(matrix)):
        matrix[i] = [0]*(len(w)+1)

    #fill in values left to right across columns
    for i in range(len(c)+1):
        for j in range(len(w)+1):
            #fill in deletion/insertion costs in the first row/column
            if i == 0 and j != 0:
                matrix[i][j] = matrix[0][j-1] + -math.log(costs["eps"][c[i]])
            elif i != 0 and j == 0:
                matrix[i][j] = matrix[i-1][0] + -math.log(costs[w[j]]["eps"])   
                
            # for cells outside the first row/column
            if i !=0 and j!=0:
                #calculate the different costs for each cell
                del_cost = matrix[i][j-1] + -math.log(costs["eps"][c[i-1]])
                ins_cost = matrix[i-1][j] + -math.log(costs[w[j-1]]["eps"])
                ms_cost = matrix[i-1][j-1] + -math.log(costs[w[j-1]][c[i-1]])
                 
                #take the minimum cost for the current cell
                minimum = min(del_cost, ins_cost, ms_cost)
                matrix[i][j] = minimum

    #return edit distance
    return matrix[-1][-1]

def gen_seq_pairs(layered_dict, phoneme_dictionary, phonemes_list, banned, units, costs):  
    """finds best sequence of words that matches the observed sequence via edit_distance, 
    discluding banned words (words longer than one phoneme that occur in that sequence) looking
    back up to units phonemes"""
    
    #the dist calcs at given pt in phonemes list
    distances = [0]*(len(phonemes_list)) 
    # the "best fit" word at a given pt
    words = []
    #how many phonemes back a given "best fit" word in the sequence accounts for
    indices = [] 
    seq_words = []  #words included the final output
    
    #for every phoneme p in the input, find the best possible 
    #match of the word looking back unit phonemes
    for p in range(len(phonemes_list)): 
        
        possibilities = {}  # store "units back/word": edit_dist pairs
        
        # for i phonemes back in units of phonemes, find the minimum 
        # distance from all words in phoneme_dictionary
        for i in range(units):
            if p-i<0:   #if we've reached the  first phoneme in the sequence, exit the loop
                continue
            w = phonemes_list[p-i:p+1] #range of phonemes we're looking at in a given pass
            for sound in layered_dict:
                #to optimize only look at words starting with phonemes similar to the first phoneme
                if costs[w[0]][sound] >= .05:   
                    for word in layered_dict[sound]:
                        if word not in banned and word in phoneme_dictionary: #ignore near-identical words
                            c = phoneme_dictionary[word]
                            #only look at words shorter than 5 phonemes long
                            if len(c) < 5:
                                #only allow for one insertion/deletion
                                if abs(len(w)-len(c)) < 1:
                                    if p == 0: 
                                        dist = (calc_dist(w, c)/(i+1))
                                    else:
                                        dist = distances[i] + (calc_dist(w, c)/(i+1))
                                    possibilities[str(i+1) + " " + word] = dist
  
        first = True
        best_fit = ""
        
        # finds the possibility with the shortest distance
        for pair in possibilities:

            if first:
                first = False
                best_fit = pair
            else:
                if possibilities[pair]<possibilities[best_fit]:
                    best_fit = pair

        #extract the index/word
        if best_fit != "":
            info = best_fit.split()
            i = int(info[0])
            indices.append(i)
            words.append(info[1])
            distances.append(possibilities[best_fit])
#         print best_fit
    
    
    # starting with the last stored word, trace the indices backwards through "words"
    #to find the best sequence
    q = len(indices)-1
    while q >= 0:
        n = indices[q]
        seq_words.insert(0,words[q].lower())
        q = q-n
          
    # convert from list to string
    output = ""
    for word in seq_words:
        output += word + " "
        
    return output

def gen_phonemes(input_string, phoneme_dictionary, filename):
    """translate input into phonemes list, checking for errors/banned words"""
    banned = []
    
    if len(input_string) > 50:
        input_string = raw_input("Phrase length exceeds 50 characters. Please re-enter: ") 
        input_items = phonemes_list , banned, ans
        open(filename, "w").close()
    else:
        ans = input_string.upper() #convert input string into all caps  
        input_string = ans.split()
        
        errors = ""
        phonemes_list = [] #create list of phonemes that correspond to the English phrase
        for word in input_string:
            if word in phoneme_dictionary:
                phonemes = phoneme_dictionary[word] 
                banned = check_banned(word, phonemes, phoneme_dictionary, banned)
                for phoneme in phonemes: 
                    phonemes_list.append(phoneme)
            else:
                errors += word + " "

        if errors != "":
            print '<br>'
            print '<br>'
            print '<br>'
            print '<br>'
            print '<br>'
            print "The following words are not in the dictionary: " + errors + ". Please re-enter: "      
            input_items = phonemes_list , banned, ans  
            open(filename, "w").close()
        else:
            ans = ans.strip()
            input_items = phonemes_list, banned, ans
        
    return input_items
def check_banned(word, phonemes,phoneme_dictionary, banned):
    """returns list of banned words containing complete words at beginning and 
    end of inputed words"""
    
    test = ""
    chars = list(word)
    
    #if beginning of word contains a complete word > three chars, add it to banned
    for char in chars:
        test += char
        if len(list(test))>3 and test in phoneme_dictionary:
            banned.append(test) 
    test = ""
    
    #ban if end of word is complete word > three chars
    for i, char in enumerate(chars):
        test += chars[len(chars)-i-1]
        if len(list(test))>3 and test[::-1] in phoneme_dictionary:
            banned.append(test[::-1]) 
   
    #ban full words longer than a single phoneme
    if len(phonemes) > 1:
        banned.append(word)
    
    #return list of words to exclude from edit dist search
    return banned 

def clearfile(filename):
    open(filename, "w").close()
    return None   

print "Content-type: text/html"
print 
print "<html><head>"
print "<title>Word Salad"
print "</title>"
print "<link rel=\"stylesheet\" type=\"text/css\" href=\"http://www.cs.dartmouth.edu/~angelagu01/style2.css\">"
print "<style>"
print ".ttlarge{font-family: Courier; font-size: 12pt;}"
print ".box{height: 550px; float: left; border: 1px solid #cdcdcd; padding: 10px;}"
print "</style>"
print "</head><body style=\"padding: 20px;\">"

print "<h1>Word Salad</h1>"
print "- Where it's not what you say, it's what you hear! Personalize a goofy game with your friends and let the words do the rest. Your team must come up with a list of phrases that t
he other team will play with. You get to watch as they race the clock and try to sound out each puzzle and come up with the original phrases. Enter your phrases and team name, and hand
 it off with the next team so they can come up with an interesting game for you. We'll be keeping score, listen carefully! Still not sure how to play? <a href=\"http://www.freemadgabon
line.com/\">Go here</a><p>"

form = cgi.FieldStorage()

phrase1 = form.getvalue("phrase1", "")
phrase2 = form.getvalue("phrase2", "")
nums = form.getvalue("nums")
numr = form.getvalue("numr")
tocheck = form.getvalue("tocheck")
totrans = form.getvalue("totrans")
func = form.getvalue("func")

print "<div class=\"box\" style=\"width:30%;\"><h3>Team 1 Enter your phrases</h3><p>"
print "<form action=\"wordsalad1.cgi\" method=\"post\">"
print "<textarea rows=\"25\" cols=\"25\" class=\"ttlarge\" name=\"phrase1\">"
print cgi.escape(phrase1)+"</textarea><p>"
print "<form action=\"wordsalad1.cgi\" method=\"post\">"
print "<input type=\"submit\" value=\"Submit\"></form><p>"
print "</div>"
print "<div class=\"box\" style=\"width:30%;\"><h3>Team 2 Enter your phrases</h3><p>"
print "<form action=\"wordsalad1.cgi\" method=\"post\">"
print "<textarea rows=\"25\" cols=\"25\" class=\"ttlarge\" name=\"phrase2\">"
print cgi.escape(phrase2)+"</textarea><p>"
print "<form action=\"wordsalad1.cgi\" method=\"post\">"
print "<input type=\"submit\" value=\"Submit\"></form><p>"
print "</div>"

o = open("Phrase1.txt", 'a')
o.write(cgi.escape(phrase1))
o.close()

o = open("Phrase2.txt", 'a')
o.write(cgi.escape(phrase2))
o.close()

#read in probability matrix

'''Forming Game Here'''

file = "phonemes-confusion.txt"
costs = build_costs_matrix(file)

units = 5
dict_file = "phon_pickle.txt"
layered_file = "layer_pickle.txt"
phoneme_dict = pickle.load(open(dict_file, "rb"))
layered_dict = pickle.load(open(layered_file, "rb"))

phrase1file = open("Phrase1.txt", "r")
phrase2file = open("Phrase2.txt", "r")

#history = open("history.txt", "a")
results1 = False
results2 = False

one = open("results1.txt", "w+")
two  = open("results2.txt", "w+")

if one.readline() == "":

    for line in phrase1file: #open file and read line, each line is a separate entry

        if line[0].isalpha(): #Check if inputs are in dicionary, same length, correct characters

            input_items =  gen_phonemes(line, phoneme_dict, "Phrase1.txt")
            phonemes_list = input_items[0]
            banned_words = input_items[1]
            answer = input_items[2]
    
            #find best similar-sounding sequence
            output = gen_seq_pairs(layered_dict, phoneme_dict, phonemes_list, banned_words, units, costs)
            answer1= open("results1.txt", 'a+')
            answer1.write(output)
            answer1.write("\n")
            answer1.close()
    
            results1 = True    
    phrase1file.close()
if results1 == True and len(phonemes_list)>0:
    print '<br>'
    print '<br>'
    print '<br>'
    print '<br>'
    print '<br>'

    print "Team 1 you are all set! Make sure you clear your entries so the other team doesn't see them."

if two.readline() == "":
    print two.readline()
    for line in phrase2file: #open file and read line, each line is a separate entry                                                          
        #print line, "is line"
        if line[0].isalpha():#Check if inputs are in dicionary, same length, correct characters                        
            
            input_items =  gen_phonemes(line, phoneme_dict, "Phrase2.txt")
            phonemes_list = input_items[0]
            banned_words = input_items[1]
            answer = input_items[2]
            
            #find best similar-sounding sequence                                                            
            output = gen_seq_pairs(layered_dict, phoneme_dict, phonemes_list, banned_words, units, costs)
            answer2 = open("results2.txt", "a+")
            answer2.write(output)
            answer2.write("\n")
            answer2.close()

            results2 = True 
    phrase2file.close()

if results2 == True and len(phonemes_list)>0:
    print '<br>'
    print '<br>'
    print '<br>'
    print '<br>'
    print '<br>'
    print "Team 2 you are all set! Make sure your clear your entries so the other team doesn't see them."

print "</div>"
print "<div style=\"clear: both;\"></div>"
print "</body><p>"
print "<center><form action=\"http://www.cs.dartmouth.edu/cgi-bin/cgiwrap/katysprout/wordsalad2.cgi\"</center><p>>"
print "<input type=\"submit\" value=\"Play!\"></form><p>"
print "<form action=\"wordsalad1.cgi\" method=\"post\">"
print "<input type=\"submit\"name=\"reset\" value=\"Reset\"><p>"
print "</div>" #create box to reset everything                                  

if "reset" in form:
    print "reset"
    open('results1.txt', 'w').close()
    open('results2.txt', 'w').close()
    open('Phrase1.txt', 'w').close()
    open('Phrase2.txt', 'w').close()

print "</form><p>"
print "</html>"
