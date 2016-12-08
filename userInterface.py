###########################################
# Rap Battle Bot
#
# NAME: Shanel Huang
# ANDREW ID: shanelh
# SECTION: F
# DATE: Fall 2016
#
###########################################

#for user interface
from Tkinter import * 

#for random and string operations
import random
import string

#for reading files
import os
from os import path

#for processing audio 
import pyaudio
import wave
from struct import pack

#for speech to text
import speech_recognition as sr

#for rhyme dictionary
import pronouncing 

###########################################
    
def init(data):
    data.currentScreen = "home" #keeps track of current mode
    data.prevScreen = "home"
    data.backgroundColor = "black"
    data.mouseX, data.mouseY = 0, 0
    data.beginButtonPressed = False
    data.recordButtonPressed = False
    data.responseButtonPressed = False
    data.responseGenerated = False
    data.responseSpoken = False
    data.responseScreenDrawn = False
    data.resetButtonPressed = False
    data.infoButtonPressed = False
    data.backButtonPressed = False
    data.skipButtonPressed = False
    data.rapOffButtonPressed = False
    data.stopButtonPressed = False
    data.rapOffScreenDrawn = False
    data.verseCount = 0
    data.recordTime = 5 #default record time, used if none selected
    data.speech = ""
    data.response = ""
    data.speechList = []
    data.probDict = processAllTexts() #processes text once for each generation
    data.bot1, data.bot2 = "", ""
    
def mousePressed(event, data):
    if data.currentScreen == "home": 
        homeScreenMousePressed(event, data)
    elif data.currentScreen == "audio": 
        audioScreenMousePressed(event, data)
    elif data.currentScreen == "processing": 
        processingScreenMousePressed(event, data)
    elif data.currentScreen == "response": 
        responseScreenMousePressed(event, data)
    elif data.currentScreen == "rapOff":
        rapOffScreenMousePressed(event, data)
    else:  #default goes to info screen
        infoScreenMousePressed(event, data)
    
def keyPressed(event, data):
    if data.currentScreen == "home": 
        homeScreenKeyPressed(event, data)
    elif data.currentScreen == "audio": 
        audioScreenKeyPressed(event, data)
    elif data.currentScreen == "processing":
        processingScreenKeyPressed(event, data)
    elif data.currentScreen == "response":
        responseScreenKeyPressed(event, data)
    elif data.currentScreen == "rapOff":
        rapOffScreenKeyPressed(event, data)
    else:  #default goes to info screen
        infoScreenKeyPressed(event, data)
    
def timerFired(data):
    if data.currentScreen == "home": 
        homeScreenTimerFired(data)
    elif data.currentScreen == "audio": 
        audioScreenTimerFired(data)
    elif data.currentScreen == "processing":
        processingScreenTimerFired(data)
    elif data.currentScreen == "response":
        responseScreenTimerFired(data)
    elif data.currentScreen == "rapOff":
        rapOffScreenTimerFired(data)
    else: #default goes to info screen
        infoScreenTimerFired(data)
    
def redrawAll(canvas, data):
    if data.currentScreen == "home": 
        homeScreenRedrawAll(canvas, data)
    elif data.currentScreen == "audio":
        audioScreenRedrawAll(canvas, data)
    elif data.currentScreen == "processing":
        processingScreenRedrawAll(canvas, data)
    elif data.currentScreen == "response":
        responseScreenRedrawAll(canvas, data)
    elif data.currentScreen == "rapOff":
        rapOffScreenRedrawAll(canvas, data)
    else: #default goes to info screen
        infoScreenRedrawAll(canvas, data)

###########################################
# Home Screen Mode
###########################################

def homeScreenMousePressed(event, data):
    data.mouseX = event.x
    data.mouseY = event.y

def beginButtonPressed(data):
    #returns true if user clicks on begin button
    beginMargin, beginHeight = 70, 40
    xbound1, xbound2 = data.width/2-beginMargin, data.width/2+beginMargin
    ybound1, ybound2 = data.height/2, data.height/2+beginHeight
    if (data.mouseX >= xbound1 and data.mouseX <= xbound2):
        if data.mouseY >= ybound1 and data.mouseY <= ybound2:
            data.beginButtonPressed = True

def homeScreenKeyPressed(event, data):
    pass

