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

###########################################
# Generate Verse
###########################################

def generateResponse(speechList, probDict):
    numVerses = pickVerseLength()
    response = ""
    acceptableRhymeList = []
    for x in range(numVerses):
        if x % 2 == 0:
            rhymeWord = getLastWord(speechList, probDict)
            acceptableRhymeList = getAcceptableRhymes(rhymeWord, probDict)
        else:
            if len(acceptableRhymeList) > 0:
                rhymeWord = random.choice(acceptableRhymeList)
            else:
                rhymeWord = getLastWord(speechList, probDict)
        newLine = makeRapVerse(speechList, probDict, rhymeWord)
        response += newLine + " \n"
    return response

def pickVerseLength():
    lowerBound, upperBound = 4,8
    lines = 1
    while lines % 2 != 0:
        lines = random.randint(lowerBound,upperBound)
    return lines
    
def getLastWord(speechList, probDict):
    #first tries to find a word that has rhymes that are also in probDict
    lastWord = -1
    for word in speechList:
        rhymeList = getRhymes(word)
        for count in range(len(rhymeList)):
            wordThatRhymes = random.choice(rhymeList)
            if wordThatRhymes in probDict:
                lastWord = word
                break
    while lastWord == -1: #could not find a word in dictionary that rhymes
        lastWord = random.choice(probDict.keys())
    return lastWord

def makeRapVerse(speechList, probDict, rhymeWord):
    verse = [rhymeWord]
    smallVerseLength, longVerseLength = 6,8
    verseLength = random.randint(smallVerseLength,longVerseLength)
    for index in range(verseLength):
        afterWord = verse[0] #represents word that comes after next word found
        verse.insert(0, prevWord(afterWord, probDict))
    return " ".join(verse)
    
def prevWord(word, probDict):
    #generates a word to go before given word
    if word not in probDict:
        return random.choice(list(probDict.keys()))
    else:
        wordProb = probDict[word]
        randProb = random.random()
        currentProb = 0.0 #initial probability
        for word in wordProb:
            currentProb += wordProb[word]
            if randProb <= currentProb:
                return word
        return random.choice(list(probDict.keys()))
    
def getRhymes(word): #returns list of words that rhyme with given word
    rhymeList = []
    rhymes = []
    if isinstance(word, str):
        #print("word: " + word)
        try:
            rhymes = pronouncing.rhymes(word)
        except:
            print("could not find rhymes")
            #print(word)
    for element in rhymes:
        try: 
            rhymeList += [str(element)]
        except:
            print("could not parse as string")
    return rhymeList

def getAcceptableRhymes(word, probDict): 
    #returns a list of words that rhyme with words and are also in probDict
    acceptableRhymes = []
    rhymeList = getRhymes(word)
    for word in rhymeList:
        if word in rhymeList:
            acceptableRhymes.append(word)
    return acceptableRhymes
    
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
    wordList = wordList[::-1] #backwards
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
#speechList = y.split()
#print("" + getLastWord([], probDict))
print(makeRapVerse(speechList, probDict))
#print(generateResponse(speechList, probDict))
#print(prevWord(word, probDict))
