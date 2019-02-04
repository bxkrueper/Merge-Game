"""
MergeGameMainMenu class
start point of the program. displays the main menu with buttons to start from level 1
or go to level select
"""
from tkinter import *
from MergeGame import MergeGame
from MergeGameLevelSelect import MergeGameLevelSelect

class MergeGameMainMenu:

    def __init__(self):
        self.root = Tk()
        self.backgroundColor = "#9999ff"
        masterFrame = Frame(self.root,width=600,height=450)
        masterFrame.config(bg=self.backgroundColor)

        masterFrame.pack_propagate(0)# disable resizing if not large enough to hold all the child widgets.

        #make inner frames (label frame on top, button frame on bottom)
        labelFrame = Frame(masterFrame,width=600,height=150)
        buttonFrame = Frame(masterFrame,width=600,height=300)
        labelFrame.pack_propagate(0)
        buttonFrame.pack_propagate(0)
        labelFrame.config(bg=self.backgroundColor)
        buttonFrame.config(bg=self.backgroundColor)

        #make title
        titleLabel = Label(labelFrame,text="Merge Game")
        titleLabel.config( height = 50, width = 100 )
        titleLabel.config(font=("Courier", 44))
        titleLabel.config(bg=self.backgroundColor)
        titleLabel.pack()

        #make buttons
        startButton = Button(buttonFrame,text="Start",command=self.start)
        startButton.config(font=("Courier", 20))
        startButton.pack(side=LEFT, padx=60)
        pickLevelButton = Button(buttonFrame,text="Pick Level",command=self.pickLevel)
        pickLevelButton.config(font=("Courier", 20))
        pickLevelButton.pack(side=RIGHT, padx=60)

        #add to frames
        labelFrame.pack()
        buttonFrame.pack()

        masterFrame.pack()

        self.root.mainloop()#to keep the window from closing right away

    def start(self):
        self.root.destroy()#destroy this window because another window is comming
        levelList = MergeGameLevelSelect.getLevelNameList()
        MergeGame(1,self,len(levelList))#start game at level 1

    def pickLevel(self):
        self.root.destroy()#destroy this window because another window is comming
        MergeGameLevelSelect(self)#load level select window

MergeGameMainMenu()#starts the game by creating an instance of MergeGameMainMenu

