"""
basic class for a coordinate object
may not be needed. can just use python tuples?
"""
class Coor:
    def __init__(self,x,y):    #constructor
        self.x = x
        self.y = y

    def getCopy(self):
        return Coor(self.x,self.y)


    def __eq__(self,otherCoor):
        return self.x == otherCoor.x and self.y == otherCoor.y


    def __str__(self):
        return "({},{})".format(self.x,self.y)

    def __hash__(self):
        return hash(self.x + 1000000*self.y)

    def move(self,dx,dy):
        self.x+=dx
        self.y+=dy

    def getMove(self,dx,dy):
        return Coor(self.x+dx,self.y+dy)
