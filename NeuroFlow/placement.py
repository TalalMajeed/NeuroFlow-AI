# This is the complete code albeit it still needs to be tested for the case when the box comes out of the blue

# This will be the grid that will contain the boxes
class Container:
    def __init__(self, boxes, connections, reversedConnections = []):
        self.boxes = boxes
        self.connections = connections
        for box in boxes:
            box.setContainer(self)
        self.numberOfBoxes = len(boxes)
        self.reversedConnections = reversedConnections
        self.startingX = 200
        self.startingY = 200
        self.standardIncrement = 600
        self.xpad = 120
        self.ypad = 120
        self.padValue = 60

    def getBoxes(self):
        return self.boxes
    
    def getConnections(self):
        return self.connections
    
    # Lets get all the copied boxes, we will pass them into the constructor in order to get the copied boxes
    def getCopiedBoxesAndConnections(self,container):
        # We will get all the copied boxes
        copiedBoxes = []
        for box in self.boxes:
            copiedBoxes.append(box.createClone(container))       
        copiedConnections = []

        # Lets now also get all the connections
        for connection in self.connections:
            # We will create the clone of the copiedConnections, but with the copied boxes as objects
            copiedConnections.append(connection.createClone(copiedBoxes))
        return copiedBoxes,copiedConnections

    # This will be the method that will be used to determine the reverse connections for a particular box
    def determineReverseConnections(self, container):
        # First of all we will get the copied boxes
        boxCopy,connectionCopy = self.getCopiedBoxesAndConnections(container)

        # Lets give the container the box copy
        container.boxes = boxCopy

        # And lets give the container the connections copy
        container.connections = connectionCopy

        # Now lets allocate the connections to the copied boxes
        container.allocateConnections()

        # We will set the coordinates of that box which is equal to the box that we are trying to find the reverse connections for
        for copiedBox in boxCopy:
            # If the box has not been placed we will set the coordinates of the box
            if copiedBox.hasPlaced == False:
                copiedBox.setCoordinates(0,0)
                copiedBox.confirmPlacement()
                copiedBox.testTargetCoordinates()
    
    def setBoxes(self):
        # We will allocate the connections to all the boxes
        self.allocateConnections()

        # We will now place the box on an instantiated grid, this grid will keep track of the container
        tempGrid = Container([],[])

        # We will now find out the reverse connections, first we pass the grid into the determineReverseConnections method
        self.determineReverseConnections(tempGrid)

        # We will find out all those boxes, that are the sources but do not originate from anywhere, and will set the coordinates of them beforehand
        destinationBoxes = []
        sourceBoxes = []

        # Destination boxes will here be considered as those boxes that have no reverse connections
        # So we will iterate over the connections of the non-reverse boxes
        for connection in self.connections:
            isReverse = False
            for reverseConnection in tempGrid.reversedConnections:
                if (Connection.compareConnections(connection,reverseConnection) == True):
                    # If it is one of the reverse connections we will not add it to the destination boxes
                    isReverse = True
                    self.reversedConnections.append(connection)
                    break
            # In case the connection in not reverse we will append it to the target boxes
            if isReverse == False:
                destinationBoxes.append(connection.target)

        # This will store the number of source boxes to initialize their position
        sourceBoxNumber = 0

        # Now we will loop through all the boxes and find out the boxes that are the sources, and we will set their coordinates
        for box in self.boxes:
            if box not in destinationBoxes:
                sourceBoxes.append(box)
                box.setCoordinates(self.startingX ,self.startingY + self.standardIncrement * sourceBoxNumber)
                box.confirmPlacement()
                box.setTargetCoordinates()
                # We will append this node to the list of nodes
                sourceBoxNumber += 1

        # Now we will find out the last boxes
        self.determineLastBoxes()

        # After doing this we will cause a shift in the boxes, effectively distorting them, in a systematic way
        self.distortBoxes()

        # This will resolve any overlap that will be caused after this distortion
        self.resolveOverlaps()
        
        # If we find out that the set of all the encompassed boxes by all the current nodes is the same as the set of all the boxes, it means we have found out all the nodes
        # This will be the set of boxes encompassed by all the current nodes
        self.scaleBackToWindow()
        
        # If we do not get the same value we will find all the nodes from the given set of destination boxes


    # This will be where we will check whether a particular box overlaps with another box
    def checkBoxOverlap(self, box, padValue):
        for otherBox in self.boxes:
            if otherBox.hasPlaced == True:
                if box.checkOverlap(otherBox,padValue) != 0:
                    return box.checkOverlap(otherBox,padValue)
        return 0
    
    # This will be the function that will determine the boxes that are at last
    def determineLastBoxes(self):
        for box in self.boxes:
            isLast = True
            for connection in box.connections:
                if connection not in self.reversedConnections:
                    if Box.compareBoxes(box,connection.source) == True:
                        isLast = False
            # If the box is still not found in the source of another box it means that it is the last box
            if isLast == True:
                box.isLast = True

    
    # This will be the method that will allocate the connections to the boxes
    def allocateConnections(self):
        for connection in self.connections:
            connection.source.setConnection(connection)

    # This will be the function that will distort the placement of the boxes in a systematic way
    def distortBoxes(self):
        # Dictionary to store boxes with same x-coordinate
        sameXBoxes = {}
        sameYBoxes = {}

        # Iterate over the boxes
        for box in self.boxes:
            if (box.hasPlaced == True):
                # If it is a new x value, create a new list for that x-coordinate
                if box.x not in sameXBoxes:
                    sameXBoxes[box.x] = []
                # Append the box to the list corresponding to its x-coordinate
                sameXBoxes[box.x].append(box)
                # If it is a new y value, create a new list for the y-coordinate
                if box.y not in sameYBoxes:
                    sameYBoxes[box.y] = []
                # Append the box to the list corresponding to its y-coordinate
                sameYBoxes[box.y].append(box)

        # Sort the boxes in the same x-coordinate
        self.sortBoxes(sameXBoxes,"y")

        # Sort the boxes in the same y-coordinate
        self.sortBoxes(sameYBoxes,"x")

        # Shift the boxes in the same x-coordinate, by some y coordinate
        self.shiftBoxes(sameXBoxes,"x")

        # Shift the boxes in the same y-coordinate
        self.shiftBoxes(sameYBoxes,"y")
    
    # We will sort the boxes in the same x-coordinate, based on the yCoordinate
    def sortBoxes(self,boxes,coordinate):
        if (coordinate == "x"):
            for key in boxes:
                boxes[key].sort(key = lambda x: x.x)
        elif (coordinate == "y"):
            for key in boxes:
                boxes[key].sort(key = lambda x: x.y)

    # This will now loop over the arranged boxes, and will increment or decrement their coordinates by the padding value
    def shiftBoxes(self,boxes,coordinate):
        for key in boxes:
            # This will be the list of the boxes, with the same coordinates that have been already sorted
            sameBoxes = boxes[key]
            for counter,sameBox in enumerate(sameBoxes):
                if (counter % 2 == 0):
                    if (coordinate == "y"):
                        sameBox.shiftY(self.padValue)
                    elif (coordinate == "x"):
                        sameBox.shiftX(self.padValue)
                else:
                    if (coordinate == "y"):
                        sameBox.shiftY(-1 * self.padValue)
                    elif (coordinate == "x"):
                        sameBox.shiftX(-1 * self.padValue)

    # This will get the most negative value of y, and then will add the absolute value of that to all the y coordinates
    def scaleBackToWindow(self):
        mostNegativeValue = 0
        for box in self.boxes:
            if box.y < mostNegativeValue:
                mostNegativeValue = box.y
        for box in self.boxes:
            box.shiftY(abs(mostNegativeValue))
    
    # This will be the method that will resolve any overlap in the end
    def resolveOverlaps(self):
        # This will check whether there is any overlap or not
        isNoOverLapDetected = False

        # While any overlap 
        while(isNoOverLapDetected == False):
            # Now in this loop I will make it true, we want to see that when there is an overlap, we will make it false
            isNoOverLapDetected = True
            # We will iterate over all the boxes
            for box in self.boxes:
                # If the box has aleady been placed, we will check for the overlap
                if (box.hasPlaced == True):
                    # If there is an overlap we will shift the box, in accordance to the overlap detected
                    # I have set a padding of 20 in this case
                    isOverlapDetected = self.checkBoxOverlap(box,20)
                    if isOverlapDetected != 0:
                        # Now that there is an overlap, we can make it false
                        isNoOverLapDetected = False

                        # We will check for the different kinds of overlaps in any case
                        # In case of an upper overlap
                        if isOverlapDetected == 1:
                            box.shiftY(-1 * self.padValue)
                        # In case of an lower overlap
                        elif isOverlapDetected == 2:
                            box.shiftY(self.padValue)
                        # In case of an right overlap
                        elif isOverlapDetected == 4:
                            box.shiftX(self.padValue)
                        # I have not done the left overlap, as it will require decrementing the values, that can lead to negative values for the boxes
                                                
            
