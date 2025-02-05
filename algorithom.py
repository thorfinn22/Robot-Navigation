from draw import drawCompletePath, drawProcess
from grid import Grid
from point2D import Point2D
from map import Map
import random
import time
import math


def AnyBool(array, p):
    for x in array:
        if (x.getX() == p.getLocation().getPos().getX() and x.getY() == p.getLocation().getPos().getY()):
            return True
    return False


def AnyBoolPoint(array, p):
    for x in array:
        if (x.getX() == p.getX() and x.getY() == p.getY()):
            return True
    return False


def AnyVar(array, p):
    for x in array:
        if (x.getX() == p.getLocation().getPos().getX() and x.getY() == p.getLocation().getPos().getY()):
            return x


def matchGoal(p, goalList):
    for goal in goalList:
        if (p.getX() == goal.getX() and p.getY() == goal.getY()):
            return True
    return False

def calculateDistance(p1, p2):
    return math.sqrt(math.pow(p1.getX() - p2.getX(), 2) + math.pow(p1.getY()-p2.getY(), 2))


def minInArray(array):
    temp = array[0]
    for a in array:
        if (a < temp):
            temp = a
    return temp


def returnDis(e):
    return e.getDistanceToGoal()

def returnFScore(e):
    return e.getFScore()


def calculateH(p1, goalList):
    if (len(goalList) > 1):
        distanceArray = []
        for g in goalList:
            distanceArray.append(calculateDistance(p1, g))
        return minInArray(distanceArray)
    elif (len(goalList) == 1):
        return calculateDistance(p1, goalList[0])


def matchGoalVal(p, goalList):
    for goal in goalList:
        if (p.getX() == goal.getX() and p.getY() == goal.getY()):
            return goal


