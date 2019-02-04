"""
this is the class for the squares in the game
square shapes start off with a single square which can be locked or unlocked
locked means merge game won't select them
merging unlocks them, except for when MergeGame initally merges shapes that are already together after loading the level
contains two dictionaries (hash maps) of coordinates to canvas objects. When one is changed, the other map changes too
one map to square objects and the other map to lock pictures if the shape is locked
"""

from Coor import Coor
from PIL import ImageTk
from PIL import Image as PilImage
from tkinter import * #for NW?



class SquareShape:
    squareSize = 1 #default
    backgroundColor = '#dddddd'
    selectedColor = '#000000'
    immovableColor = '#000000'
    lockPhotoImg = None#this reference must be remembered after it is set or the images will be garbage collected

    def __init__(self,startCoor,color,locked,canvas):    #constructor
        self.coorRectMap = {}
        self.coorXMap = {}
        self.color = color
        self.locked = locked
        self.addCoor(startCoor,canvas)

        
    def addCoor(self,coor,canvas):
        self.coorRectMap[coor] = canvas.create_rectangle(coor.x * self.squareSize,coor.y * self.squareSize, (coor.x+1) * self.squareSize, (coor.y+1) * self.squareSize, fill=self.color,outline=self.backgroundColor)
        if(self.locked):
            self.coorXMap[coor] = self.createCanvasImage(canvas,coor.x * self.squareSize,coor.y * self.squareSize)
    

    def deleteCoor(self,coor):
        canvas.delete(coorRectMap.pop(coor))
        canvas.delete(coorXMap.pop(coor))

    def deleteShape(self,shape):
        pass

    def containsCoor(self,coor):
        return self.coorRectMap.__contains__(coor)

    def isColliding(self,shape):
        return isColliding(self,shape,0,0)

    #shapes are colliding if they share at least 1 of the same coordinate
    def isColliding(self,otherShape,dx,dy):
        newCoords = set()
        for key in self.coorRectMap.keys():
            newCoords.add(key.getMove(dx,dy))
        otherShapeCoorsSet = otherShape.getCoorSet()
        return len(set.intersection(newCoords,otherShapeCoorsSet))>0

    #returns a set of all coordinates that are touching the shape
    def getAdjacentSet(self):
        adjacentSet = set()
        for coor in self.coorRectMap.keys():
            adjacentSet.add(coor.getMove(0,1))
            adjacentSet.add(coor.getMove(0,-1))
            adjacentSet.add(coor.getMove(1,0))
            adjacentSet.add(coor.getMove(-1,0))
        return adjacentSet

    #uses the keys in coorRectMap only, though the other map should have the same keys if the shape is locked
    def getCoorSet(self):
        coorSet = set()
        for coor in self.coorRectMap.keys():
            coorSet.add(coor.getCopy())
        return coorSet

    #tests if the shape is touching another shape
    def isAdjacent(self,otherShape):
        adjacentSet = self.getAdjacentSet()
        otherShapeSet = otherShape.getCoorSet()
        return len(set.intersection(adjacentSet,otherShapeSet))>0

    #tests if a shape can merge. If it can, do so and return True
    def tryMerge(self,otherShape,keepXs,canvas):
        if(self.isAdjacent(otherShape) and self.color==otherShape.color):
            self.merge(otherShape,keepXs,canvas)
            return True
        return False

