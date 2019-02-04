"""
this class is the interface for the level select
the buttons are arranged in the grid and are created dynamically based on the
files in the levels folder
"""

from tkinter import *
from MergeGame import MergeGame
import os
from functools import partial

class MergeGameLevelSelect:

    levelNameList = None#singleton so levels only have to be checked once
    levelsInRow = 5

    def __init__(self,menuInst):
        self.root = Tk()
        self.backgroundColor = "#9999ff"
        self.menuInst = menuInst#menuInst is an instance of the main menu so it can call it
        self.root.bind("<m>", self.toMainMenu)
        masterFrame = Frame(self.root,width=600,height=450)
        masterFrame.config(bg=self.backgroundColor)

        #label Frame on top, button frame on bottom
        labelFrame = Frame(masterFrame,width=600,height=100)
        buttonFrame = Frame(masterFrame,width=600,height=350)
        labelFrame.config(bg=self.backgroundColor)
        buttonFrame.config(bg=self.backgroundColor)

        #menu button
        menuButton = Button(labelFrame,text="Menu",command=self.toMainMenu)
        menuButton.config(font=("Courier", 20))
        menuButton.pack(side=LEFT)

        #select level label
        titleLabel = Label(labelFrame,text="Select Level")
        titleLabel.config(font=("Courier", 44))
        titleLabel.config(bg=self.backgroundColor)
        titleLabel.pack(side=LEFT)

        self.addLevelButtons(buttonFrame)

        #add
        labelFrame.pack()
        buttonFrame.pack()
        masterFrame.pack()

        self.root.mainloop()#the window needs to be continuously on screen


    def addLevelButtons(self,buttonFrame):
        self.getLevelNameList()
        numLevels = len(self.levelNameList)
        for level in range(1,numLevels+1):
            button = Button(buttonFrame,text=str(level),command=partial(self.openLevel,level),width=10,height=5)
            button.grid(row=(level-1)//self.levelsInRow,column=(level-1)%self.levelsInRow,padx=3,pady=3)
            #partial creates a method with that specific value for level. that method is assigned to that button



    def openLevel(self,level):
        self.root.destroy()
        MergeGame(level,self.menuInst,len(self.levelNameList))

    #levelNameList is a singleton so levels only have to be checked once
    @classmethod
    def getLevelNameList(cls):
        if(cls.levelNameList==None):
            cls.createLevelNameList()
        return cls.levelNameList

    #level file names that are included are levels/level#.csv for #==1 to last uninterupted integer
    #(if you have levels 1-15 but are missing level 8, then only level 1-7 will be put in the list
    @classmethod
    def createLevelNameList(cls):
        cls.levelNameList = []
        levelNumber = 0

        while(True):
            levelNumber += 1
            filePath = "levels/level" + str(levelNumber) + ".csv"
            if os.path.exists(filePath):
                cls.levelNameList.append(filePath)
            else:
                break

    def toMainMenu(self,event=None):
        self.root.destroy()
        self.menuInst.__init__()