def homeScreenTimerFired(data):
    #checks for flow from home to other screens
    beginButtonPressed(data)
    infoButtonPressed(data)
    rapOffButtonPressed(data)
    #when begin button is pressed, app moves on to audio screen
    if data.beginButtonPressed == True:
        #reset mouse to prevent double clicking on next screen
        data.mouseX = 0 
        data.mouseY = 0
        data.currentScreen = "audio"
        data.beginButtonPressed = False
    
def rapOffButtonPressed(data):
    #checks if option to start computer rap off is selected
    rapOffMargin, rapOffHeight = 70, 40
    offset = 75
    xbound1, xbound2 = data.width/2-rapOffMargin, data.width/2+rapOffMargin
    ybound1, ybound2 = data.height/2+offset, data.height/2+rapOffHeight+offset
    if (data.mouseX >= xbound1 and data.mouseX <= xbound2):
        if data.mouseY >= ybound1 and data.mouseY <= ybound2:
            data.rapOffButtonPressed = True
    if data.rapOffButtonPressed == True:
        data.mouseX = 0 
        data.mouseY = 0
        data.currentScreen = "rapOff"
    
def homeScreenRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, 
                                                fill = data.backgroundColor)
    drawInfoButton(canvas, data)
    drawRapOffButton(canvas, data)
    title, titleMargin = "RAP BATTLE BOT!", 150
    canvas.create_text(data.width/2, data.height/2-titleMargin, text = title, 
                                    fill = "white", font = "Helvetica 50 bold")
    directions, directionsMargin = "click to start", 25
    canvas.create_text(data.width/2, data.height/2-directionsMargin, 
            text = directions, fill = "white", font = "Helvetica 20 bold")
    drawBeginButton(canvas, data)

def drawRapOffButton(canvas, data):
    #draws one button on home screen "computer rap off"
    rapOffMargin, rapOffHeight = 70, 40
    offset = 75
    canvas.create_rectangle(data.width/2-rapOffMargin, data.height/2+offset, 
        data.width/2+rapOffMargin, data.height/2+rapOffHeight+offset,
                                                    fill = "gray")
    x = getMiddle(data.width/2-rapOffMargin, data.width/2+rapOffMargin)
    y = getMiddle(data.height/2+offset, data.height/2+rapOffHeight+offset)
    canvas.create_text(x, y, text = "Computer Rap Off", fill = "black", 
                                    font = "Helvetica 15")

def drawBeginButton(canvas, data):
    #draws one button: "begin"
    beginMargin, beginHeight = 70, 40
    canvas.create_rectangle(data.width/2-beginMargin, data.height/2, 
            data.width/2+beginMargin, data.height/2+beginHeight, fill = "gray")
    beginTextMargin = 20
    canvas.create_text(data.width/2, data.height/2+beginTextMargin, 
            text = "BEGIN", fill = "black", font = "Helvetica 15")

###########################################
# Info Screen Mode
###########################################

def infoScreenMousePressed(event, data):
    data.mouseX = event.x
    data.mouseY = event.y
    
def infoScreenKeyPressed(event, data):
    pass
    
def infoScreenTimerFired(data):
    backButtonPressed(data)
    if data.backButtonPressed == True:
        data.mouseX, data.mouseY = 0, 0 # reset mouse position
        data.currentScreen = data.prevScreen #keeps track of return screen
        data.backButtonPressed = False
    
def infoScreenRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, 
                                                    fill = data.backgroundColor)
    drawInfoButton(canvas, data)
    drawBackButton(canvas, data)
    title, titleMargin, textMargin = "INFORMATION", 100, 150
    canvas.create_text(data.width/2, titleMargin, text = title, 
                                    fill = "white", font = "Times 30 bold")
    who = "WHO: Shanel Huang (andrew ID: shanelh)"
    what = """WHAT: Rap Battle Bot is an application that generates \n
                response rap verses according to what your say."""
    where = "WHERE: Rap Battle Bot was developed at Carnegie Mellon University"
    when = "WHEN: Fall Semester 2016"
    why = "WHY: 15-112 Term Project"
    how = ("""HOW: This program uses a Markov chain algorithm and a \n
            collection of existing rap songs to predict a \n
            rap verse in relation to the user's speech""")
    textList = [who, what, where, when, why, how]
    space = [0, 50, 105, 145, 185, 250]
    for i in range(len(textList)):
        canvas.create_text(data.width/2, textMargin+space[i], 
                    text = textList[i], fill = "white", font = "Times 15" )

