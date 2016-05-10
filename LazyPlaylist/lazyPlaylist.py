from tkinter import *

import pyaudio
import threading
from selenium import webdriver
from bs4 import BeautifulSoup

import wave, array, math, time, argparse, sys
import numpy, pywt
from scipy import signal
import pdb
import os
####################################
# init
####################################

def init(data):
    imageInit(data)
    audioInit(data)
    data.mode = "startScreen"
    data.backX = 15
    data.backY = 15
    startScreenInit(data)
    workoutInit(data)
    data.userInputAge = None
    data.lyrics = None
    data.actualAge = None
    data.targetHeartRate = None
    data.skipNextX = data.playButtonX + 50
    data.skipNextY = data.playButtonY  
    data.skipPrevX = data.playButtonX - 50
    data.skipPrevY = data.playButtonY 
    data.finalLyrics, data.level = None, None
    data.rDiff = 1
    data.red, data.green, data.blue  = 188, 65, 106
    data.up = True
    data.playlistLen = None
    data.notEnough = False
    data.buttonCol = rgbString(143, 188, 233)
    data.peakInfo = []

def rgbString(red, green, blue): # taken from graphics notes
    return "#%02x%02x%02x" % (red, green, blue)

def imageInit(data):
    data.backImage = PhotoImage(file='back.gif')
    data.skipImage = PhotoImage(file = 'skipnext.gif')
    data.prevImage = PhotoImage(file = 'prev.gif')

####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if (data.mode == "startScreen"): startScreenMousePressed(event, data)
    elif (data.mode == "cannot make"): cannotMousePressed(event, data)
    elif (data.mode == "workout"): workoutMousePressed(event, data)
    elif (data.mode == "study") : playerMousePressed(event, data)
    elif (data.mode == "sleep") : playerMousePressed(event, data)
    elif (data.mode == "random") : playerMousePressed(event, data)
    elif (data.mode == "rock") : playerMousePressed(event, data)
    elif (data.mode == "hype") : playerMousePressed(event, data)
    elif(data.mode == "loading"): loadingMousePressed(event, data)
    elif(data.mode == "chooseLen"): chooseLenMousePressed(event, data)
    elif (data.mode == "beginner"):   playerMousePressed(event, data)
    elif (data.mode == "intermediate"): playerMousePressed(event, data)
    elif (data.mode == "experienced"): playerMousePressed(event, data)
    elif (data.mode == "finished"): finishedMousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "startScreen"): startScreenKeyPressed(event, data)
    elif (data.mode == "cannot make"): cannotKeyPressed(event, data)
    elif (data.mode == "workout"): workoutKeyPressed(event, data)
    elif (data.mode == "study") : playerKeyPressed(event, data)
    elif (data.mode == "sleep") : playerKeyPressed(event, data)
    elif (data.mode == "random") : playerKeyPressed(event, data)
    elif (data.mode == "rock") : playerKeyPressed(event, data)
    elif (data.mode == "hype") : playerKeyPressed(event, data)
    elif(data.mode == "loading"): loadingKeyPressed(event, data)
    elif(data.mode == "chooseLen"): chooseLenKeyPressed(event, data)
    elif (data.mode == "beginner"):   playerKeyPressed(event, data)
    elif (data.mode == "intermediate"): playerKeyPressed(event, data)
    elif (data.mode == "experienced"): playerKeyPressed(event, data)
    elif (data.mode == "finished"): finishedKeyPressed(event, data)

def timerFired(data):
    colorLim, colorChanger = 200, 100
    if(data.mode == "loading"): loadingTimerFired(data)
    if data.rDiff == colorLim: data.up = False
    elif data.rDiff == 0: data.up = True
    if data.up: data.rDiff += 1
    else: data.rDiff -= 1
    if data.rDiff != colorLim:
        data.red = data.rDiff % colorLim
    elif data.rDiff % colorChanger == 1:
        data.rDiff = 1
    data.backgroundColor = rgbString(data.red, data.green, data.blue)
    if (data.mode == "startScreen"): startScreenTimerFired(data)
    elif (data.mode == "workout"): workoutTimerFired(data)
    elif (data.mode == "cannot make"): cannotTimerFired(data)
    elif (data.mode == "study") : playerTimerFired(data)
    elif (data.mode == "sleep") : playerTimerFired(data)
    elif (data.mode == "random") : playerTimerFired(data)
    elif (data.mode == "rock") : playerTimerFired(data)
    elif (data.mode == "hype") : playerTimerFired(data)
    elif(data.mode == "chooseLen"): chooseLenTimerFired(data)
    elif (data.mode == "beginner"):   playerTimerFired(data)
    elif (data.mode == "intermediate"): playerTimerFired(data)
    elif (data.mode == "experienced"): playerTimerFired(data)
    elif (data.mode == "finished"): finishedTimerFired(data)

def redrawAll(canvas, data):  
    canvas.create_rectangle(0, 0, data.width,data.height,
                                    fill = data.backgroundColor)
    if (data.mode == "startScreen"): startScreenRedrawAll(canvas, data)
    elif (data.mode == "cannot make"): cannotRedrawAll(canvas, data)
    elif (data.mode == "workout"): workoutRedrawAll(canvas, data)
    elif (data.mode == "study") : studyRedrawAll(canvas, data)
    elif (data.mode == "sleep") : sleepRedrawAll(canvas, data)
    elif (data.mode == "random") : randomRedrawAll(canvas, data)
    elif (data.mode == "rock") : rockRedrawAll(canvas, data)
    elif (data.mode == "hype") : hypeRedrawAll(canvas, data)
    elif (data.mode == "chooseLen"): chooseLenRedrawAll(canvas, data)
    elif (data.mode == "loading"): loadingRedrawAll(canvas, data)
    elif (data.mode == "beginner"):   beginnerRedrawAll(canvas, data)
    elif (data.mode == "intermediate"): intermediateRedrawAll(canvas, data)
    elif (data.mode == "experienced"): experiencedRedrawAll(canvas, data)
    elif (data.mode == "finished"): finishedRedrawAll(canvas, data)

####################################
# startScreen mode
####################################

def startScreenInit(data):
    data.titleAdjust = 90
    data.descpAdjust = 20   
    data.studyX = 190
    data.studyY = 300
    data.sleepX = 300
    data.sleepY = 300
    data.randomX = 410
    data.randomY = 300
    data.rockX = data.studyX
    data.rockY = 350
    data.hypeX = data.sleepX
    data.hypeY = 350
    data.workX = data.randomX
    data.workY = 350
    data.buttonWidth = 50
    data.buttonHeight = 50
    data.nextMode = None
    
