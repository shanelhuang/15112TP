###########################################
# Rap Battle Bot
#
# NAME: Shanel Huang
# ANDREW ID: shanelh
# SECTION: F
# DATE: November 2016
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
    data.backgroundColor = "black"
    data.mouseX, data.mouseY = 0, 0
    data.beginButtonPressed = False
    data.recordButtonPressed = False
    data.responseButtonPressed = False
    data.responseGenerated = False
    data.responseSpoken = False
    data.responseScreenDrawn = False
    data.resetButtonPressed = False
    data.recordTime = 5
    data.speech = ""
    data.speechList = []
    data.probDict = dict()
    
def mousePressed(event, data):
    if data.currentScreen == "home": 
        homeScreenMousePressed(event, data)
    elif data.currentScreen == "audio": 
        audioScreenMousePressed(event, data)
    elif data.currentScreen == "processing": 
        processingScreenMousePressed(event, data)
    elif data.currentScreen == "response": 
        responseScreenMousePressed(event, data)
    
def keyPressed(event, data):
    if data.currentScreen == "home": 
        homeScreenKeyPressed(event, data)
    elif data.currentScreen == "audio": 
        audioScreenKeyPressed(event, data)
    elif data.currentScreen == "processing":
        processingScreenMousePressed(event, data)
    elif data.currentScreen == "response":
        responseScreenMousePressed(event, data)
    
def timerFired(data):
    if data.currentScreen == "home": 
        homeScreenTimerFired(data)
    elif data.currentScreen == "audio": 
        audioScreenTimerFired(data)
    elif data.currentScreen == "processing":
        processingScreenTimerFired(data)
    elif data.currentScreen == "response":
        responseScreenTimerFired(data)
    
def redrawAll(canvas, data):
    if data.currentScreen == "home": 
        homeScreenRedrawAll(canvas, data)
    elif data.currentScreen == "audio":
        audioScreenRedrawAll(canvas, data)
    elif data.currentScreen == "processing":
        processingScreenRedrawAll(canvas, data)
    elif data.currentScreen == "response":
        responseScreenRedrawAll(canvas, data)

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
    beginButtonPressed(data)
    #when begin button is pressed, app moves on to audio screen
    if data.beginButtonPressed == True:
        #reset mouse to prevent double clicking on next screen
        data.mouseX = 0 
        data.mouseY = 0
        data.currentScreen = "audio"

def homeScreenRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, 
                                                fill = data.backgroundColor)
    title, titleMargin = "RAP BATTLE BOT!", 150
    canvas.create_text(data.width/2, data.height/2-titleMargin, text = title, 
                                    fill = "white", font = "Helvetica 50 bold")
    directions, directionsMargin = "click to start", 25
    canvas.create_text(data.width/2, data.height/2-directionsMargin, 
            text = directions, fill = "white", font = "Helvetica 20 bold")
    #draw begin button 
    beginMargin, beginHeight = 70, 40
    canvas.create_rectangle(data.width/2-beginMargin, data.height/2, 
            data.width/2+beginMargin, data.height/2+beginHeight, fill = "gray")
    beginTextMargin = 20
    canvas.create_text(data.width/2, data.height/2+beginTextMargin, 
            text = "begin", fill = "black", font = "Helvetica 15")
            

###########################################
# Audio Screen Mode
###########################################

def audioScreenMousePressed(event, data):
    data.mouseX = event.x
    data.mouseY = event.y

def audioScreenKeyPressed(event, data):
    pass

def audioScreenTimerFired(data):
    timeButtonsPressed(data)
    recordButtonPressed(data)

def recordButtonPressed(data):
    #returns true when record button is pressed
    r, c = 20, 30
    xbound1 = data.width/2-r
    xbound2 = data.width/2+r
    ybound1 = data.height/2+c-r
    ybound2 = data.height/2+c+r
    if (data.mouseX >= xbound1 and data.mouseX <= xbound2):
        if data.mouseY >= ybound1 and data.mouseY <= ybound2:
            data.recordButtonPressed = True

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
            print("time set to 5 sec")

def tenSecButtonPressed(data):
    marginBetweenButtons, windowDistance = 25, 50
    buttonWidth, buttonHeight = 75, 25
    xbound1, ybound1 = data.width/2-buttonWidth/2, 2*windowDistance
    xbound2, ybound2 = xbound1 + buttonWidth, ybound1 + buttonHeight
    if (data.mouseX >= xbound1 and data.mouseX <= xbound2):
        if data.mouseY >= ybound1 and data.mouseY <= ybound2:
            data.recordTime = 10
            print("time set to 10 sec")

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
            print("time set to 15 sec")
            