def drawBackButton(canvas, data):
    #returns to previous screen when pressed
    backWidth, backHeight = 125, 40
    x1, y1 = data.width-backWidth, data.height-backHeight
    canvas.create_rectangle(x1, y1, data.width, data.height, fill = "gray")
    canvas.create_text((x1+data.width)/2, (y1+data.height)/2, text = "BACK", 
                                                fill = "black")
    
def backButtonPressed(data):
    backWidth, backHeight = 125, 40
    xbound1, ybound1 = data.width-backWidth, data.height-backHeight
    xbound2, ybound2 = data.width, data.height
    if (data.mouseX >= xbound1 and data.mouseX <= xbound2):
        if data.mouseY >= ybound1 and data.mouseY <= ybound2:
            data.backButtonPressed = True
    
def drawInfoButton(canvas, data):
    margin = 15
    radius = 20
    canvas.create_oval(margin, data.height-margin-2*radius, margin+2*radius, 
            data.height-margin, fill = "light blue", outline = "black")
    x = getMiddle(margin, margin+2*radius)
    y = getMiddle(data.height-margin-2*radius, data.height-margin)
    canvas.create_text(x, y, text = "i", fill = "blue",font = "Times 20 italic") 
    
def infoButtonPressed(data):
    margin, radius = 15, 20
    xbound1, xbound2 = margin, margin+2*radius
    ybound1, ybound2 = data.height-margin-2*radius, data.height-margin
    if (data.mouseX >= xbound1 and data.mouseX <= xbound2):
        if data.mouseY >= ybound1 and data.mouseY <= ybound2:
            data.infoButtonPressed = True
    if data.infoButtonPressed == True:
        #reset mouse to prevent double clicking on next screen
        data.mouseX = 0 
        data.mouseY = 0
        data.prevScreen = data.currentScreen
        data.currentScreen = "info"
        data.infoButtonPressed = False
    
###########################################
# Audio Screen Mode
###########################################

def audioScreenMousePressed(event, data):
    data.mouseX = event.x
    data.mouseY = event.y

def audioScreenKeyPressed(event, data):
    pass

def audioScreenTimerFired(data):
    infoButtonPressed(data)
    timeButtonsPressed(data)
    recordButtonPressed(data)
    skipButtonPressed(data)

def timeButtonsPressed(data):
    fiveSecButtonPressed(data)
    tenSecButtonPressed(data)
    fifteenSecButtonPressed(data)
    recordButtonPressed(data)
    if data.recordButtonPressed == True:
        record(data)
        speechTuple = convertSpeechToText() #(speech as list, speech for display)
        data.speech = speechTuple[1]
        data.speechList = speechTuple[0]
        #reset mouse setting to prevent double click on next page 
        data.mouseX = 0 
        data.mouseY = 0
        #automatically moves to processing screen after done recording
        data.currentScreen = "processing"
        data.recordButtonPressed = False
        
def fiveSecButtonPressed(data):
    marginBetweenButtons, windowDistance = 25, 50
    buttonWidth, buttonHeight = 75, 25
    xbound1 = data.width/2-buttonWidth/2-buttonWidth-marginBetweenButtons
    ybound1 = 2*windowDistance
    xbound2 = data.width/2-buttonWidth/2-marginBetweenButtons
    ybound2 = ybound1 + buttonHeight
    if (data.mouseX >= xbound1 and data.mouseX <= xbound2):
        if data.mouseY >= ybound1 and data.mouseY <= ybound2:
            data.recordTime = 5
            #print("time set to 5 sec")

def tenSecButtonPressed(data):
    marginBetweenButtons, windowDistance = 25, 50
    buttonWidth, buttonHeight = 75, 25
    xbound1, ybound1 = data.width/2-buttonWidth/2, 2*windowDistance
    xbound2, ybound2 = xbound1 + buttonWidth, ybound1 + buttonHeight
    if (data.mouseX >= xbound1 and data.mouseX <= xbound2):
        if data.mouseY >= ybound1 and data.mouseY <= ybound2:
            data.recordTime = 10
            #print("time set to 10 sec")