class algorithom:

    def __init__(self, initialState, goalState, map):
        self.pos = Point2D(initialState[0], initialState[1])
        self.goalPos = []
        self.robotMap = map
        for p in goalState:
            self.goalPos.append(Point2D(p[0], p[1]))

    def getPos(self):
        return self.pos

    def moveUp(self):
        return "up"

    def moveDown(self):
        return "down"

    def moveRight(self):
        return "right"

    def moveLeft(self):
        return "left"

    # create solution
    def createSolution(self, method, goal, nodes):
        solution = ""
        path = []
        action = []

        nodes.reverse()

        for p in nodes:
            for g in goal:
                if (p.getX() == g.getX() and p.getY() == g.getY()):
                    path.append(p)

            if (len(path) != 0):
                if (path[-1].getParentNode().getX() == p.getX() and path[-1].getParentNode().getY() == p.getY()):
                    path.append(p)

        path.reverse()

        for i in range(0, len(path)):
            if(i == len(path)-1):
                break

            if(path[i+1].getX() == path[i].getX() + 1):
                action.append(self.moveRight())

            if(path[i+1].getX() == path[i].getX() - 1):
                action.append(self.moveLeft())

            if(path[i+1].getY() == path[i].getY() + 1):
                action.append(self.moveDown())

            if(path[i+1].getY() == path[i].getY() - 1):
                action.append(self.moveUp())

        for a in action:
            solution = solution + a + "; "

        drawCompletePath(self.pos, self.goalPos,
                         self.robotMap.getWallList(), path, self.robotMap.getWidth(), self.robotMap.getLength())

        return "Method used: " + method + "\n" + "Visited: " + str(len(nodes)) + " nodes" + "\n" + "Path: " + solution


    def createSolutionExtend(self, goal, nodes):
        solution = ""
        path = []
        action = []

        nodes.reverse()

        for p in nodes:
            if (p.getX() == goal.getX() and p.getY() == goal.getY()):
                path.append(p)

            if (len(path) != 0):
                if (path[-1].getParentNode().getX() == p.getX() and path[-1].getParentNode().getY() == p.getY()):
                    path.append(p)

        path.reverse()

        for i in range(0, len(path)):
            if(i == len(path)-1):
                break

            if(path[i+1].getX() == path[i].getX() + 1):
                action.append(self.moveRight())

            if(path[i+1].getX() == path[i].getX() - 1):
                action.append(self.moveLeft())

            if(path[i+1].getY() == path[i].getY() + 1):
                action.append(self.moveDown())

            if(path[i+1].getY() == path[i].getY() - 1):
                action.append(self.moveUp())

        for a in action:
            solution = solution + a + "; "

        return len(nodes), solution

    # DFS
    def DfsSearch(self):
        if (matchGoal(self.pos, self.goalPos)):
            return "The goal point is the initial positition, no movement required"
        else:
            open = [] 
            visited = [] 

            open.insert(0, self.pos)

            while (len(open) != 0):
                currentNode = open.pop(0) 
                
                visited.append(currentNode)

                drawProcess(self.pos, self.goalPos,
                            self.robotMap.getWallList(), currentNode, self.robotMap.getWidth(), self.robotMap.getLength())
                time.sleep(0.2)

                for g in self.robotMap.getGrids():
                    if (currentNode.getX() == g.getPos().getX() and currentNode.getY() == g.getPos().getY()):
                        if(len(g.getPath()) != 0):
                            for p in g.getPath():
                                if (AnyBool(visited, p) == False and AnyBool(open, p) == False):
                                    p.getLocation().getPos().setParentNode(Point2D(currentNode))
                                    open.insert(0, p.getLocation().getPos())

                        # Found solution
                        if(matchGoal(currentNode, self.goalPos)):
                            return self.createSolution("DFS - Depth-First Search", self.goalPos, visited)

            return "No solution"

    # BFS
    def BfsSearch(self):
        if (matchGoal(self.pos, self.goalPos)):
            return "The goal point is the initial positition, no movement required"
        else:
            open = []  
            visited = []  
            open.insert(0, self.pos) 
            while (len(open) != 0):
                currentNode = open.pop()  
                visited.append(currentNode)

                drawProcess(self.pos, self.goalPos,
                            self.robotMap.getWallList(), currentNode, self.robotMap.getWidth(), self.robotMap.getLength())
                time.sleep(0.2)

                for g in self.robotMap.getGrids():
                    if (currentNode.getX() == g.getPos().getX() and currentNode.getY() == g.getPos().getY()):
                        if(len(g.getPath()) != 0):
                            for p in g.getPath():
                                if (AnyBool(visited, p) == False and AnyBool(open, p) == False):
                                    p.getLocation().getPos().setParentNode(Point2D(currentNode))
                                    open.insert(0, p.getLocation().getPos())

                        if(matchGoal(currentNode, self.goalPos)):
                            return self.createSolution("BFS - Breadth-First Search", self.goalPos, visited)

            return "No solution"

    #GBFS
    def GbfsSearch(self):
        if (matchGoal(self.pos, self.goalPos)):
            return "The goal point is the initial positition, no movement required"
        else:
            open = [] 
            visited = []  

            open.append(self.pos)

            while (len(open) != 0):

                open.sort(reverse=False, key=returnDis)

                currentNode = open.pop(0)
                visited.append(currentNode)

                drawProcess(self.pos, self.goalPos,
                            self.robotMap.getWallList(), currentNode, self.robotMap.getWidth(), self.robotMap.getLength())
                time.sleep(0.2)

                for g in self.robotMap.getGrids():
                    if (currentNode.getX() == g.getPos().getX() and currentNode.getY() == g.getPos().getY()):
                        if(len(g.getPath()) != 0):
                            for p in g.getPath():
                                if (visited.count(AnyVar(visited, p)) == 0):
                                    p.getLocation().getPos().setParentNode(Point2D(currentNode))
                                    p.getLocation().getPos().setDistanceToGoal(
                                        calculateH(p.getLocation().getPos(), self.goalPos))
                                    open.append(p.getLocation().getPos())

                        if(matchGoal(currentNode, self.goalPos)):
                            return self.createSolution("GBFS - Greedy Best First Search", self.goalPos, visited)

            return "No solution"

    # A* 
    def AStarSearch(self):
        if (matchGoal(self.pos, self.goalPos)):
            return "The goal point is the initial positition, no movement required"
        else:
            open = []  
            visited = [] 

            open.append(self.pos)

            self.pos.setGScore(0)  

            while (len(open) != 0):

                open.sort(reverse=False, key=returnFScore)

                currentNode = open.pop(0)
                visited.append(currentNode)

                drawProcess(self.pos, self.goalPos,
                            self.robotMap.getWallList(), currentNode, self.robotMap.getWidth(), self.robotMap.getLength())
                time.sleep(0.2)

                for g in self.robotMap.getGrids():
                    if (currentNode.getX() == g.getPos().getX() and currentNode.getY() == g.getPos().getY()):
                        if(len(g.getPath()) != 0):
                            for p in g.getPath():
                                if (AnyBool(visited, p) == False and AnyBool(open, p) == False):
                                    p.getLocation().getPos().setParentNode(Point2D(currentNode))
                                    p.getLocation().getPos().setGScore(currentNode.getGScore() + 1)
                                    p.getLocation().getPos().setFScore(p.getLocation().getPos().getGScore() +
                                                                       calculateH(p.getLocation().getPos(), self.goalPos))
                                    open.append(p.getLocation().getPos())

                        if(matchGoal(currentNode, self.goalPos)):
                            return self.createSolution("AS - A* Search", self.goalPos, visited)

            return "No solution"

    #CS1
    def UcsSearch(self):
        if (matchGoal(self.pos, self.goalPos)):
            return "The goal point is the initial positition, no movement required"
        else:
            open = []
            visited = []

            open.insert(0, self.pos)

            while (len(open) != 0):

            
                open.sort(reverse=True, key=returnDis)

                currentNode = open.pop()
                visited.append(currentNode)

                drawProcess(self.pos, self.goalPos,
                            self.robotMap.getWallList(), currentNode, self.robotMap.getWidth(), self.robotMap.getLength())
                time.sleep(0.2)

                for g in self.robotMap.getGrids():
                    if (currentNode.getX() == g.getPos().getX() and currentNode.getY() == g.getPos().getY()):
                        if(len(g.getPath()) != 0):
                            for p in g.getPath():
                                if (AnyBool(visited, p) == False and AnyBool(open, p) == False):
                                    p.getLocation().getPos().setParentNode(Point2D(currentNode))
                                    p.getLocation().getPos().setDistanceToGoal(
                                        currentNode.getDistanceToGoal() + random.randint(1, 5))
                                    open.insert(0, p.getLocation().getPos())

                        if(matchGoal(currentNode, self.goalPos)):
                            return self.createSolution("CUS1 - Uniform Cost Search" + "\nThe cost between two points is a random number in the range 1-5. So the result will be different every time the program run" + "\nIf the cost is the same the result will be the same as BFS", self.goalPos, visited)

            return "No solution"

    #CS2
    def IdasSearch(self):
        if (matchGoal(self.pos, self.goalPos)):
            return "The goal point is the initial positition, no movement required"
        
        else:
            open = []  
            visited = [] 

            open.append(self.pos)
            bound = calculateH(self.pos, self.goalPos)

            self.pos.setGScore(0)  # g(n)

            while (len(open) != 0):

             
                open.sort(reverse=False, key=returnFScore)

                currentNode = open.pop(0)
                visited.append(currentNode)

                drawProcess(self.pos, self.goalPos,
                            self.robotMap.getWallList(), currentNode, self.robotMap.getWidth(), self.robotMap.getLength())
                time.sleep(0.2)

                for g in self.robotMap.getGrids():
                    if (currentNode.getX() == g.getPos().getX() and currentNode.getY() == g.getPos().getY()):
                        if(len(g.getPath()) != 0):
                            for p in g.getPath():
                                if (AnyBool(visited, p) == False and AnyBool(open, p) == False):
                                    if (calculateH(p.getLocation().getPos(), self.goalPos) < bound):
                                        p.getLocation().getPos().setParentNode(Point2D(currentNode))
                                        p.getLocation().getPos().setGScore(currentNode.getGScore() + 1)
                                        p.getLocation().getPos().setFScore(p.getLocation().getPos().getGScore() +
                                                                           calculateH(p.getLocation().getPos(), self.goalPos))
                                        open.append(p.getLocation().getPos())
                                        bound = p.getLocation().getPos().getFScore()

                        if(matchGoal(currentNode, self.goalPos)):
                            return self.createSolution("CUS2 - Iterative Deepening A*", self.goalPos, visited)

            return "No solution"
     #CUS3
    def AStarSearchExtend(self):
        open = []  
        visited = [] 

        open.append(self.pos)

        self.pos.setGScore(0)

        while (len(open) != 0):
            # sort by f(n), ascending order
            open.sort(reverse=False, key=returnFScore)

            currentNode = open.pop(0)
            visited.append(currentNode)
            drawProcess(self.pos, self.goalPos,
                        self.robotMap.getWallList(), currentNode, self.robotMap.getWidth(), self.robotMap.getLength())
            time.sleep(0.2)

            for g in self.robotMap.getGrids():
                if (currentNode.getX() == g.getPos().getX() and currentNode.getY() == g.getPos().getY()):
                    if(len(g.getPath()) != 0):
                        for p in g.getPath():
                            if (AnyBool(visited, p) == False and AnyBool(open, p) == False):
                                p.getLocation().getPos().setParentNode(Point2D(currentNode))
                                p.getLocation().getPos().setGScore(currentNode.getGScore() + 1)
                                p.getLocation().getPos().setFScore(p.getLocation().getPos().getGScore() +
                                                                   calculateH(p.getLocation().getPos(), self.goalPos))
                                open.append(p.getLocation().getPos())
                    if(matchGoal(currentNode, self.goalPos)):
                        return self.createSolutionExtend(matchGoalVal(currentNode, self.goalPos), visited), matchGoalVal(currentNode, self.goalPos)

    
    def VisitAllGoalShortest(self):
        solution = "Method: Research - VisitAllGoalShortest\n"
        result = 0

        tempVar = len(self.goalPos)

        for i in range(0, tempVar):
            r, goal = self.AStarSearchExtend()
            if (i == 0):
                solution = solution + "Start point to Goal " + \
                    str(i+1) + ": " + r[1] + "\n"
            else:
                solution = solution + "Goal " + \
                    str(i) + " to Goal " + str(i+1) + ": " + r[1] + "\n"
            result = result + r[0]
            if (len(self.goalPos) != 0):
                self.goalPos.remove(goal)
                self.pos = goal

        return solution + "Visited: " + str(result) + " nodes"