# This will be the class that will be used to represent the boxes
class Box:
    def __init__(self, name, width, height, x = None, y = None,container = None,adjacentBoxes = []):
        self.name = name
        self.width = width
        self.height = height
        self.connections = []
        self.x = x
        self.y = y
        self.hasPlaced = False
        self.container = container
        self.isLast = False
        self.isRightIn = False
        self.isRightOut = False
        self.isLeftIn = False
        self.isLeftOut = False
        self.isTopIn = False
        self.isTopOut = False
        self.isBottomIn = False
        self.isBottomOut = False
    
    def setConnection(self, connection):
        self.connections.append(connection)

    # We will set the container of the box to the current container
    def setContainer(self, container):
        self.container = container


    # This will be the function that will get the padded box
    def getPaddedCoordinates(width,height,padding):
        return width + padding,height + padding

    # This will be used to check for the overlap of the boxes, and we will also check out the type of the overlap
    def checkOverlap(self,box2,paddingValue):
        # If it is a overlap in which the self box is above box2, we will return 1
        # If it is a overlap in which the self box is below box2, we will return 2
        # If it is a overlap in which the self box is to the left of box2, we will return 3
        # If it is a overlap in which the self box is to the right of box2, we will return 4
        # If there is no overlap we will return 0 
        box2NewWidth,box2NewHeight = Box.getPaddedCoordinates(self.width,self.height,paddingValue)
        box1NewWidth,box1NewHeight = Box.getPaddedCoordinates(box2.width,box2.height,paddingValue)
        # This can only be done if the two boxes have been placed
        if (box2.hasPlaced == False or self.hasPlaced == False):
            return 0
        
        # We want to check whether the passed in box is the same as the box that we are checking for overlap
        if self == box2:
            return 0
        
        # If we are into this loop we will check for the overlap, and if it is detected we will return the type of overlap, for further processing
        if self.x < box2.x + box2NewWidth and self.x + box1NewWidth > box2.x and self.y < box2.y + box2NewHeight and self.y + box1NewHeight > box2.y:
            return Box.checkOverlapType(Box("temp",box2NewWidth,box2NewHeight,self.x,self.y),Box("temp2",box1NewWidth,box1NewHeight,box2.x,box2.y))
        return 0
    
    # This function will check for the overlap type
    def checkOverlapType(box1,box2):
        # This will be the condition for a upper overlap
        if box1.y < box2.y:
            return 1
        
        # This will be the condition for a lower overlap
        if box1.y > box2.y:
            return 2
        
        # This will be the condition for a right overlap
        if box1.x > box2.x:
            return 4
        
        # This will be the condition for a left overlap
        if box1.x < box2.x:
            return 3


    # This will set up the coordinates of the box, but only when we are sure that we have placed the box in the correct position
    def setCoordinates(self, x, y):
        if (self.hasPlaced == False):
            self.x = x
            self.y = y

    # This will be the function that will shift the x coordinates, by a given value of the boxes
    def shiftX(self,xIncrement):
        self.x += xIncrement

    # This will be the function that will shift the y coordinates, by a given value
    def shiftY(self,yIncrement):
        self.y += yIncrement
    
    # This will be the method that will confirm the placement of the boxes
    def confirmPlacement(self):
        self.hasPlaced = True

    # This will be a method that will be used when we have to use the box to determine the reverseConnections, it is to be called with testing boxes only
    def testTargetCoordinates(self):
        # This is very important, we have to maintain the list of the placedConnections and the unPlacedConnections, and our main concern is with the placed connections
        # We will extract the placed connections, and we will append them to the reverseConnectionsList of the window
        placedConnections = []
        unPlacedConnections = []
        for connection in self.connections:
            if connection.target.hasPlaced == True:
                placedConnections.append(connection)
            else:
                unPlacedConnections.append(connection)

        # We will place the unPlacedConnections
        for connection in unPlacedConnections:
            connection.target.setCoordinates(self.x + self.width + self.container.xpad, self.y)
            connection.target.confirmPlacement()
            connection.setConnection("right","left")
            connection.target.testTargetCoordinates()
        
        # Now we will place the placedConnections into the reverseConnectionsList
        for placedConnection in placedConnections:
            # This will keep track whether the reverse has been detected or not
            isReverseDetected = False 
            # We will loop over the reverseConnectionsList and check whether the reverse of the placedConnection is already present in the reverseConnectionsList
            for reverseConnection in self.container.reversedConnections:
                if Connection.checkIfAreReverse(placedConnection,reverseConnection) == True: 
                    # In this case we will not append the placedConnection to the reverseConnectionsList, and we will break out of the loop
                    isReverseDetected = True
                    break
            # If its reverse has already been determined in the container we will not append it to the reversedConnections list, because it has already been appended
            if isReverseDetected == False:
                self.container.reversedConnections.append(placedConnection)

    # This will be the method that will be used to set the coordinates of the target boxes that originate from this box
    def setTargetCoordinates(self):
        # First we will maintain a list of all the already placed target boxes and all the new boxes
        placedConnections = []
        unPlacedConnections = []
        for connection in self.connections:
            if connection.target.hasPlaced == True:
                placedConnections.append(connection)
            else:
                unPlacedConnections.append(connection)
        
        # First we will place all the unPlaced target boxes in such a way that they are placed in the same row as the source box, and we will also stack them on top of each other
        self.placeUnplacedBoxes(unPlacedConnections, self.container.xpad, 0)

        # Then we will make make the connections between the boxes that have been already placed
        self.placePlacedBoxes(placedConnections)

        # After setting the coordinates, the root node will now called the setTargetCoordinates method of the target nodes which are just placed right now
        for connection in unPlacedConnections:
            connection.target.setTargetCoordinates()

    # This will be the method that will be used to place the unplaced boxes
    def placeUnplacedBoxes(self, unPlacedConnections, startingXPosition, startingYPosition):        
        if (len(unPlacedConnections) % 2 == 1):
                self.setOddConnections(unPlacedConnections,startingXPosition,startingYPosition)
        else:
                self.setEvenConnections(unPlacedConnections,startingXPosition,startingYPosition)

        # After we have placed all the boxes we will check for the overlap of the placed boxes with other boxes, if there is an overlap we will call the function again with a changed starting position, iteratively making sure that all the boxes are placed properly
        for connection in unPlacedConnections:
            isOverlapDetected = self.container.checkBoxOverlap(connection.target,self.container.padValue)
            if isOverlapDetected != 0:
                # For an upper overlap we will decrement the y counter
                if isOverlapDetected == 1:
                    self.placeUnplacedBoxes(unPlacedConnections, startingXPosition, startingYPosition - 2 * self.container.padValue)
                # For an lower overlap we will increment the y counter
                if isOverlapDetected == 2:
                    self.placeUnplacedBoxes(unPlacedConnections, startingXPosition, startingYPosition + 2 * self.container.padValue)
                # For a right overlap we will increment the x counter
                if isOverlapDetected == 4:
                    self.placeUnplacedBoxes(unPlacedConnections, startingXPosition + 2 * self.container.padValue, startingYPosition)
                return
            
        # Once we are sure of no overlaps we will confirm the placement of the boxes and we will also set the source edge and the target edge of the connection
        for connection in unPlacedConnections:
            connection.target.confirmPlacement()
            connection.setConnection("right","left")

    def setEvenConnections(self,unPlacedConnections,startingXPosition,startingYPosition):
        for i in range(len(unPlacedConnections)):
            if i == 0:
                unPlacedConnections[i].target.setCoordinates(self.x + self.width + startingXPosition, self.y + startingYPosition - self.container.ypad - unPlacedConnections[i].target.height)

            elif (i == 1):
                unPlacedConnections[i].target.setCoordinates(self.x + self.width + startingXPosition, self.y + startingYPosition + self.height + self.container.ypad)
            
            elif (i % 2 == 0):
                unPlacedConnections[i].target.setCoordinates(self.x + self.width + startingXPosition, unPlacedConnections[i - 2].target.y + startingYPosition - self.container.ypad - unPlacedConnections[i].target.height)
            
            elif (i % 2 == 1):
                unPlacedConnections[i].target.setCoordinates(self.x + self.width + startingXPosition, unPlacedConnections[i - 2].target.y + startingYPosition + unPlacedConnections[i - 2].target.height + self.container.ypad)

    
    def setOddConnections(self,unPlacedConnections,startingXPosition,startingYPosition):
        for i in range(len(unPlacedConnections)):
            if i == 0:
                unPlacedConnections[i].target.setCoordinates(self.x + self.width + startingXPosition, self.y + startingYPosition)

            elif (i == 1):
                unPlacedConnections[i].target.setCoordinates(self.x + self.width + startingXPosition, self.y + startingYPosition - self.container.ypad - unPlacedConnections[i].target.height)
            
            elif (i == 2):
                unPlacedConnections[i].target.setCoordinates(self.x + self.width + startingXPosition, self.y + startingYPosition + self.height + self.container.ypad)

            elif (i % 2 == 1):
                unPlacedConnections[i].target.setCoordinates(self.x + self.width + startingXPosition, unPlacedConnections[i - 2].target.y + startingYPosition - self.container.ypad - unPlacedConnections[i - 2].target.height)
            
            elif (i % 2 == 0):
                unPlacedConnections[i].target.setCoordinates(self.x + self.width + startingXPosition, unPlacedConnections[i - 2].target.y + startingYPosition + unPlacedConnections[i - 2].target.height + self.container.ypad)
            

    # For the already placed connections, we will set their connections only in accordance with the relative heights of the two boxes
    def placePlacedBoxes(self, placedConnections):
        for connection in placedConnections:
            isManyToOne = False
            # We will ge the sources for the connection
            sources = connection.target.getSources()
            # If it the target box has the source of an stackedBox to a box, we will set the connection accordingly, from left to right
            for source in sources:
                if Box.isStacked(source,self):
                    # In case of a stacked source box we will set the connection from left to right
                    connection.setConnection("right","left")
                    isManyToOne = True
                    break
            # If it is not a many to one case we will set the connection from top to bottom
            if self.y < connection.target.y and isManyToOne == False:
                connection.setConnection("up","up")
            elif self.y >= connection.target.y and isManyToOne == False:
                connection.setConnection("down","down")
            # If the two boxes happen to be stacked on each other and you want to express them, you can use a variety of arrows, like
            if (Box.isStacked(connection.target,connection.source) == True):
                if (Box.areImmediate(connection.target,connection.source) == True):
                    # If the target is above the source, we will go for a up, down connection
                    if connection.target.y < connection.source.y:
                        connection.setConnection("up","down")

                    # Else we will go for a down,up connection
                    else:
                        connection.setConnection("down","up")
                else:
                    # In case the target is the last box we will go for the right, right case
                    if connection.target.isLast == True:
                        connection.setConnection("right","right")
                    # In case the target is not the last box we will check out the which of the four connections is free
                    else:
                        if connection.source.isTopIn == False:
                            connection.setConnection("up","left")
                        elif connection.source.isBottomIn == False:
                            connection.setConnection("down","left")
                        else:
                            connection.setConnection("right","left")

    # This will be the function that will compare two boxes, two boxes are equal if they have the same width, height, x and y coordinates
    def compareBoxes(box1,box2):
        if box1.width == box2.width and box1.height == box2.height and box1.name == box2.name:
            return True
        return False

    # This will be the method that will create the clone of the box
    def createClone(self,grid = None):
        if grid == None:
            return Box(self.name,self.width,self.height,self.x,self.y)
        else:
            return Box(self.name,self.width,self.height,self.x,self.y,container=grid)
    
    def isStacked(box1,box2):
        # If two boxes are stacked we will return true, they are stacked if they have the same x coordinate
        if (box1.x == box2.x and box1.hasPlaced == True and box2.hasPlaced == True and Box.compareBoxes(box1,box2) == False):
            return True

        # If it is not the case we wil return false
        return False
    
    def areImmediate(box1,box2):
        if (Box.compareBoxes(box1,box2) == True):
            return False
        # For two adjacent boxes, you can find that by using the formula
        # For box2 above the box1
        # I am assuming that the ypad is 100,and the container of the box1 is the same as the box2
        if box2.y == box1.y - box1.height - box1.container.ypad:
            return True
        
        # For box1 above box2 
        if box1.y == box2.y - box2.height - box1.container.ypad:
            return True
        
        # If either of the cases do not occur we will return false
        return False
        
    # In order to find out the many to one cases we will need to find out the stacked boxes to the box
    # When it is the time to place a box, we will find out the boxes adjacent to that box
    def findStackedBoxes(self):
        for box in self.container.boxes:
            # We will check if two boxes are stacked on top of each other
            if (Box.isStacked(self,box)):
                self.adjacentBoxes.append(box)
    
    # This will be the method that can be used to find out the sources of a box
    def getSources(self):
        sources = []
        for connection in self.container.connections:
            # If the target of the connection is the current box, we will append the source of the connection to the sources list
            if Box.compareBoxes(connection.target,self):
                sources.append(connection.source)
        return sources
    
    # This will be the method that can be used to find out the targets of a box
    def getTargets(self):
        targets = []
        for connection in self.connections:
            targets.append(connection.target)
        return targets