def fifteenSecButtonPressed(data):
    marginBetweenButtons, windowDistance = 25, 50
    buttonWidth, buttonHeight = 75, 25
    xbound1 = data.width/2-buttonWidth/2+buttonWidth+marginBetweenButtons
    ybound1 =  2*windowDistance
    xbound2 = xbound1 + buttonWidth + marginBetweenButtons + buttonWidth
    ybound2 = ybound1 + buttonHeight
    if (data.mouseX >= xbound1 and data.mouseX <= xbound2):
        if data.mouseY >= ybound1 and data.mouseY <= ybound2:
            data.recordTime = 15
            #print("time set to 15 sec")
            
def drawRecordButton(canvas, data):
    directionsMargin, r = 100, 20
    c = 25
    directions = ("Press the record button to start" + "\n" +
                                    "recording. Then, start speaking.")
    canvas.create_text(data.width/2, data.height/2-directionsMargin, 
        text = directions, fill = "white", font = "Helvetica 20 bold")  
    canvas.create_oval(data.width/2-r, data.height/2-r-c, data.width/2+r, 
            data.height/2+r-c, fill = "red", outline = "black")
    canvas.create_text(data.width/2, data.height/2-c, text = "REC")    

def recordButtonPressed(data):
    #returns true when record button is pressed
    r, c = 20, 25
    xbound1 = data.width/2-r
    xbound2 = data.width/2+r
    ybound1 = data.height/2-r-c
    ybound2 = data.height/2+r-c
    if (data.mouseX >= xbound1 and data.mouseX <= xbound2):
        if data.mouseY >= ybound1 and data.mouseY <= ybound2:
            data.recordButtonPressed = True
    
def drawTimeButtons(canvas, data):
    marginBetweenButtons, windowDistance = 25, 50
    buttonWidth, buttonHeight = 75, 25
    x1, y1 = data.width/2-buttonWidth/2, 2*windowDistance
    x2, y2 = x1 + buttonWidth, y1 + buttonHeight
    canvas.create_rectangle(x1, y1, x2, y2, fill = "gray")
    tenMiddle, middleY = getMiddle(x1,x2), getMiddle(y1, y2)
    canvas.create_text(tenMiddle, middleY, text = "10 sec", fill = "black", 
                                                        font = "Helvetica 15")
    canvas.create_rectangle(x1-buttonWidth-marginBetweenButtons, y1, 
                    x1-marginBetweenButtons, y2, fill = "gray")
    fiveMiddle = getMiddle(x1-buttonWidth-marginBetweenButtons,
                                        x1-marginBetweenButtons)
    canvas.create_text(fiveMiddle, middleY, text = "5 sec", fill = "black", 
                                                        font = "Helvetica 15")
    canvas.create_rectangle(x2+marginBetweenButtons, y1, 
           x2 + marginBetweenButtons + buttonWidth, y2, fill = "gray")
    fifteenMiddle = getMiddle(x2+marginBetweenButtons, 
                                x2 + marginBetweenButtons + buttonWidth)
    canvas.create_text(fifteenMiddle, middleY, text = "15 sec", fill = "black", 
                                        font = "Helvetica 15")
    
def getMiddle(x1, x2):
    #returns the middle value of 2 numbers
    return (float(x1)+x2)/2
    
def audioScreenRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, 
                                                fill = data.backgroundColor)
    drawInfoButton(canvas, data)
    drawTimeButtons(canvas, data)
    drawRecordButton(canvas, data)
    timeMessage = "Select a time duration to record for: "
    marginBetweenButtons, windowDistance = 25, 50
    buttonWidth, buttonHeight = 75, 25
    canvas.create_text(data.width/2, windowDistance, text = timeMessage, 
        fill = "white", font = "Helvetica 17 bold")
    drawSkipRecord(canvas, data)
    
def drawSkipRecord(canvas, data):
    #draws one button on audio screen: "skip"
    skipMargin = 30
    option = "OR skip recording and generate a random verse: "
    canvas.create_text(data.width/2, data.height/2 + skipMargin, 
                    fill = "white", text = option, font = "Helvetica 17 bold")
    buttonWidth, buttonHeight = 50, 40
    startx, stopx = data.width/2-buttonWidth, data.width/2+buttonWidth
    starty = data.height/2+skipMargin + buttonHeight
    stopy = starty + buttonHeight
    canvas.create_rectangle(startx, starty, stopx, stopy, fill = "gray")
    canvas.create_text(getMiddle(startx, stopx), getMiddle(starty, stopy), 
            text = "SKIP", fill = "black")
    