def startScreenMousePressed(event, data):
    if clickOn(data.workX, data.workY, data.workX + data.buttonWidth, 
                        data.workY + data.buttonHeight, event.x, event.y):
            data.mode = "chooseLen" 
            data.nextMode = "workout"
    elif clickOn(data.studyX, data.studyY, data.studyX + data.buttonWidth, 
                        data.studyY + data.buttonHeight, event.x, event.y):
            data.mode = "chooseLen"     
            data.nextMode = "study"
    elif clickOn(data.sleepX, data.sleepY, data.sleepX + data.buttonWidth, 
                        data.sleepY + data.buttonHeight, event.x, event.y):
            data.mode = "chooseLen"     
            data.nextMode = "sleep"
    elif clickOn(data.randomX, data.randomY, data.randomX + data.buttonWidth, 
                        data.randomY + data.buttonHeight, event.x, event.y):
            data.mode = "chooseLen"     
            data.nextMode = "random"
    elif clickOn(data.rockX, data.rockY, data.rockX + data.buttonWidth, 
                        data.rockY + data.buttonHeight, event.x, event.y):
            data.mode = "chooseLen"     
            data.nextMode = "rock"
    elif clickOn(data.hypeX, data.hypeY, data.hypeX + data.buttonWidth, 
                        data.hypeY + data.buttonHeight, event.x, event.y):
            data.mode = "chooseLen"      
            data.nextMode = "hype"
    

def startScreenKeyPressed(event, data):
    pass

def startScreenTimerFired(data):
    audioTimerFired(data)

def drawMusicChoiceButtons(canvas, data):
    canvas.create_text(data.width/2, data.height/2-data.titleAdjust,
                       text="lazy playlist.", fill = data.titleGrey, 
                       font="verdana 60")
    canvas.create_text(data.width/2, data.height/2-data.descpAdjust,
      text="Choose what type of music you're in the mood for:", 
                    fill = data.textGrey, font="Helvetica 20")
    canvas.create_rectangle(data.workX, data.workY, 
            data.workX + data.buttonWidth, data.workY + data.buttonHeight, 
                fill = data.buttonCol, outline = "")
    canvas.create_rectangle(data.studyX, data.studyY, 
            data.studyX + data.buttonWidth, data.studyY + data.buttonHeight, 
                fill = data.buttonCol, outline = "")
    canvas.create_rectangle(data.sleepX, data.sleepY, 
            data.sleepX + data.buttonWidth, data.sleepY + data.buttonHeight, 
            fill = data.buttonCol, outline = "")
    canvas.create_rectangle(data.randomX, data.randomY, 
            data.randomX + data.buttonWidth, data.randomY + data.buttonHeight, 
            fill = data.buttonCol, outline = "")
    canvas.create_rectangle(data.rockX, data.rockY, 
                data.rockX + data.buttonWidth, data.rockY + data.buttonHeight, 
            fill = data.buttonCol, outline = "")
    canvas.create_rectangle(data.hypeX, data.hypeY, 
                data.hypeX + data.buttonWidth, data.hypeY + data.buttonHeight, 
            fill = data.buttonCol, outline = "")