#this was problem   canvas was garbage collecting it because I called this method instead of creating direcly???
    #returns the image for the canvas map to store
    def createCanvasImage(self,canvas,x,y):
        image = canvas.create_image(x,y, anchor=NW, image=self.getPhotoImage())
        return image

    
    def getPhotoImage(self):
        if self.lockPhotoImg == None:
            image = PilImage.open('pictures/lock.png')
            image = image.resize((self.squareSize,self.squareSize))
            self.lockPhotoImg = ImageTk.PhotoImage(image)
        return self.lockPhotoImg
        
    #steal the other shapes's stuff. MergeGame deletes the other shape from its list
    def merge(self,otherShape,keepXs,canvas):
        
        if keepXs:#for initial merge
            if self.locked:#it already has x's for all its coords
                if otherShape.locked:
                    self.coorXMap.update(otherShape.coorXMap)#steal other x's
                else:#make x's for the other shape
                    coorSet = otherShape.getCoorSet()
                    for coor in coorSet:
                        self.coorXMap[coor] = self.createCanvasImage(canvas,coor.x * self.squareSize,coor.y * self.squareSize)
            else:# self is unlocked
                if otherShape.locked:
                    self.locked = True
                    #add x's to all its shapes and steal otherShape's x's
                    self.coorXMap.update(otherShape.coorXMap)#steal other x's
                    #add x's to all its shapes
                    coorSet = self.getCoorSet()
                    for coor in coorSet:
                        self.coorXMap[coor] = self.createCanvasImage(canvas,coor.x * self.squareSize,coor.y * self.squareSize)
                else:#neither are locked
                    pass


        else:#for when player merges
            if self.locked:#delete its own x's
                self.locked = False
                coorSet = self.getCoorSet()
                for coor in coorSet:
                    canvas.delete(self.coorXMap[coor])
            if otherShape.locked:#delete other shape's x's
                coorSet = otherShape.getCoorSet()
                for coor in coorSet:
                    canvas.delete(otherShape.coorXMap[coor])

            self.coorXMap = {}
        #steal other shape's squares
        self.coorRectMap.update(otherShape.coorRectMap)

    def inBounds(self,xMin,yMin,xMax,yMax):
        pass

    def getCanvasSquares(self,squareSize):
        pass

    def squareSizeChanged(self,newSize):
        pass

    #tests if there is anything preventing the shape from moving (level bounds or other blocks)
    def canMove(self,dx,dy,squareShapeList,lowestX,lowestY,highestX,highestY):
        return (not self.wouldBeOutOfBounds(dx,dy,lowestX,lowestY,highestX,highestY) and not self.wouldIntersectOtherShape(dx,dy,squareShapeList))

    #tests if any part of the shape, if moved by dx,dy, would be out outside of the given bounds
    def wouldBeOutOfBounds(self,dx,dy,lowestX,lowestY,highestX,highestY):
        if self.getLowestX()+dx<lowestX:
            return True
        if self.getLowestY()+dy<lowestY:
            return True
        if self.getHighestX()+dx>highestX:
            return True
        if self.getHighestY()+dy>highestY:
            return True
        return False

    def getLowestX(self):
        lowestX = float("inf")
        for key in self.coorRectMap.keys():
            if key.x<lowestX:
                lowestX=key.x
        return lowestX

    def getLowestY(self):
        lowestY = float("inf")
        for key in self.coorRectMap.keys():
            if key.y<lowestY:
                lowestY=key.y
        return lowestY

    def getHighestX(self):
        highestX = float("-inf")
        for key in self.coorRectMap.keys():
            if key.x>highestX:
                highestX=key.x
        return highestX

    def getHighestY(self):
        highestY = float("-inf")
        for key in self.coorRectMap.keys():
            if key.y>highestY:
                highestY=key.y
        return highestY

    def wouldIntersectOtherShape(self,dx,dy,squareShapeList):
        for otherShape in squareShapeList:
            if otherShape==self:
                continue
            if self.isColliding(otherShape,dx,dy):
                return True
        return False

    #updates the positions of each coordinate and their respective placements on the canvas
    def move(self,dx,dy,canvas):
        newMap = {}
        for coor, rect in self.coorRectMap.items():
            coorX = coor.x + dx
            coorY = coor.y + dy
            canvasX = coorX*self.squareSize
            canvasY = coorY*self.squareSize
            canvas.coords(rect,(canvasX,canvasY,canvasX+self.squareSize,canvasY+self.squareSize))
            newMap[Coor(coorX,coorY)] = rect
        newXMap = {}
        for coor, x in self.coorXMap.items():
            coorX = coor.x + dx
            coorY = coor.y + dy
            canvasX = coorX*self.squareSize
            canvasY = coorY*self.squareSize
            canvas.coords(x,(canvasX,canvasY,canvasX+self.squareSize,canvasY+self.squareSize))
            newXMap[Coor(coorX,coorY)] = x

        self.coorRectMap = newMap
        self.coorXMap = newXMap


    def moveUp(self,canvas):
        self.move(0,-1,canvas)

    def moveDown(self,canvas):
        self.move(0,1,canvas)

    def moveRight(self,canvas):
        self.move(1,0,canvas)

    def moveLeft(self,canvas):
        self.move(-1,0,canvas)


    def select(self,canvas):
        for key in self.coorRectMap.keys():
            rect = self.coorRectMap[key]
            canvas.itemconfig(rect,outline=self.selectedColor)#adds outline to all blocks

    def deselect(self,canvas):
        for key in self.coorRectMap.keys():
            rect = self.coorRectMap[key]
            canvas.itemconfig(rect,outline=self.backgroundColor)#removes outline



    def __str__(self):
        return self.squaresString() + " Color: " + self.color + " Locked: " + str(self.locked)

    def squaresString(self):
        ans = ""
        for coor in self.coorRectMap.keys():
            ans = ans + " " + str(coor)

        return ans