def skipButtonPressed(data):
    #checks if skip button is pressed
    skipMargin = 30
    buttonWidth, buttonHeight = 50, 40
    xbound1, xbound2 = data.width/2-buttonWidth, data.width/2+buttonWidth
    ybound1 = data.height/2+skipMargin + buttonHeight
    ybound2 = ybound1 + buttonHeight
    if (data.mouseX >= xbound1 and data.mouseX <= xbound2):
        if data.mouseY >= ybound1 and data.mouseY <= ybound2:
            data.skipButtonPressed = True
    if data.skipButtonPressed == True:
        data.currentScreen = "response"
        data.skipButtonPressed = False
    
###########################################
# Convert Audio File to Text
###########################################

def convertSpeechToText():
    audio = readAudioFile()
    audioString = recognizeSpeech(audio)
    text = removePunctuation(audioString)
    textListWithU = text.split(" ")
    textList = removeU(textListWithU)
    textString = str(audioString)
    return (textList, textString)
    
def removeU(textList):
    #remvoes U from output of speech recognition module
    newList = []
    for word in textList:
        newList += [str(word)]
    return newList
    
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
    
# modified from python speech_recognition module audio transcribing example
# https://github.com/Uberi/speech_recognition/blob/master/examples
def readAudioFile():
    # obtain path to "english.wav" in the same folder as this script
    audioFile = path.join(path.dirname(path.realpath(__file__)), 
                                                            "audioFile.wav")
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(audioFile) as source:
        audio = r.record(source) # read the entire audio file
        return audio

# modified from python speech_recognition module audio transcribing example
# https://github.com/Uberi/speech_recognition/blob/master/examples   
def recognizeSpeech(audio):
    # recognize speech using Google Speech Recognition
    r = sr.Recognizer()
    try:
        speech = r.recognize_google(audio)
        print("You said: " + speech)
        return speech
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Could not generate results.; {0}".format(e))
        return ""

###########################################
# Record Audio to a Wave File
# modified from https://people.csail.mit.edu/hubert/pyaudio/
###########################################

def record(data):
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = data.recordTime
    CHUNK = 1024
    WAVE_OUTPUT_FILENAME = "audioFile.wav"
    p = pyaudio.PyAudio()

    #start recording
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    print("recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        
    print("finished recording")

    #stop recording
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

###########################################
# Processing Screen Mode
###########################################

def processingScreenMousePressed(event, data):
    data.mouseX = event.x
    data.mouseY = event.y

def processingScreenKeyPressed(event, data):
    pass

def processingScreenTimerFired(data):
    infoButtonPressed(data)
    responseButtonPressed(data)
    if data.responseButtonPressed == True:
        #reset mouse position after pressing button to prevent double click
        data.mouseX = 0
        data.mouseY = 0
        data.currentScreen = "response"
        #reset button setting
        data.responseButtonPressed = False

def responseButtonPressed(data):
    generateMargin, generateHeight = 100, 40
    generateTextMargin = 20
    xbound1, xbound2 = data.width/2-generateMargin, data.width/2+generateMargin
    ybound1, ybound2 = data.height/2, data.height/2+generateHeight
    if (data.mouseX >= xbound1 and data.mouseX <= xbound2):
        if data.mouseY >= ybound1 and data.mouseY <= ybound2:
            data.responseButtonPressed = True

def processingScreenRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, 
                                                fill = data.backgroundColor)
    drawInfoButton(canvas, data)
    data.speech = formatSpeech(data.speech)
    words = "Rap Battle Bot thinks you said: \n" + "\'" + data.speech + "\'"
    margin = 100 #distance from center
    canvas.create_text(data.width/2, data.height/2-margin, 
                text = words, fill = "white", font = "Helvetica 20 bold")
    generateMargin, generateHeight = 100, 40
    canvas.create_rectangle(data.width/2-generateMargin, data.height/2, 
        data.width/2+generateMargin, data.height/2+generateHeight, fill = "gray")
    generateTextMargin = 20 #distance between texts
    canvas.create_text(data.width/2, data.height/2+generateTextMargin, 
        text = "Generate Response Verse", fill = "black", font = "Helvetica 15")
        
