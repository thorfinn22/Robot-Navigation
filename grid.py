class Grid:
    
    def __init__(self, pos, wall):
        self.pos = pos
        self.isWall = wall
        self.paths = []

   
    def getPos(self):
        return self.pos
 
    def getIsWall(self):
        return self.isWall
  
    def setIsWall(self, val):
        self.isWall = val
 
    def getPath(self):
        return self.paths

    def setPath(self, val):
        self.paths = val
