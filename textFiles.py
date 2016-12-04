###########################################
# Text Files
#
# NAME: Shanel Huang
# ANDREW ID: shanelh
# SECTION: F
# DATE: November 2016
#
# Description: searches directory for .txt files and process them
#
###########################################

import os
from os import path
import string
import random
import pronouncing

###########################################
# Generate Verse
###########################################

def makeRapVerse(speechList, probDict):
    firstWord = -1
    for index in range(len(speechList)):
        word = speechList[random.randint(0, len(speechList)-1)]
        if word in probDict:
            firstWord = word
            break
    if firstWord == -1:
        firstWord = random.choice(list(probDict.keys()))
    verse = [firstWord]
    verseLength = 10
    for index in range(verseLength):
        if verse == []:
            verse.append(nextWord(firstWord, probDict))
        else:
            verse.append(nextWord(verse[-1], probDict))
    return " ".join(verse)
    
def nextWord(word, probDict):
    if word not in probDict:
        return random.choice(list(probDict.keys()))
    else:
        wordProb = probDict[word]
        randProb = random.random()
        currentProb = 0.0
        for word in wordProb:
            currentProb += wordProb[word]
            if randProb <= currentProb:
                return word
        return random.choice(list(probDict.keys()))

def pickRandomWord(speechList):
    index = random.randint(0, len(speechList) - 1)
    return speechList[index]
    
###########################################
# Process Text
###########################################

def processAllTexts():
    #adds all text to database of occurences and probaility
    path = "lyrics" #folder of all lyrics in txt files
    fileList = findFiles(path)
    txtFileList = isolateTextFiles(fileList)
    freqDict = dict()
    for file in txtFileList:
        text = str(readFile(file))
        text = formatText(text)
        freqDict = updateNumOccurences(text, freqDict)
    probDict = getProbabilities(freqDict)
    return probDict
    
def formatText(text):
    newText = text.lower()
    newText = removePunctuation(newText)
    newText = newText.replace("\n", " ")
    newText = newText.replace("\xe2\x80\xa8", " ") #unicode line separator
    return newText
    
def updateNumOccurences(text, frequencyDict):
    #returns in form of a dictionary of dictionaries
    #level 1: maps first word to second word
    #level 2: maps first-second word combo to number of occurences
    freqDict = frequencyDict
    wordList = text.split(" ")
    for word in wordList:
        if word == '' or word == ' ' or word == None:
            wordList.remove(word) 
    for i in range(len(wordList) - 1):
        firstWord = wordList[i]
        secondWord = wordList[i+1]
        if firstWord in freqDict: #first word already in dictionary
            if secondWord in freqDict[firstWord]: #first-second combo exists
                freqDict[firstWord][secondWord] = freqDict[firstWord].get(secondWord) + 1
            else: 
                freqDict[firstWord][secondWord] = 1
        else: #found new first word
            freqDict[firstWord] = {secondWord : 1}
    return freqDict

def getProbabilities(freqDict):
    # returns in form of a dictionary of dictionaries 
    # level 1: maps first word to second word
    # level 2: maps first-second word combo to probability of combo
    digitsRounded = 5
    probabilityDict = dict()
    for firstWord in freqDict:
        probs = dict()
        count = 0   #count of how many times first word occurred
        secondWordOccurrences = freqDict[firstWord]
        for word in secondWordOccurrences:
            count += secondWordOccurrences[word]
        for secondWord in secondWordOccurrences:
            prob = secondWordOccurrences[secondWord]/float(count)
            roundedProb = round(prob,digitsRounded)
            probs[secondWord] = roundedProb
        probabilityDict[firstWord] = probs
    return probabilityDict
    
def removePunctuation(text): 
    #returns the same text without any punctuation
    newString = ""
    punct = string.punctuation
    for char in text:
        if char in punct:
            pass
        else:
            newString += char
    return newString

def findFiles(path): 
    #returns list of all files
    if (os.path.isdir(path) == False):
        return [path]
    else:
        filesList = []
        for file in os.listdir(path):
            filesList += findFiles(path + "/" + file)
        return filesList
    
def isolateTextFiles(filesList): 
    #returns list of all text files
    for element in filesList:
        if element.endswith(".txt") == False:
            filesList.remove(element)
    return filesList
    
def readFile(filename, mode="rt"): # taken from 15-112 course notes
    # rt = "read text"
    with open(filename, mode) as fin:
        return fin.read()
        
probDict = processAllTexts()
speechList = ["cars", "this", "work", "monkey", "drink", "girl", "money"]
print(makeRapVerse(speechList, probDict))