def formatSpeech(speech):
    #prevents text from running off the page
    #returns a string of speech, formatted with max 5 words per line
    newSpeech = ""
    while len(speech.split()) > 5: 
        newSpeech += " ".join(speech.split()[0:5]) + " \n "
        speech = " ".join(speech.split()[5:])
    newSpeech += " ".join(speech.split())
    return newSpeech
    
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
    #returns same text with unicode line separators removed from web files
    newText = text.lower()
    newText = removePunctuation(newText)
    newText = newText.replace("\n", " ")
    newText = newText.replace("\xe2\x80\xa8", " ") #unicode line separator
    newText = newText.replace("\xe2\x80\x99", " ")
    newText = newText.replace("\xe2\x80\x94", " ")
    newText = newText.replace("\xe2\x80\x98", " ")
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
                freqDict[firstWord][secondWord] = (
                                        freqDict[firstWord].get(secondWord) + 1)
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
    
###########################################
# Response Screen Mode
###########################################

def responseScreenMousePressed(event, data):
    data.mouseX = event.x
    data.mouseY = event.y

def responseScreenKeyPressed(event, data):
    pass

def responseScreenTimerFired(data):
    infoButtonPressed(data)
    resetButtonPressed(data)
    if data.resetButtonPressed == True:
        init(data)

def responseScreenRedrawAll(canvas, data):
    if data.responseGenerated == False: #creates a response
        data.response = generateResponse(data.speechList, data.probDict)
        data.responseGenerated = True
    canvas.create_rectangle(0, 0, data.width, data.height, 
                                                fill = data.backgroundColor)
    drawInfoButton(canvas, data)
    actualResponse = "Robot Response: \n"  + data.response
    canvas.create_text(data.width/2, data.height/2, text = actualResponse ,
                                fill = "white", font = "Helvetica 20")
    drawResetButton(canvas,data)
    if data.responseScreenDrawn == False:
        data.responseScreenDrawn = True
        return
    if data.responseSpoken == False and data.responseScreenDrawn == True:
        response = data.response.replace("\n", " ")
        os.system("say" + " " + response)
        data.responseSpoken = True

def drawResetButton(canvas, data):
    resetWidth, resetHeight = 125, 40
    x1, y1 = data.width-resetWidth, data.height-resetHeight
    canvas.create_rectangle(x1, y1, data.width, data.height, fill = "gray")
    canvas.create_text((x1+data.width)/2, (y1+data.height)/2, text = "RESET", 
                                                fill = "black")
    
def resetButtonPressed(data):
    resetWidth, resetHeight = 125, 40
    xbound1, ybound1 = data.width-resetWidth, data.height-resetHeight
    xbound2, ybound2 = data.width, data.height
    if (data.mouseX >= xbound1 and data.mouseX <= xbound2):
        if data.mouseY >= ybound1 and data.mouseY <= ybound2:
            data.resetButtonPressed = True
    
###########################################
# Generate Verse
###########################################

def generateResponse(speechList, probDict):
    numVerses = pickVerseLength()
    response = ""
    acceptableRhymeList = []
    #print("speechList", speechList)
    for x in range(numVerses):
        if x % 2 == 0:
            rhymeWord = getLastWord(speechList, probDict)
            if rhymeWord in speechList: #to prevent repeats
                speechList.remove(rhymeWord)
                #speech list now doesn't include previous word
                #forces program to choose another word to rhyme with
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
    #returns one word
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
        try:
            rhymes = pronouncing.rhymes(word)
        except: # to prevent crash in case of no existing rhymes
            print("could not find rhymes")
            print(word)
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
# Rap Off Screen Mode
###########################################

def rapOffScreenMousePressed(event, data):
    data.mouseX = event.x
    data.mouseY = event.y
    
def rapOffScreenKeyPressed(event, data):
    pass

def rapOffScreenTimerFired(data):
    #every time the timer is fired, generate response from a different bot
    infoButtonPressed(data)
    stopButtonPressed(data)
    if data.stopButtonPressed == False:
        alternateBots(data)
    else: #stop button pressed defaults back to home screen
        init(data)

def alternateBots(data):
    print("verseCount: ", data.verseCount)
    if data.verseCount == 0: #generate starting verse
        data.bot1 = generateResponse(data.speechList, data.probDict)
        data.verseCount += 1
        print("bot1", data.bot1)
    else:
        if data.verseCount % 2 == 1: #bot2's turn
            temp = data.bot1
            data.bot2 = generateResponse(temp.split(), data.probDict)
            #print("bot1", temp)
        else: #bot1's turn
            temp = data.bot2
            data.bot1 = generateResponse(temp.split(), data.probDict)
            #print("bot2", temp)
        data.verseCount += 1
    
def rapOffScreenRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, 
                                                fill = data.backgroundColor)
    margin = 30
    canvas.create_line(0, getMiddle(0, data.height-margin), 
            data.width, getMiddle(0, data.height-margin), fill = "white")
    buttonWidth, buttonHeight = 50, 40
    drawInfoButton(canvas, data)
    canvas.create_rectangle(data.width/2-buttonWidth, data.height-margin-
      buttonHeight, data.width/2+buttonWidth, data.height-margin, fill = "red")
    x = getMiddle(data.width/2-buttonWidth, data.width/2+buttonWidth)
    y = getMiddle(data.height-margin-buttonHeight, data.height-margin)
    canvas.create_text(x, y, text = "STOP", fill = "black",
                                                font = "Times 15 bold")
    drawRapOffBots(canvas, data)
    drawBotResponses(canvas, data)

def drawBotResponses(canvas, data):
    margin = 20
    firstx, firsty = data.width/2, (data.height/2)/2
    secondx, secondy = data.width/2, getMiddle(data.height-margin,data.height/2)
    canvas.create_text(firstx, firsty, text = data.bot1, fill = "white",
                                                        font = "Times 15")
    canvas.create_text(secondx, secondy, text = data.bot2, fill = "white",
                                                        font = "Times 15")
                                                        
def stopButtonPressed(data):
    buttonWidth, buttonHeight = 50, 40
    margin = 30
    xbound1, xbound2 = data.width/2-buttonWidth, data.width/2+buttonWidth
    ybound1, ybound2 = data.height-margin-buttonHeight, data.height-margin
    if (data.mouseX >= xbound1 and data.mouseX <= xbound2):
        if data.mouseY >= ybound1 and data.mouseY <= ybound2:
            data.stopButtonPressed = True
    
def drawRapOffBots(canvas, data):
    middle1 = getMiddle(0, data.width/2)
    middle2 = getMiddle(data.width/2, data.width)
    margin = 20
    canvas.create_text(data.width/2, margin, text = "BOT 1", fill = "white", 
                                                        font = "Times 15")
    canvas.create_text(data.width/2, (data.height-margin)/2 + margin, 
                        text = "BOT 2", fill = "white", font = "Times 15")
    
###########################################
# run function modified from 15-112 course notes
###########################################

def runApp(): 
    width = 600
    height = 600
    run(width, height)
    
def run(width=400, height=400):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    def buttonPressed(data):
        data.currentScreen = "audio"
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root, canvas, and button
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    #data.mybutton = Button(root, text = "Begin", command = buttonPressed(data))
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
    
###########################################
# Test Functions
###########################################

def testIsolateTextFiles():
    print("testing isolateTextFiles()....")
    filesList1 =  []
    filesList2 = ["one.txt", "two.txt", "three.txt"]
    filesList3 = ["one.txt",  "notATextFile"]
    assert(isolateTextFiles(filesList1) == filesList1)
    assert(isolateTextFiles(filesList2) == filesList2)
    assert(isolateTextFiles(filesList3) == ["one.txt"])
    print("Passed!")

def testRemovePunctuation():
    print("testing removePunctuation().....")
    txt1 = "Hello, my name is Shanel."
    ans1 = "Hello my name is Shanel"
    assert(removePunctuation(txt1) == ans1)
    print("Passed!")

def testGetRhymes():
    print("tesing getRhymes().......")
    rhymes = pronouncing.rhymes("sleekly")
    expected = [
        'beakley', 'biweekly', 'bleakley', 'meekly', 'obliquely',
        'steakley', 'szekely', 'uniquely', 'weakley', 'weakly',
        'weekley', 'weekly', 'yeakley']
    assert(expected == rhymes)
    print("Passed!")

def testFormatSpeech():
    print("testing formatSpeech().........")
    speech1 = "something with frustration when she keep saying anything stop"
    speech2 = "something exactly five single words"
    speech3 = "under 5 words"
    ans1 = 'something with frustration when she \n keep saying anything stop'
    assert(formatSpeech(speech1) == ans1)
    assert(formatSpeech(speech2) == speech2)
    assert(formatSpeech(speech3) == speech3)
    print("Passed!")
    
#testIsolateTextFiles()
#testRemovePunctuation()
#testGetRhymes
#testFormatSpeech()

runApp()