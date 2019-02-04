"""
This class handles, the graphics, rules, and controls for the core game.
the state of the bosrd is displayed here
"""

from tkinter import *
import tkinter.messagebox
from SquareShape import SquareShape
from Coor import Coor
from random import shuffle
import time
from Stuff import playSound
from PIL import ImageTk
from PIL import Image as PilImage

class MergeGame:

    SquareShape.squareSize = 20
    

    def __init__(self,startLevel,menuInst,totalLevels):
        self.menuInstance = menuInst
        self.level = startLevel
        self.totalLevels = totalLevels
        self.root = Tk()
        self.addMenu()
        self.root.configure(background=SquareShape.backgroundColor)
        self.canvas = Canvas(self.root)

        self.root.bind("<Right>", self.rightPressed)
        self.root.bind("<Left>", self.leftPressed)
        self.root.bind("<Up>", self.upPressed)
        self.root.bind("<Down>", self.downPressed)
        self.root.bind("<d>", self.rightPressed)
        self.root.bind("<a>", self.leftPressed)
        self.root.bind("<w>", self.upPressed)
        self.root.bind("<s>", self.downPressed)
        self.root.bind("<r>", self.restartLevel)
        self.root.bind("<m>", self.goToMainMenu)
        self.root.bind("<Button-1>", self.mouseClicked)
        self.canvas.pack()
    
        self.loadLevelNumber(self.level)
        self.root.mainloop()

    def addMenu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)#configure a menu for this software, and it is this menu   already puts the menu at the top

        subMenu = Menu(menu)#put submenu in main menu
        subMenu2 = Menu(menu)
        menu.add_cascade(label="File",menu=subMenu)#creates a file button with dropdown functionality using subMenu
        subMenu.add_command(label="Main Menu (M)",command=self.goToMainMenu)#add_command adds a "leaf" that does something when clicked, as opposed to showing another menu
        subMenu.add_command(label="Restart(R)",command=self.restartLevel)
        menu.add_cascade(label="Help",menu=subMenu2)
        subMenu2.add_command(label="Rules",command=self.rulesPopUp)
        subMenu2.add_command(label="Controls",command=self.controlsPopUp)
        

    def goToMainMenu(self,event=None):
        self.root.destroy()
        self.menuInstance.__init__()

    

    def rulesPopUp(self):
        tkinter.messagebox.showinfo('Rules','Move blocks of the same color to combine them\nGet every block of the same color together to win\n locked blocks can be unlocked by merging')

    def controlsPopUp(self):
        tkinter.messagebox.showinfo('Controls','Click on a shape to select it\nWASD or arrow keys to move selected block\nR to reset level\nM to go to menu')

    #if the selected shape can move, do so and check merge/win conditions
    def pushSelectedSquareShape(self,dx,dy):
        if(self.selected==None):
            return
        #play sounds
        if self.selected.canMove(dx,dy,self.squareShapeList,0,0,self.squaresInWidth-1,self.squaresInHeight-1):
            self.selected.move(dx,dy,self.canvas)
            if self.tryMergeWithOthersInList(self.selected,0,False):
                self.selected.select(self.canvas)#reselect shape to update outline
                playSound('sounds/merge.wav')

        if(self.meetsWinCondition()):
            self.levelTransition()#go to next level

    def rightPressed(self,event):
        self.pushSelectedSquareShape(1,0)
    def leftPressed(self,event):
        self.pushSelectedSquareShape(-1,0)
    def upPressed(self,event):
        self.pushSelectedSquareShape(0,-1)
    def downPressed(self,event):
        self.pushSelectedSquareShape(0,1)

    #select the shape the mouse is on
    def mouseClicked(self,event):
        oldSelected = self.selected
        self.selected = self.getSelected(event.x, event.y)
        if(oldSelected!=self.selected):
            if(oldSelected!=None):
                oldSelected.deselect(self.canvas)
            if(self.selected!=None):
                self.selected.select(self.canvas)

    def levelTransition(self):
        self.canvas.update_idletasks()#makes the canvas redraw
        playSound('sounds/Rupee.wav')
        time.sleep(1)
        self.nextLevel()


    #return true if it merged with something
    def tryMergeWithOthersInList(self,squareShape,searchStartIndex,keepXs):
        toReturn = False

        for shape in self.squareShapeList[searchStartIndex:]:#squareShapeList[searchStartIndex:] is a copy of squareShapeList
            if shape==squareShape:
                continue
            if squareShape.tryMerge(shape,keepXs,self.canvas):
                toReturn = True
                self.squareShapeList.remove(shape)
        return toReturn



    #returns the shape that is located at the given canvas coordinates
    #black blocks can't be selected
    #can return None if no shapes in here
    def getSelected(self,canvasX,canvasY):
        coor = Coor(canvasX//SquareShape.squareSize,canvasY//SquareShape.squareSize)
        for squareShape in self.squareShapeList:
            if(not(squareShape.color == "#000000") and not squareShape.locked and squareShape.containsCoor(coor)):
                return squareShape
        return None

    #each unique color must be in a single square shape
    def meetsWinCondition(self):
        colorSet = set()
        for squareShape in self.squareShapeList:
            if colorSet.__contains__(squareShape.color):
                return False
            elif not (squareShape.color == SquareShape.immovableColor):
                colorSet.add(squareShape.color)

        return True

    def nextLevel(self):
        self.level += 1
        if(self.level>self.totalLevels):
            self.goToMainMenu()
        else:
            self.loadLevelNumber(self.level)

    def restartLevel(self,event=None):
        self.loadLevelNumber(self.level)

    def loadLevelNumber(self,levelNumber):
        self.loadLevel('levels/level' + str(levelNumber) + '.csv')

    def loadLevel(self,fileName):
        self.canvas.delete(ALL)
        self.squareShapeList = []
        
        ##read file, first line contains row and column ammounts
        fileRead = open(fileName,'r')
        firstLine = fileRead.readline()
        firstLineList = firstLine.split(',')
        self.squaresInWidth = int(firstLineList[1])
        self.squaresInHeight = int(firstLineList[0])
        self.canvas.config(width=SquareShape.squareSize*self.squaresInWidth, height=SquareShape.squareSize*self.squaresInHeight)
        self.addBackground()

        #populate grid based on file data
        row=0
        for line in fileRead:
            lineList = line.split(',')
            column=0
            for cellString in lineList:
                cellString = cellString.strip()#get rid of possible new line
                cellList = cellString.split(' ')
                colorString = cellList[0]
                locked = (cellList[1]=="True")

                colorStringWithHashTag = '#' + colorString
                if(colorStringWithHashTag=='#FFFFFF'):#white = no block
                    pass
                else:
                    self.squareShapeList.append(SquareShape(Coor(column,row),colorStringWithHashTag,locked,self.canvas))
                column+=1
            row+=1

        self.selected = None
        fileRead.close()
        
        #squareShapeList.append(SquareShape(Coor(5,5),"red",canvas))
        self.initialMerge(0)

    def addBackground(self):
        myimage = PilImage.open('pictures/marble.jpg')
        myimage = myimage.resize((SquareShape.squareSize*self.squaresInWidth, SquareShape.squareSize*self.squaresInHeight))
        self.myimage = ImageTk.PhotoImage(myimage)
        self.canvas.create_image(0,0, anchor=NW, image=self.myimage)
        
    def initialMerge(self,startIndex):
        pass
        for index,squareShape in enumerate(self.squareShapeList[startIndex:]):
            if self.tryMergeWithOthersInList(squareShape,index,True):
                self.initialMerge(index+1)#tryMergeWithOthersInList already merged everything at index
                break







