#!/usr/bin/env python

import subprocess
import commands
import cgi
import os
import re
import random
import string
import cgitb; cgitb.enable()


def checkanswer(submission, answers_file):
    score = 0
    sub_list = submission
    ans_list = []

    #read answers file and create list of answers
    answers = open(answers_file, 'r') 
    answercount = 0
    for line in answers:
        ans_list.append(line)
        answercount += 1
    answers.close()

    #increase score by 1 if the submission matches the answer
    if sub_list != None: 
        for i in range(len(sub_list)):
            if str(cgi.escape(sub_list[i])).lower().strip() == str(ans_list[i]).lower().strip():
                score += 1
    return score, answercount


print "Content-type: text/html"
print 
print "<html><head>"
print "<title>Word Salad"
print "</title>"
print "<link rel=\"stylesheet\" type=\"text/css\" href=\"http://www.cs.dartmouth.edu/~angelagu01/style.css\">"
print "<style>"
print ".ttlarge{font-family: Courier; font-size: 12pt;}"
print ".box{height: 425px; float: left; border: 1px solid #070B19; padding: 10px;}"
print "</style>"
print "</head><body style=\"padding: 20px;\">"

print "<center><h1>Word Salad: Game Time!</h1></center>"

# Create instance of FieldStorage 
form = cgi.FieldStorage() 
team1_ans = form.getlist("team1_ans")
team2_ans = form.getlist("team2_ans")

print "<div class=\"box\" style=\"width: 35%; margin-left: 160px;\">"
print "<form action=\"wordsalad2.cgi\" method=\"post\">"
print "<center><h2>Team 1</h2></center><p>"
print "<h4>Can you decode the following?</h4><p>"

questions1 = open('results1.txt', 'r') #text file containing the gibberish 

#print out questions and an submssion text box for each question
for line in questions1:
    print line, '<br>'
    print "<input type=\"text\" name=\"team1_ans\" required><p>"
questions1.close()

if "submit" in form:
    print "<h4>Results</h4>"
    result = 0
    result, answercount = checkanswer(team1_ans, 'Phrase1.txt')
    print "You got " 
    print result 
    print " out of ", answercount, " correct!<p>"

    answers1 = open('Phrase1.txt', 'r') #read text file containing the answer string
    for line in answers1:
        print line, '<br>' #print answers
    answers1.close()

print "</div>"
print "<div class=\"box\" style=\"width: 35%; margin-left: 25px;\">"
print "<center><h2>Team 2</h2></center><p>"
print "<h4>Can you decode the following?</h4></center><p>"

questions2 = open('results2.txt', 'r') #read text file containing the gibberish 
for line in questions2:
    print line, '<br>'
    print "<input type=\"text\" name=\"team2_ans\"required><p>"
questions2.close()

if "submit" in form:

    print "<h4>Results</h4>"
    result = 0
    result, answercount = checkanswer(team2_ans, 'Phrase2.txt')
    print "You got "
    print result 
    print " out of ", answercount, "  correct!<p>"

    answers2 = open('Phrase2.txt', 'r') #text file containing the answer string
    for line in answers2:
        print line, '<br>'
    answers2.close()
    
    open('results1.txt', 'w').close()
    open('results2.txt', 'w').close()
    open('Phrase1.txt', 'w').close()
    open('Phrase2.txt', 'w').close()


print "</div>"
print "<div style=\"clear: both;\"></div>"
print "</body><p>"
print "<center><input type=\"submit\" name=\"submit\" value=\"Check answers\"></center><p>" #create submit box for all answers
print "</form><p>"
print "</html>"