def drawMusicChoiceText(canvas, data):
    canvas.create_text(data.workX + data.buttonWidth//2, 
                        data.workY + data.buttonHeight//2, text = "Exercise")
    canvas.create_text(data.studyX + data.buttonWidth//2, 
                        data.studyY + data.buttonHeight//2, text = "Study")
    canvas.create_text(data.sleepX + data.buttonWidth//2, 
                        data.sleepY + data.buttonHeight//2, text = "Sleep")
    canvas.create_text(data.randomX + data.buttonWidth//2, 
                        data.randomY + data.buttonHeight//2, text = "Random")
    canvas.create_text(data.rockX + data.buttonWidth//2, 
                        data.rockY + data.buttonHeight//2, text = "Rock")
    canvas.create_text(data.hypeX + data.buttonWidth//2, 
                        data.hypeY + data.buttonHeight//2, text = "Hype")

def startScreenRedrawAll(canvas, data):
    data.titleGrey = rgbString(238, 230, 223)
    data.textGrey = rgbString(226, 221, 216)
    drawMusicChoiceButtons(canvas, data)
    drawMusicChoiceText(canvas, data)

####################################
# cannot make mode
####################################
def cannotMousePressed(event, data):
    goBack(data, event.x, event.y)

def cannotKeyPressed(event, data):
    pass

def cannotTimerFired(data):
    audioTimerFired(data)

def cannotRedrawAll(canvas, data):
    drawBackButton(canvas, data)
    canvas.create_text(data.width//2, data.height//2, 
        text = "You don't have enough songs for such a playlist! \
                Please go back and choose a new playlist.")


####################################
# chooseLen mode
####################################
def chooseLenVars(data):
    data.boxSize = 50
    data.X1 = 100
    data.Y1 = 250
    data.X2 = data.X1 + data.boxSize
    data.Y2 = data.Y1
    data.X3 = data.X1 + 2*data.boxSize
    data.Y3 = data.Y1
    data.X4 = data.X1 + 3*data.boxSize
    data.Y4 = data.Y1
    data.X5 = data.X1 + 4* data.boxSize
    data.Y5 = data.Y1
    data.X6 = data.X1 + 5* data.boxSize
    data.Y6 = data.Y1
    data.X7 = data.X1 + 6 * data.boxSize
    data.Y7 = data.Y1
    data.X8 = data.X1 + 7 * data.boxSize
    data.Y8 = data.Y1
    data.X9 = data.X1 + 8 * data.boxSize
    data.Y9 = data.Y1
    data.X10 = data.X1 + 9 * data.boxSize
    data.Y10 = data.Y1
    data.numW = data.numH =40
    textVars(data)

def textVars(data):
    data.X1Text = data.X1 + data.numW//2
    data.Y1Text = data.Y1 + data.numH//2
    data.X2Text = data.X2 + data.numW//2
    data.Y2Text = data.Y2 + data.numH//2
    data.X3Text = data.X3 + data.numW//2
    data.Y3Text = data.Y3 + data.numH//2
    data.X4Text = data.X4 + data.numW//2
    data.Y4Text = data.Y4 + data.numH//2
    data.X5Text = data.X5 + data.numW//2
    data.Y5Text = data.Y5 + data.numH//2
    data.X6Text = data.X6 + data.numW//2
    data.Y6Text = data.Y6 + data.numH//2
    data.X7Text = data.X7 + data.numW//2
    data.Y7Text = data.Y7 + data.numH//2
    data.X8Text = data.X8 + data.numW//2
    data.Y8Text = data.Y8 + data.numH//2
    data.X9Text = data.X9 + data.numW//2
    data.Y9Text = data.Y9 + data.numH//2
    data.X10Text = data.X10 + data.numW//2
    data.Y10Text = data.Y10 + data.numH//2

def chooseLenMousePressed(event, data):
    goBack(data, event.x, event.y)
    chooseLenVars(data)
    if clickOn(data.X1, data.Y1, data.X1 + data.buttonWidth, 
                        data.Y1 + data.buttonHeight, event.x, event.y):
        data.getPlaylist = True
        data.mode = "loading"
        data.playlistLen = 1
    elif clickOn(data.X2, data.Y2, data.X2 + data.buttonWidth, 
                        data.Y2 + data.buttonHeight, event.x, event.y):
        data.getPlaylist = True
        data.mode = "loading"
        data.playlistLen = 2
    elif clickOn(data.X3, data.Y3, data.X3 + data.buttonWidth, 
                        data.Y3 + data.buttonHeight, event.x, event.y):
        data.getPlaylist = True
        data.mode = "loading"
        data.playlistLen = 3
    elif clickOn(data.X4, data.Y4, data.X4 + data.buttonWidth, 
                        data.Y4 + data.buttonHeight, event.x, event.y):
        data.getPlaylist = True
        data.mode = "loading"
        data.playlistLen = 4
    elif clickOn(data.X5, data.Y5, data.X5 + data.buttonWidth, 
                        data.Y5 + data.buttonHeight, event.x, event.y):
        data.getPlaylist = True
        data.mode = "loading"
        data.playlistLen = 5
    elif clickOn(data.X6, data.Y6, data.X6 + data.buttonWidth, 
                        data.Y6 + data.buttonHeight, event.x, event.y):
        data.getPlaylist = True
        data.mode = "loading"
        data.playlistLen = 6
    elif clickOn(data.X7, data.Y7, data.X7 + data.buttonWidth, 
                        data.Y7 + data.buttonHeight, event.x, event.y):
        data.getPlaylist = True
        data.mode = "loading"
        data.playlistLen = 7
    elif clickOn(data.X8, data.Y8, data.X8 + data.buttonWidth, 
                        data.Y8 + data.buttonHeight, event.x, event.y):
        data.getPlaylist = True
        data.mode = "loading"
        data.playlistLen = 8
    elif clickOn(data.X9, data.Y9, data.X9 + data.buttonWidth, 
                        data.Y9 + data.buttonHeight, event.x, event.y):
        data.getPlaylist = True
        data.mode = "loading"
        data.playlistLen = 9
    elif clickOn(data.X10, data.Y10, data.X10 + data.buttonWidth, 
                        data.Y10 + data.buttonHeight, event.x, event.y):
        data.getPlaylist = True
        data.mode = "loading"
        data.playlistLen = 10
    if data.nextMode == "workout" and data.level == None: data.mode = "workout"
    
def chooseLenKeyPressed(event, data):
    pass

def chooseLenTimerFired(data):
    audioTimerFired(data)

def makeChoicesText(canvas, data):
    canvas.create_text(data.X1Text, data.Y1Text, text = "1")
    canvas.create_text(data.X2Text, data.Y2Text, text = "2")
    canvas.create_text(data.X3Text, data.Y3Text, text = "3")
    canvas.create_text(data.X4Text, data.Y4Text, text = "4")
    canvas.create_text(data.X5Text, data.Y5Text, text = "5")
    canvas.create_text(data.X6Text, data.Y6Text, text = "6")
    canvas.create_text(data.X7Text, data.Y7Text, text = "7")
    canvas.create_text(data.X8Text, data.Y8Text, text = "8")
    canvas.create_text(data.X9Text, data.Y9Text, text = "9")
    canvas.create_text(data.X10Text, data.Y10Text, text = "10")

def chooseLenRedrawAll(canvas, data):
    drawBackButton(canvas, data)
    chooseLenVars(data)
    textY = 200
    textYAdj = 400
    textYAdj2 = 430

    canvas.create_text(data.width//2, textY, 
        text = "Choose the desired playlist length:", font = "verdana 20",
                    fill = data.textGrey)
    canvas.create_text(data.width//2, textYAdj, 
        text = "If you don't have enough songs to fill your chosen playlist ", 
        font = "verdana 16",
                    fill = data.textGrey)
    canvas.create_text(data.width//2, textYAdj2, 
        text = "length, it will make a playlist with as many songs as it can:", 
        font = "verdana 16",
                    fill = data.textGrey)
    canvas.create_oval(data.X1, data.Y1, data.X1 + data.numW, 
                   data.Y1 + data.numH, fill = data.buttonCol,
                                        outline = "")
    canvas.create_oval(data.X2, data.Y2, data.X2 + data.numW, 
                   data.Y2 + data.numH, fill = data.buttonCol,
                                        outline = "")
    canvas.create_oval(data.X3, data.Y3, data.X3 + data.numW, 
                   data.Y3 + data.numH, fill = data.buttonCol,
                                        outline = "")
    canvas.create_oval(data.X4, data.Y4, data.X4 + data.numW, 
                   data.Y4 + data.numH, fill = data.buttonCol,
                                        outline = "")
    canvas.create_oval(data.X5, data.Y5, data.X5 + data.numW, 
                   data.Y5 + data.numH, fill = data.buttonCol,
                                        outline = "")
    canvas.create_oval(data.X6, data.Y6, data.X6 + data.numW, 
                   data.Y6 + data.numH, fill = data.buttonCol,
                                        outline = "")
    canvas.create_oval(data.X7, data.Y7, data.X7 + data.numW, 
                   data.Y7 + data.numH, fill = data.buttonCol,
                                        outline = "")
    canvas.create_oval(data.X8, data.Y8, data.X8 + data.numW, 
                   data.Y8 + data.numH, fill = data.buttonCol,
                                        outline = "")
    canvas.create_oval(data.X9, data.Y9, data.X9 + data.numW, 
                   data.Y9 + data.numH, fill = data.buttonCol,
                                        outline = "")
    canvas.create_oval(data.X10, data.Y10, data.X10 + data.numW, 
                   data.Y10 + data.numH, fill = data.buttonCol,
                                        outline = "")
    makeChoicesText(canvas, data)

####################################
# workout mode
####################################
def workoutInit(data):
    data.ageAdjust = 25
    data.begX = int(data.width*(2/10))
    data.begY = data.height/2+data.ageAdjust+20
    data.intX = data.begX + 150
    data.intY = data.begY
    data.advX = data.begX + 300
    data.advY = data.begY
    data.buttonWidth = 100
    data.buttonHeight = 40
    data.begTextX= data.begX + data.buttonWidth//2
    data.begTextY = data.begY + data.buttonHeight//2
    data.intTextX= data.intX + data.buttonWidth//2
    data.intTextY = data.intY + data.buttonHeight//2
    data.advTextX= data.advX + data.buttonWidth//2
    data.advTextY = data.advY + data.buttonHeight//2
    data.backX, data.backY = 20, 20
    data.backImageW = 20
    data.skipImageW = 50
    data.remove = False
    data.clickAge = False
    data.getPlaylist = False

def workoutMousePressed(event, data):
    goBack(data, event.x, event.y)
    if data.remove:
        data.getPlaylist = True
        if clickOn(data.begX, data.begY, data.begX + data.buttonWidth, 
                        data.begY + data.buttonHeight, event.x, event.y):      
            data.level = "beginner"
            getTargetBPMs(data)            
            data.mode = "loading"

        elif clickOn(data.intX, data.intY, data.intX + data.buttonWidth, 
                        data.intY + data.buttonHeight, event.x, event.y):
            data.level = "intermediate"
            getTargetBPMs(data)
            data.mode = "loading"

        elif clickOn(data.advX, data.advY, data.advX + data.buttonWidth, 
                        data.advY + data.buttonHeight, event.x, event.y):
            data.level = "experienced"
            getTargetBPMs(data)
            data.mode = "loading"

    elif clickOn(data.boxX1, data.boxY1, data.boxX2, data.boxY2, 
                         event.x, event.y):
        data.clickAge = True

def workoutKeyPressed(event, data):
    if data.clickAge:
        if event.keysym in "0123456789":
            if data.userInputAge == None:
                data.userInputAge = event.keysym
            else:
                data.userInputAge += event.keysym
        elif event.keysym == "BackSpace":
            data.userInputAge = data.userInputAge[:-1]
        elif event.keysym == "Return":
            data.actualAge = data.userInputAge
            if data.userInputAge != None:
                data.clickAge = False
                data.remove = True

def workoutTimerFired(data):
    audioTimerFired(data)

def drawTextAndButtons(canvas, data): 
    canvas.create_text(data.width/2, data.height/2,
                    text="Choose a level of fitness:", 
                    fill = data.textGrey, font="Helvetititca 16")
    canvas.create_rectangle(data.begX, data.begY, data.begX + data.buttonWidth,
                                data.begY + data.buttonHeight, 
                                outline = "")
    canvas.create_text(data.begTextX, data.begTextY, text = "beginner", 
                        fill = "white", font="Helvetica 16")
    canvas.create_rectangle(data.intX, data.intY, data.intX + data.buttonWidth,
                                data.intY + data.buttonHeight, 
                                outline = "")
    canvas.create_text(data.intTextX, data.intTextY, text = "intermediate", 
                        fill = "white", font="Helvetica 16")
    canvas.create_rectangle(data.advX, data.advY, data.advX + data.buttonWidth,
                                data.advY + data.buttonHeight, 
                                outline = "")
    canvas.create_text(data.advTextX, data.advTextY, text = "experienced", 
                        fill = "white", font="Helvetica 16")

def drawTextBox(canvas, data):
    if data.clickAge == True: color = rgbString(172, 201, 233)
    else: color = rgbString(143, 188, 233)
    selCol = rgbString(98, 151, 233)
    ageY = data.height//2 + 60
    data.ageBoxW, data.ageBoxH = 60, 15
    data.ageTextAdj, data.boxDiff = 9, 5
    data.boxX1 = data.width//2-data.ageBoxW
    data.boxY1 = ageY-data.ageBoxH
    data.boxX2 = data.width//2+data.ageBoxW
    data.boxY2 = ageY+data.ageBoxH
    data.box2X1 = data.boxX1 - data.boxDiff
    data.box2Y1 = data.boxY1 - data.boxDiff
    data.box2X2 = data.boxX2 + data.boxDiff
    data.box2Y2 = data.boxY2 + data.boxDiff
    data.cursorStartX = (data.boxX2 - data.boxX1)/2 + data.boxX1
    data.cursorStartY = data.boxY1 + 5
    if data.clickAge == True:
        canvas.create_rectangle(data.box2X1, data.box2Y1, data.box2X2, 
            data.box2Y2, fill = selCol, outline = "")
    canvas.create_rectangle(data.boxX1, data.boxY1, data.boxX2, data.boxY2,
                            fill = color, outline = "")
    
    if data.userInputAge != None:
        canvas.create_text(data.cursorStartX, data.cursorStartY+data.ageTextAdj, 
                            text = data.userInputAge)

def workoutRedrawAll(canvas, data):
    drawBackButton(canvas, data)
    descriptionFirstAdj = 50
    descrpAdju = 30
    if not data.remove:
        canvas.create_text(data.width//2, data.height//2-descriptionFirstAdj, 
            text = "We'll use your age to calculate a target targetHeartRate", 
            font = "verdana 18", fill = data.textGrey)
        canvas.create_text(data.width//2, data.height//2-descrpAdju, 
            text = "and match it to a song BPM", font = "verdana 18",
            fill = data.textGrey)
        canvas.create_text(data.width/2, data.height/2+data.ageAdjust,
                        text="Enter your age:", 
                        fill = "white", font="Helvetica 20")
    if not data.remove:
        drawTextBox(canvas, data)
    if data.remove:
        drawTextAndButtons(canvas, data)
        

####################################
# general funtions
####################################

def clickOn(x1, y1, x2, y2, eventX, eventY):
    return (x1<= eventX <= x2 and y1 <= eventY <= y2)

def drawBackButton(canvas, data):
    canvas.create_image(data.backX, data.backY, image=data.backImage)

def drawSkipNextButton(canvas, data):
    canvas.create_image(data.skipNextX, data.skipNextY, image = data.skipImage)

def drawSkipPrevButton(canvas, data):
    canvas.create_image(data.skipPrevX, data.skipPrevY, image = data.prevImage)

def skip(data, x, y):
    if clickOn(data.skipNextX - data.skipImageW//2, 
        data.skipNextY-data.skipImageW//2,
                data.skipNextX+data.skipImageW//2, 
                data.skipNextY+data.skipImageW//2, 
                x, y) and data.songPlaying:
        data.skipNext = True
    elif clickOn(data.skipPrevX - data.skipImageW//2, 
        data.skipPrevY-data.skipImageW//2,
                data.skipPrevX+data.skipImageW//2, 
                data.skipPrevY+data.skipImageW//2, 
                x, y):
        data.pressPrev = True
        data.skipNext = True

def goBack(data, x, y):
    if clickOn(data.backX - data.backImageW//2, data.backY-data.backImageW//2,
        data.backX+data.backImageW//2, data.backY+data.backImageW//2, x, y):
        if data.playlist != None:
            for song in data.playlist:
                song.is_playing = False
        init(data)
        data.playlist = None
        data.nextMode = None
        data.mode = "startScreen"

def playerMousePressed(event, data):
    goBack(data, event.x, event.y)
    skip(data, event.x, event.y)
    audioMousePressed(event, data)

def playerKeyPressed(event, data):
    pass

def playerTimerFired(data):
    audioTimerFired(data)

def playerRedrawAll(canvas, data):
    textX = 500
    textY = 40
    canvas.create_text(textX, textY, text = "lyrics (if the song has lyrics):",
        fill = data.textGrey)
    drawBackButton(canvas, data)  
    audioRedrawAll(canvas, data)
    drawSkipNextButton(canvas, data)
    drawSkipPrevButton(canvas, data)
    drawSongInfo(canvas, data)

####################################
# get desired BPM stats
####################################

def getTargetBPMs(data):
    data.maxHeartRate = 220 - int(data.actualAge)
    if data.level == "beginner":
        data.targetHeartRate = int(0.5 * data.maxHeartRate)
    elif data.level == "intermediate":
        data.targetHeartRate = int(0.7 * data.maxHeartRate)
    elif data.level == "experienced":
        data.targetHeartRate = int(0.9 * data.maxHeartRate)

####################################
# get BPM
####################################
def readWave(filename):
    wf = wave.open(filename,'rb')
    numOfWavSamples = wf.getnframes()
    samplingRate = wf.getframerate()
    samples = list(array.array('i',wf.readframes(numOfWavSamples)))
    return (samples, samplingRate)
    
# adapted from github user scaperot. I took what I needed from his code based on 
# what I read from the following 2 papers: 
# http://www.math.duke.edu/~ingrid/publications/cpam41-1988.pdf
# http://citeseerx.ist.psu.edu/viewdoc/downloadjsessionid=69A32C78593909A3B37B
# 0E18F1F22FA3?doi=10.1.1.63.5712&rep=rep1&type=pdf

def peakDetect(data):
    maxVal = numpy.amax(abs(data)) 
    peakIndex = numpy.where(data==maxVal)
    if len(peakIndex[0]) == 0: #if nothing found then the max must be negative
        peakIndex = numpy.where(data==-maxVal)
    return peakIndex

def applyFiltersAndTampering(data, samplingRate):
    cA, cD = [], [] # from pywt documentation
    cDSum = []
    coeffWavletFam = 4 # using the 4 coefficient wavelet family
    maxDecimation = 2**(coeffWavletFam-1)
    alphaVal = .99

    for level in range(coeffWavletFam):
        cD = []     
        if level == 0: # Perform DWT to analyze frequencies
            [cA,cD] = pywt.dwt(data,'db4') # from pywt documentation
            # db4 because we're using the 4 coefficient wavelet family
            cDMinLen = len(cD)/maxDecimation+1
            cDSum = numpy.zeros(cDMinLen)
        else:
            [cA,cD] = pywt.dwt(cA,'db4') # from pywt documentation
        # low pass filter from equation 3 in 2nd paper, using alpha value 0.99
        cD = signal.lfilter([1 - alphaVal], [1 - alphaVal], cD)
        # full wave rectification (equation 4 on 2nd paper)
        cD = abs(cD[::(2**(coeffWavletFam-level-1))])
        cD = cD - numpy.mean(cD)
        cDSum = cD[:cDMinLen] + cDSum
    cA = abs(signal.lfilter([1 - alphaVal], [1 - alphaVal], cA))
    cA = cA - numpy.mean(cA)
    cDSum = cA[:cDMinLen] + cDSum
    return cDSum


def bpmDetector(data, samplingRate):
    coeffWavletFam = 4 # using the 4 coefficient wavelet family
    maxDecimation = 2**(coeffWavletFam-1)

    autoCorrelation = []
    minIndex = 60/ 220 * (samplingRate/maxDecimation)
    maxIndex = 60/ 40 * (samplingRate/maxDecimation)
    alphaVal = .99
    
    cDSum = applyFiltersAndTampering(data, samplingRate)
    
    # autocorrelation function section

    autoCorrelation = numpy.correlate(cDSum,cDSum,'full') 
    midpoint = len(autoCorrelation) / 2
    correlationMidpt = autoCorrelation[midpoint:]
    peakIndex = peakDetect(correlationMidpt[minIndex : maxIndex])

    peakIndexAdjusted = peakIndex[0]+minIndex
    bpm = 60 / peakIndexAdjusted * (samplingRate//maxDecimation)
    return bpm,autoCorrelation

def bpm(filename):
    windowSizeScanned = 3
    samples, samplingRate = readWave(filename)
    # samples is a list of audio samples from the wav file
    # sampleingRate is the num of audio samples per sec
    sampleSubset = []
    correl=[]
    bpm = 0
    numOfWavSamples = len(samples) # total samples per file
    windowSamples = windowSizeScanned*samplingRate 
    currSample = 0 
    numOfWindows = numOfWavSamples // windowSamples
    bpms = numpy.zeros(numOfWindows) # more efficient than [0] * numOfWindows
    for window in range(1,numOfWindows):

        # go through all the samples of the song
        sampleSubset = samples[currSample : currSample+windowSamples]
        
        bpm, correl = bpmDetector(sampleSubset,samplingRate)
        bpms[window] = bpm # store the bpm from that window into the list bpms
 
        #iterate at the end of the loop
        currSample = currSample+windowSamples

    bpm = numpy.median(bpms)
    return bpm

####################################
# get data from audio files
####################################
def getPeakIndicesHelper(sampleSubset, samplingRate):
    data.peakInfo = []
    coeffWavletFam = 4 # using the 4 coefficient wavelet family
    maxDecimation = 2**(coeffWavletFam-1)

    autoCorrelation = []
    minIndex = 60/ 220 * (samplingRate/maxDecimation)
    maxIndex = 60/ 40 * (samplingRate/maxDecimation)
    alphaVal = .99
    
    cDSum = applyFiltersAndTampering(sampleSubset, samplingRate)
    
    # autocorrelation function section

    autoCorrelation = numpy.correlate(cDSum,cDSum,'full') 
    midpoint = len(autoCorrelation) / 2
    correlMidpointTmp = autoCorrelation[midpoint:]
    peakIndex = peakDetect(correlMidpointTmp[minIndex:maxIndex])

    peakIndexAdjusted = peakIndex[0]+minIndex
    data.peakInfo += ([int(peakIndexAdjusted)])
    return autoCorrelation

def getPeakIndices(filename):
    windowSizeScanned = 3
    samples, samplingRate = readWave(filename)
    # samples is a list of audio samples from the wav file
    # sampleingRate is the num of audio samples per sec
    sampleSubset = []
    correl=[]
    numOfWavSamples = len(samples) # total samples per file
    windowSamples = windowSizeScanned*samplingRate 
    currSample = 0 
    numOfWindows = numOfWavSamples // windowSamples
    for window in range(1,numOfWindows):
        # go through all the samples of the song
        sampleSubset = samples[currSample : currSample+windowSamples]   
        correl = getPeakIndicesHelper(sampleSubset,samplingRate)
        #iterate at the end of the loop
        currSample = currSample+windowSamples
    return data.peakInfo

def getStandardDeviation(filename):
    a = numpy.array(getPeakIndices(filename))
    return numpy.std(a)

def getSampleInfo(filename):
    samples,samplingRate = readWave(filename)
    return numpy.mean(samples)

####################################
# make playlist
####################################
def getAllSongs(path):
    if not os.path.isdir(path):
        return path
    else:
        songs = set()
        for child in os.listdir(path):
            if getAllSongs(path + "/" + child).endswith(".wav"):
                songs.add(getAllSongs(path + "/" + child))
        return songs

def makePlaylistWorkout(targetHeartRate):
    playlist = []
    allSongNames = getAllSongs("audiofiles")

    for song in allSongNames:
        if len(playlist) < data.playlistLen:
            if bpm(song) >= targetHeartRate:
                playlist.append(AudioFile(song))
        else:
            break
    if len(playlist) < data.playlistLen:
        data.notEnough = True
    return playlist

def makePlaylistStudy(data):
    playlist = []
    stdLimLower = 800
    stdLimUpper = 890
    allSongNames = getAllSongs("audiofiles")
    for song in allSongNames:
        if len(playlist) < data.playlistLen:
            if (stdLimLower <= getStandardDeviation(song) <= stdLimUpper and 
                getSampleInfo(song) < 0 and bpm(song) < 92):
                playlist.append(AudioFile(song))
        else:
            break
    if len(playlist) < data.playlistLen:
        data.notEnough = True
    return playlist

def makePlaylistSleep(data):
    playlist = []
    stdLimLower = 1290
    allSongNames = getAllSongs("audiofiles")
    for song in allSongNames:
        if len(playlist) < data.playlistLen:
            if (stdLimLower <= getStandardDeviation(song)):
                playlist.append(AudioFile(song))
        else:
            break
    if len(playlist) < data.playlistLen:
        data.notEnough = True
    return playlist

def makePlaylistRandom(data):
    playlist = []
    allSongNames = getAllSongs("audiofiles")
    for song in allSongNames:
        if len(playlist) < data.playlistLen: 
            playlist.append(AudioFile(song))
        else:
            break
    if len(playlist) < data.playlistLen:
        data.notEnough = True
    return playlist

def makePlaylistRock(data):
    playlist = []
    genreLower = 40000
    genreUpper = 72000
    allSongNames = getAllSongs("audiofiles")
    for song in allSongNames:
        if len(playlist) < data.playlistLen:
            if (genreLower <= getSampleInfo(song) <= genreUpper):
                playlist.append(AudioFile(song))
        else:
            break
    if len(playlist) < data.playlistLen:
        data.notEnough = True
    return playlist

def makePlaylistHype(data):
    playlist = []
    stdLimUpper = 1200
    genreLower = -2000000
    allSongNames = getAllSongs("audiofiles")
    for song in allSongNames:
        if len(playlist) < data.playlistLen:
            if (getStandardDeviation(song) <= stdLimUpper and
                genreLower <= getSampleInfo(song)):
                playlist.append(AudioFile(song))
        else:
            break
    if len(playlist) < data.playlistLen:
        data.notEnough = True
    return playlist

# def makePlaylistIinstrumental(data):
#     pass

####################################
# loading mode
####################################

def loadingMousePressed(event, data):
    pass

def loadingKeyPressed(event, data):
    pass

def loadingTimerFired(data):
    if data.getPlaylist:
        data.getPlaylist = False

    if data.nextMode == "sleep":
        data.playlist = makePlaylistSleep(data)
    elif data.nextMode == "study":
        data.playlist = makePlaylistStudy(data)
    elif data.nextMode == "random":
        data.playlist = makePlaylistRandom(data)
    elif data.nextMode == "rock":
        data.playlist = makePlaylistRock(data)
    elif data.nextMode == "hype":
        data.playlist = makePlaylistHype(data)
    elif data.nextMode == "workout":
        data.playlist = makePlaylistWorkout(data.targetHeartRate)

    if len(data.playlist) == 0 and data.notEnough:
        data.mode = "cannot make"
    if len(data.playlist) == data.playlistLen or data.notEnough:
        data.currSong = data.playlist[data.songCounter]
        if data.nextMode == "workout":
            data.mode = data.level
        elif (data.nextMode == "sleep" or data.nextMode == "study" 
            or data.nextMode == "random" or data.nextMode == "rock" or
                data.nextMode == "hype"):
            data.mode = data.nextMode

def loadingRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width,data.height,
        fill = data.backgroundColor)
    canvas.create_text(data.width//2, data.height//2, 
        text = "loading your %s playlist.." % data.nextMode, 
        font = "Verdana 24", fill = data.textGrey)

####################################
# sleep mode
####################################

def sleepRedrawAll(canvas, data):
    modeInfoX = data.width//4 + 20
    modeInfoY = 400
    modeInfoY2 = modeInfoY + 20

    playerRedrawAll(canvas, data)
    canvas.create_text(modeInfoX, modeInfoY, 
      text = "This playlist was generated based off song frequencies and BPM.")
    canvas.create_text(modeInfoX, modeInfoY2, 
        text = "It should yield songs that won't detract from your sleep.")
    

####################################
# study mode
####################################

def studyRedrawAll(canvas, data):
    modeInfoX = data.width//4 + 20
    modeInfoY = 400
    modeInfoY2 = modeInfoY + 20
    modeInfoY3 = modeInfoY + 40

    playerRedrawAll(canvas, data)
    canvas.create_text(modeInfoX, modeInfoY, 
        text = "This playlist was generated based off song frequencies. It")
    canvas.create_text(modeInfoX, modeInfoY2, 
        text = "should yield songs that won't detract from your studies but")
    canvas.create_text(modeInfoX, modeInfoY3, 
        text = "should not be so slow you fall asleep.")

####################################
# random mode
####################################

def randomRedrawAll(canvas, data):
    modeInfoX = data.width//4 + 20
    modeInfoY = 400
    modeInfoY2 = modeInfoY + 20

    playerRedrawAll(canvas, data)
    canvas.create_text(modeInfoX, modeInfoY, 
        text = "This is a randomly generated playlist based on the music")
    canvas.create_text(modeInfoX, modeInfoY2, 
        text = "in your library. There were no musical preferences.")

    
####################################
# rock mode
####################################

def rockRedrawAll(canvas, data):
    modeInfoX = data.width//4 + 20
    modeInfoY = 400
    modeInfoY2 = modeInfoY + 20

    playerRedrawAll(canvas, data)
    canvas.create_text(modeInfoX, modeInfoY, 
       text = "This is a playlist with entirely rock songs.")
    canvas.create_text(modeInfoX, modeInfoY2, 
        text = "Songs were chosen based on frequencies.")

####################################
# hype mode
####################################

def hypeRedrawAll(canvas, data):
    modeInfoX = data.width//4 + 20
    modeInfoY = 400
    modeInfoY2 = modeInfoY + 20

    playerRedrawAll(canvas, data)
    canvas.create_text(modeInfoX, modeInfoY, 
       text = "This playlist is filled with songs that will get you excited!")
    canvas.create_text(modeInfoX, modeInfoY2, 
        text = "Songs were chosen based on frequencies and BPM.")
    
####################################
# beginner mode
####################################

def beginnerRedrawAll(canvas, data):
    modeInfoX = data.width//4 + 20
    modeInfoY = 400
    modeInfoY2 = modeInfoY + 20
    modeInfoY3 = modeInfoY + 40

    playerRedrawAll(canvas, data)
    canvas.create_text(modeInfoX, modeInfoY, 
       text = "This is a playlist made to match your target heart rate.")
    canvas.create_text(modeInfoX, modeInfoY2, 
        text = "Songs were chosen based on their BPM. In the beginner level,")
    canvas.create_text(modeInfoX, modeInfoY3, 
        text = "exercise is less rigorous, so songs will have a slower BPM")

####################################
# intermediate mode
####################################
def intermediateRedrawAll(canvas, data):
    modeInfoX = data.width//4 + 20
    modeInfoY = 400
    modeInfoY2 = modeInfoY + 20
    modeInfoY3 = modeInfoY + 40
    modeInfoY4 = modeInfoY + 60

    playerRedrawAll(canvas, data)
    canvas.create_text(modeInfoX, modeInfoY, 
       text = "This is a playlist made to match your target heart rate.")
    canvas.create_text(modeInfoX, modeInfoY2, 
      text = "Songs were chosen based on their BPM. In the intermediate level,")
    canvas.create_text(modeInfoX, modeInfoY3, 
        text = "exercise is moderately rigorous, so songs will have a")
    canvas.create_text(modeInfoX, modeInfoY4, 
        text = "slightly faster BPM")


####################################
# experienced mode
####################################

def experiencedRedrawAll(canvas, data):
    modeInfoX = data.width//4 + 20
    modeInfoY = 400
    modeInfoY2 = modeInfoY + 20
    modeInfoY3 = modeInfoY + 40

    playerRedrawAll(canvas, data)
    canvas.create_text(modeInfoX, modeInfoY, 
       text = "This is a playlist made to match your target heart rate.")
    canvas.create_text(modeInfoX, modeInfoY2, 
      text = "Songs were chosen based on their BPM. In the experienced level,")
    canvas.create_text(modeInfoX, modeInfoY3, 
        text = "exercise is rigorous, so songs will have a much faster BPM.")

####################################
# finished mode
####################################

def finishedMousePressed(event, data):
    goBack(data, event.x, event.y)

def finishedKeyPressed(event, data):
    pass
    
def finishedTimerFired(data): 
    pass

def finishedRedrawAll(canvas, data):
    finishedHeightAdj = 40
    canvas.create_rectangle(0, 0, data.width,data.height,
        fill = data.backgroundColor)
    canvas.create_text(data.width/2, data.height/2-finishedHeightAdj,
                       text="Thanks for listening!", font="Arial 26 bold")
    drawBackButton(canvas, data)

####################################
# Audio class
####################################
class AudioFile(object):
    chunk = 1024

    def __init__(self, file):
        """ Init audio stream """ 
        self.name = file
        self.wf = wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
        ) # taken from documentation

        self.is_playing = False
        self.my_thread = None
        self.data = self.wf.readframes(AudioFile.chunk)
        self.songPlaying = False
        self.over = False
        self.lyrics = None

    def __repr__(self):
        return self.name

    def play(self):
        if self.lyrics == None:
            t = threading.Thread(target = getLyrics)
            t.start()               
        while self.data != '' and self.is_playing: 
            self.stream.start_stream()
            self.stream.write(self.data)
            self.data = self.wf.readframes(AudioFile.chunk)

        self.stream.stop_stream()
        if self.is_playing: 
            self.over = True
            self.stream.close()
            self.p.terminate()

    def press_button_play(self):
        if not self.is_playing:
            self.is_playing = True
            self.my_thread = threading.Thread(target=self.play)
            self.my_thread.start()

    def press_button_pause(self):
        self.is_playing = False

    def length(self):
        frames = (self.wf.getnframes())
        frameRate = self.wf.getframerate()
        time = (frames/frameRate)
        totalSeconds = int(round(time))
        return totalSeconds

def audioInit(data):
    data.playButtonX =  190
    data.playButtonY = 175
    data.playButtonR = 20
    data.playImageW = 84
    data.song = None
    data.playlist = None
    data.playImg = PhotoImage(file="playbutton.gif")
    data.pauseImg = PhotoImage(file="pausebutton.gif")
    data.songPlaying = False
    data.songCounter = 0
    data.currSong = None
    data.startTime = None
    data.skipNext = False
    data.playNextSong = True
    data.prev = 0
    data.justPaused = False
    data.getDiff = True
    data.currTime = 0
    data.pressPrev = False

def drawPlayButton(canvas, data):
    if data.songPlaying:
        buttonImage = data.pauseImg
    else:
        buttonImage = data.playImg
    canvas.create_image(data.playButtonX, data.playButtonY, image=buttonImage) 

def audioMousePressed(event, data):
    if clickOn(data.playButtonX - data.playImageW//2, 
                        data.playButtonY-data.playImageW//2, 
                        data.playButtonX+data.playImageW//2, 
                        data.playButtonY+data.playImageW//2, event.x, event.y):
        if not data.songPlaying: # no song is playing, want to play
            data.songPlaying = True
            data.currSong.press_button_play()
        else: # song is already playing, want to pause
            data.songPlaying = False
            data.justPaused = True
            data.currSong.press_button_pause()

def audioTimerFired(data):
    if data.currSong != None:
        if data.songPlaying == True:
            try: 
                if data.startTime == None:
                    data.startTime = data.currSong.stream.get_time()
                elif data.getDiff == True:
                    data.getDiff = False
                    data.diff = int(int(data.currSong.stream.get_time() - 
                                    data.startTime) - data.prev)
                data.currTime = int(data.currSong.stream.get_time() 
                                        - data.startTime) - data.diff
                data.prev = data.currTime
            except: 
                data.currTime = data.prev
        elif data.currSong.is_playing == False:
            #  keeps the progress bar there after pausing
            data.getDiff = True
            data.currTime = data.prev
        else:
            # when you start a new song
            data.currTime = 0
        nextSongTimerFired(data)
        if data.skipNext == True:
            data.currTime = 0
            data.skipNext = False
            data.currSong.wf.rewind()
            data.currSong.is_playing = False
            data.currSong.over = True
            nextSongTimerFired(data)
        
def nextSongTimerFired(data):
    if data.currSong.over == True:
        if data.songCounter < len(data.playlist) - 1:
            data.currTime = 0
            if data.pressPrev and data.songCounter != 0: 
                data.songCounter -= 1    
                data.pressPrev = False            
            else:
                data.songCounter += 1
            data.currSong.over = False
            data.currSong = data.playlist[data.songCounter]
            if data.playNextSong == True:
                data.startTime = None
                data.currSong.press_button_play()
        else:
            data.mode = "finished"

def getLength(data):
    totalSeconds = data.currSong.length()
    minutes = totalSeconds//60
    seconds = totalSeconds%60
    if seconds < 10:
        return ("%d:0%d" %(minutes, seconds))
    return ("%d:%d" %(minutes, seconds))

def drawTime(canvas, data):
    data.timeX = data.playButtonX
    data.timeY = data.playButtonY + 60
    secUpper = 59
    if data.currTime < 10:
        timeText = "0:0%d/%s" % (data.currTime, getLength(data))
    elif 10 <= data.currTime <= secUpper:
        timeText = "0:%d/%s" % (data.currTime, getLength(data))
    else:
        mins = data.currTime//60
        secs = data.currTime%60
        if secs < 10:
            timeText = "%d:0%d/%s" % (mins, secs, getLength(data))
        else:
            timeText = "%d:%d/%s" % (mins, secs, getLength(data))
    canvas.create_text(data.timeX, data.timeY, text = timeText, fill = "white",
                        font="Helvetica 20")

def drawTimeCircles(canvas, data):
    data.circleX = 80
    data.circleX2 = 290
    data.outerX = 90
    data.outerX2 = 280
    if not data.justPaused and not data.songPlaying:
        extendVal = 0
    else:
        extendVal = ((data.currTime+1)/data.currSong.length())*360
    canvas.create_oval(data.circleX , data.circleX , data.circleX2, 
                                data.circleX2, fill="white")
    canvas.create_arc(data.circleX, data.circleX, data.circleX2, data.circleX2, 
        extent=extendVal, fill = "blue")
    canvas.create_oval(data.outerX, data.outerX, data.outerX2, data.outerX2, 
        fill="black")

def audioRedrawAll(canvas, data):
    drawTimeCircles(canvas, data)
    drawPlayButton(canvas, data)
    drawTime(canvas, data)
    drawSongInfo(canvas, data)
    drawLyrics(canvas, data)

####################################
# getting song info
####################################
def getSongInfo(canvas, data):
    titleAndArtist = data.currSong.name.split("/")[-1].split(".wav")[0]
    title = titleAndArtist.split("~")[0].replace("-", " ")
    artist = titleAndArtist.split("~")[1].replace("-", " ")
    return (title, artist)

def drawSongInfo(canvas, data):
    data.songTitleX = data.width//4 + 20
    data.songTitleY = 350
    data.artistX = data.songTitleX
    data.artistY = data.songTitleY+20
    songTitle, artist = getSongInfo(canvas, data)
    canvas.create_text(data.songTitleX, data.songTitleY, 
        text = ("Currently playing: %s" % songTitle), 
        font = "verdana 16")
    canvas.create_text(data.artistX, data.artistY, 
        text = ("Artist: %s" % artist), 
        font = "verdana 16")

####################################
# lyrics
####################################
def getLyrics():
    windoeSize = 40
    song = data.currSong.name.split("/")[-1]
    song = song.replace("~", "-lyrics-")
    song = song.replace(".wav", ".html")
    song = "http://www.metrolyrics.com/" + song 

    driver = webdriver.Chrome()
    driver.set_window_size(windoeSize, windoeSize)
    driver.get(song)

    pageSource = driver.page_source

    soup = BeautifulSoup(pageSource, 'html.parser')
    lyrics = soup.find_all(id="lyrics-body-text")

    for child in lyrics:
        data.currSong.lyrics = child.get_text()

    driver.quit()

def drawLyrics(canvas, data):
    data.lyricsX = 550
    data.lyricsY = data.height//2 + 20
    canvas.create_text(data.lyricsX, data.height//2, 
        text = data.currSong.lyrics, font = "verdana 8", 
        fill = data.textGrey)


####################################
# use the run function as-is
####################################

def run(width=300, height=300):
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

    # create the root and the canvas
    global root
    root = Tk()
    # Set up data and call init
    class Struct(object): pass
    global data
    data = Struct()

    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    
    
    root.resizable(width=FALSE, height=FALSE)
    
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    
    init(data)
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    if data.playlist != None:
        for song in data.playlist:
            song.is_playing = False
    print("bye!")

run(700, 500)