def drawRecordButton(canvas, data):
    directionsMargin = 46
    directions = ("Press the record button to start" + "\n" +
                                    "recording. Then, start speaking.")
    canvas.create_text(data.width/2, data.height/2-directionsMargin, 
        text = directions, fill = "white", font = "Helvetica 20 bold")  
    r, c = 20, 30
    canvas.create_oval(data.width/2-r, data.height/2+c-r, data.width/2+r, 
            data.height/2+c+r, fill = "red", outline = "black")
    canvas.create_text(data.width/2, data.height/2+c, text = "REC")    
    
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
    return (x1+x2)/2
    
def audioScreenRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, 
                                                fill = data.backgroundColor)
    drawRecordButton(canvas, data)
    timeMessage = "Select a time duration to record for: "
    marginBetweenButtons, windowDistance = 25, 50
    buttonWidth, buttonHeight = 75, 25
    canvas.create_text(data.width/2, windowDistance, text = timeMessage, 
        fill = "white", font = "Helvetica 17 bold")
    drawTimeButtons(canvas, data)

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
    responseButtonPressed(data)
    if data.responseButtonPressed == True:
        data.mouseX = 0
        data.mouseY = 0
        data.currentScreen = "response"

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
    words = "Rap Battle Bot thinks you said: \n" + "\'" + data.speech + "\'"
    margin = 100
    canvas.create_text(data.width/2, data.height/2-margin, 
                text = words, fill = "white", font = "Helvetica 20 bold")
    generateMargin, generateHeight = 100, 40
    canvas.create_rectangle(data.width/2-generateMargin, data.height/2, 
        data.width/2+generateMargin, data.height/2+generateHeight, fill = "gray")
    generateTextMargin = 20
    canvas.create_text(data.width/2, data.height/2+generateTextMargin, 
        text = "Generate Response Verse", fill = "black", font = "Helvetica 15")
        
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
    resetButtonPressed(data)
    if data.resetButtonPressed == True:
        init(data)

def responseScreenRedrawAll(canvas, data):
    data.probDict = processAllTexts()
    if data.responseGenerated == False: #creates a response
        data.response = generateResponse(data.speechList, data.probDict)
        data.responseGenerated = True
    canvas.create_rectangle(0, 0, data.width, data.height, 
                                                fill = data.backgroundColor)
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
    print(data.mouseX, data.mouseY)
    print(xbound1, xbound2)
    print(ybound1, ybound2)
    if (data.mouseX >= xbound1 and data.mouseX <= xbound2):
        if data.mouseY >= ybound1 and data.mouseY <= ybound2:
            data.resetButtonPressed = True
    
###########################################
# Generate Verse
###########################################

def generateResponse(speechList, probDict):
    numVerses = 4
    response = ""
    for x in range(numVerses):
        if x == 0:
            rhymeWord = getLastWord(speechList, probDict)
            acceptableRhymeList = getAceptableRhymes(rhymeWord, probDict)
            newLine = makeRapVerse(speechList, probDict, rhymeWord)
        else:
            rhymeWord = random.choice(acceptableRhymeList)
            newLine = makeRapVerse(speechList, probDict, rhymeWord)
        response += newLine + " \n "
    return response

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
    if lastWord == -1: #could not find a word in dictionary that rhymes
        lastWord = random.choice(list(probDict.keys()))
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
    for element in pronouncing.rhymes(word):
        rhymeList += [str(element)]
    return rhymeList

def getAceptableRhymes(word, probDict): 
    #returns a list of words that rhyme with words and are also in probDict
    acceptableRhymes = []
    rhymeList = getRhymes(word)
    for word in rhymeList:
        if word in rhymeList:
            acceptableRhymes.append(word)
    return acceptableRhymes
    
###########################################
# run function modified from 15-112 course notes
###########################################

def runApp(): 
    width = 500
    height = 500
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

def test_rhymes():
    rhymes = pronouncing.rhymes("sleekly")
    expected = [
        'beakley', 'biweekly', 'bleakley', 'meekly', 'obliquely',
        'steakley', 'szekely', 'uniquely', 'weakley', 'weakly',
        'weekley', 'weekly', 'yeakley']
    assertEqual(expected, rhymes)
    
#testIsolateTextFiles()
#testRemovePunctuation()
#test_rhymes 
runApp()