# This will be the class that will be the used to represent the connections
class Connection():
    def __init__(self, source, target, isReverse = False):
        self.source = source
        self.target = target
        self.sourceEdge = None
        self.targetEdge = None

    def setConnection(self, sourceEdge, targetEdge):
        self.sourceEdge = sourceEdge
        self.targetEdge = targetEdge
    
        if sourceEdge == "right":
            self.source.isRightOut = True
        elif sourceEdge == "left":
            self.source.isLeftOut = True
        elif sourceEdge == "up":
            self.source.isTopOut = True
        elif sourceEdge == "down":
            self.source.isBottomOut = True

        if targetEdge == "right":
            self.target.isRightIn = True
        elif targetEdge == "left":
            self.target.isLeftIn = True
        elif targetEdge == "up":
            self.target.isTopIn = True
        elif targetEdge == "down":
            self.target.isBottomIn = True
        


    # If it is a reverse connection we will declare it as a reverse connection
    def declareReverse(self):
        self.isReverse = True

    # This will create a clone of the current connection, with the new references to the boxes
    def createClone(self,boxes,grid = None):
        newSource = None
        newTarget = None
        for box in boxes:
            if Box.compareBoxes(box,self.source):
                newSource = box
            if Box.compareBoxes(box,self.target):
                newTarget = box
        if (newSource == None or newTarget == None):
            raise Exception("The boxes are not present in the list of boxes")
        
        return Connection(newSource,newTarget)
    
    # This will be the method that will compare two connections, to see if they are reverse or not
    def checkIfAreReverse(connection1,connection2):
        if Box.compareBoxes(connection1.source,connection2.target) == True and Box.compareBoxes(connection1.target,connection2.source) == True:
            return True
        return False
    
    # We will compare two connections, they are the same if the source and the target are the same
    def compareConnections(connection1,connection2):
        if Box.compareBoxes(connection1.source,connection2.source) and Box.compareBoxes(connection1.target,connection2.target):
            return True
        return False
    
def generatePlacement(x,y):
    boxes = []
    connections = []

    for box in x:
        boxes.append(Box(box[0],box[1],box[2]))
    
    for connection in y:
        for box in boxes:
            if box.name == connection[0]:
                source = box
            if box.name == connection[1]:
                target = box
        connections.append(Connection(source,target))

    container = Container(boxes,connections)

    container.setBoxes()

    boxes = container.boxes

    response = []
    sub = []

    for box in boxes:
        sub.append([box.x,box.y])

    response.append(sub)
    sub = []
    
    for connection in container.connections:
        sub.append([connection.source.name,connection.target.name,connection.sourceEdge,connection.targetEdge])
    response.append(sub)

    return response
