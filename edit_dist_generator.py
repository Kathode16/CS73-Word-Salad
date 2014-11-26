!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division #integer division
import math
import string
from _collections import defaultdict
from __builtin__ import True
import random
import pickle
import sys

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

def gen_seq_pairs(phoneme_dictionary, phonemes_list, banned, units):  
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
                                        dist = (calc_dist(w, c)/(i+1)) #take the average distance per phoneme
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

def readin_pho_dict(file):
    """for reading in phoneme dictionary from text file (generated from CMU dict)"""
    
    phoneme_dictionary = {} # store "word: phoneme_list" pairs
    
    for line in open(file):
        key = line[0:line.index("[")]
        list = line[line.index("["):len(line)-1]
        #take first list for cases of more than one pronunciation
        line = list[list.index("["):list.index("]")+1] 
        line = line.split(",")
        for item in line:
            index = line.index(item)
            item = item.rstrip("]")
            item = item.lstrip("[")
            item = item.lstrip("[")
            item = item.rstrip("'")
            item = item.lstrip(" '")
            
            line[index] = item
        
        phoneme_dictionary[key] = line  
     
    return phoneme_dictionary
    
def readin_layered_dict(file):
    """for reading in layered dictionary"""
    layered_dict = {}
    for line in open(file):
        key = line[0:line.index("[")]
        list = line[line.index("["):len(line)-1]
        #take first list for cases of more than one pronunciation
        line = list[list.index("["):list.index("]")+1] 
        line = line.split(",")
        for item in line:
            index = line.index(item)
            item = item.rstrip("]")
            item = item.lstrip("[")
            item = item.lstrip("[")
            item = item.rstrip("'")
            item = item.lstrip(" '")
            
            line[index] = item
        layered_dict[key] = line
    
    return layered_dict

def check_banned(word, phonemes, banned):
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
            
def gen_phonemes(input_string):
    """translate input into phonemes list, checking for errors/banned words"""
    
    banned = []
    
    print "You entered: ", input_string 

    if len(input_string) > 50:
        input_string = raw_input("Phrase length exceeds 50 characters. Please re-enter: ") 
        input_items = gen_phonemes(input_string)
    else:
        ans = input_string.upper() #convert input string into all caps  
        input_string = ans.split()
        
        errors = ""
        phonemes_list = [] #create list of phonemes that correspond to the English phrase
        for word in input_string:
            if word in phoneme_dictionary:
                phonemes = phoneme_dictionary[word] 
                banned = check_banned(word, phonemes, banned)
                for phoneme in phonemes: 
                    phonemes_list.append(phoneme)
            else:
                errors += word + " "

        if errors != "":
            orig_phrase = raw_input("The following words are not in the dictionary: " + errors + ". Please re-enter: ")        
            input_items = gen_phonemes(orig_phrase)  
        else:
            ans = ans.strip()
            input_items = phonemes_list, banned, ans
        
    return input_items

def take_team_input(phoneme_dictionary, units, Qs, team):
    """stores a set of questions/answers for each team of players"""
    answers = []
    questions = []
    
    print ""
    print "WELCOME TEAM " + str(team)
    while len(questions)<Qs:
        orig_phrase = raw_input("Enter an English phrase (no more than 50 characters): ") #request user to input English phrase
        
        input_items = gen_phonemes(orig_phrase)
        phonemes_list = input_items[0]
        banned = input_items[1]
        answer = input_items[2]

        #find best similar-sounding sequence
        output = gen_seq_pairs(phoneme_dictionary, phonemes_list, banned, units)
    
        output = output.upper()
        
        answers.append(answer)
        questions.append(output)
    
    qa = []
    qa.append(questions)
    qa.append(answers)
    print "THANK YOU TEAM " + str(team)
    return qa

def score_game(scores):
    """prints scores and calculates the winner/ties"""
    
    max = 0
    ties = []
    winner = ""
    
    #find the maximum scorer. If there is a tie, record the tied teams
    for team in scores:
        print "TEAM " + str(team) + " score: " + str(scores[team])
        if max < scores[team]:
            max = scores[team]
            winner = team
            tie = False
            ties = []
        elif max == scores[team]:
            ties.append(team)
            if winner != "":
                ties.append(winner)
                winner = ""
            tie = True
    
    #print out winners/ties
    print ""
    if tie:
        winners = ""
        for team in ties:
            winners += str(team)
        won = ""
        for win in winners:
            if won != "":
                won += " and "
            won += win
            
        print "TEAMS " + won + " TIED!"
        
    else:
        print "TEAM " + str(winner) + " IS THE WINNER!"
        
def play_game(question_set):
    """presents questions to next team and keeps track of correct answers"""

    num_teams = len(question_set)
    scores = {} #dictionary of team number:number of correct answers
    for t in range(num_teams):
        scores[t+1] = 0
    for q in range(len(question_set[0][0])): #for each question
        for t in range(num_teams):
            print ""
            print "TEAM " + str(t+1) + "'S TURN:"
            p = (t+1) % num_teams   #give each team the questions of the preceding team
            print question_set[p][0][q]
            given_ans = raw_input("answer: ")
            given_ans = given_ans.upper().strip()
            answer = question_set[p][1][q]

            if given_ans == answer:
                print "CORRECT!"
                scores[t+1] = scores[t+1] + 1
            else:
                print "That is incorrect. The answer was: "
                print answer

    score_game(scores)
    
if __name__=='__main__':
    
    cost_file = sys.argv[1] #first arg must be "phonemes_confusion.txt"
    phon_file = sys.argv[2]  #second argument must be "phon_pickle.txt"
    layer_file = sys.argv[-1]  #last argument must be "layer_pickle.txt"
    
    #define constants
    NUM_TEAMS = int(raw_input("ENTER THE NUMBER OF TEAMS: "))
    Qs = int(raw_input("ENTER THE NUMBER OF QUESTIONS: "))
    UNITS = 5
    
    #read in phoneme dictionary
#     file = "phoneme_output.txt"
#     phoneme_dictionary = readin_pho_dict(file)
    phon_file = open(phon_file, 'r') 
    
    phoneme_dictionary = pickle.load(phon_file)

    #read in layered dictionary
#     file = "layered_output.txt"
#     layered_dict = readin_layered_dict(file)   
    layer_file = open(layer_file, 'r') 
    layered_dict = pickle.load(layer_file) 

    #read in probability matrix
    costs = build_costs_matrix(cost_file) 

    question_set = []
    
    for i in range(NUM_TEAMS):
        QA_set = take_team_input(phoneme_dictionary, UNITS, Qs, i+1)
        question_set.append(QA_set)
    
    play_game(question_set)
    
