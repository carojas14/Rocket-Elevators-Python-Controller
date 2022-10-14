
class Column:
    def __init__(self, id, amountOfFloors, amountOfElevators):
        self.ID = id
        self.status = "online"
        self.elevatorList = []
        self.callButtonList = []

        self.createElevators(amountOfFloors, amountOfElevators)
        self.createCallButtons(amountOfFloors)



    # Create a list of call buttons for each column using CallButton class
        # @param amountOfFloor
    def createCallButtons(self, amountOfFloors):
        buttonFloor = 1
        callButtonID = 0

        for i in range(amountOfFloors): #If it's not the last floor
            if buttonFloor < amountOfFloors:
                callButton = CallButton(callButtonID, buttonFloor, "Up")
                self.callButtonList.append(callButton)
                callButtonID+=1

            if buttonFloor > 1:
                callButton = CallButton(callButtonID, buttonFloor, "Down")
                self.callButtonList.append(callButton)
                callButtonID+=1

            buttonFloor+=1



    # Create a list of elevators for each column using Elevator class
        # @param amountOfFloor
    def createElevators(self, amountOfFloors, amountOfElevators):
        for i in range(amountOfElevators):
            elevatorID = i + 1
            elevator = Elevator(elevatorID, amountOfFloors)
            self.elevatorList.append(elevator)


    # User press a button outside the elevator
        #  @param floor
        #  @param direction
        #  @return elevator
    def requestElevator(self, floor, direction):
        elevator = self.findElevator(floor, direction)
        elevator.floorRequestList.append(floor)
        elevator.move()
        #elevator.door.status = "opened"
        elevator.operateDoors()
        return elevator


    # Find the best elevator
        # @param requestedFloor
        # @param requestedDirection
        # @return bestElevator
    def findElevator(self, requestedFloor, requestedDirection):

        bestElevator = None
        bestScore = 5
        referenceGap = 10000000
        bestElevatorInformations = None

        for i in range(len(self.elevatorList)):
            if requestedFloor == self.elevatorList[i].currentFloor and self.elevatorList[i].status == "stopped" and requestedDirection == self.elevatorList[i].direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(1, self.elevatorList[i], bestScore, referenceGap, bestElevator, requestedFloor)
            #The elevator is lower than me, is coming up and I want to go up
            elif requestedFloor > self.elevatorList[i].currentFloor and self.elevatorList[i].direction == "up" and requestedDirection == self.elevatorList[i].direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(2, self.elevatorList[i], bestScore, referenceGap, bestElevator, requestedFloor)
            #The elevator is higher than me, is coming down and I want to go down
            elif requestedFloor < self.elevatorList[i].currentFloor and self.elevatorList[i].direction == "down" and requestedDirection == self.elevatorList[i].direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(2, self.elevatorList[i], bestScore, referenceGap, bestElevator, requestedFloor)
            #The elevator is idle
            elif self.elevatorList[i].status == "idle":
                bestElevatorInformations = self.checkIfElevatorIsBetter(3, self.elevatorList[i], bestScore, referenceGap, bestElevator, requestedFloor)
            else:
                bestElevatorInformations = self.checkIfElevatorIsBetter(4, self.elevatorList[i], bestScore, referenceGap, bestElevator, requestedFloor)

            bestElevator = bestElevatorInformations["bestElevator"]
            bestScore = bestElevatorInformations["bestScore"]
            referenceGap = bestElevatorInformations["referenceGap"]
        return bestElevator


    # Called by findElevator to compare current elevator in elevatorList with
        # other elevators and return an object with the best score.
        # @param scoreToCheck
        # @param newElevator
        # @param bestScore
        # @param referenceGap
        # @param bestElevator
        # @param floor
        # @return {bestElevator, bestScore, referenceGap}
    def checkIfElevatorIsBetter(self, scoreToCheck, newElevator, bestScore, referenceGap, bestElevator, floor):
        if scoreToCheck < bestScore:
            bestScore = scoreToCheck
            bestElevator = newElevator
            referenceGap = abs(newElevator.currentFloor - floor)
        elif bestScore == scoreToCheck:
            gap = abs(newElevator.currentFloor - floor)
            if referenceGap > gap:
                bestElevator = newElevator
                referenceGap = gap

        return {
            "bestElevator":bestElevator,
            "bestScore":bestScore,
            "referenceGap":referenceGap
        }


class Elevator:
    def __init__(self, id, amountOfFloors):
        self.ID = id
        self.status = "idle"
        self.direction = None
        self.currentFloor = 1
        self.door = Door(id)
        self.floorRequestButtonList = []
        self.floorRequestList = []

        self.createFloorRequestButtons(amountOfFloors)


    # Create a list of call floor buttons for each column using FloorRequestButton class
        # @param amountOfFloors
    def createFloorRequestButtons(self, amountOfFloors):
        buttonFloor = 1
        floorRequestButtonID = 1
        for i in range(amountOfFloors):
            floorRequestButton = FloorRequestButton(floorRequestButtonID, buttonFloor)
            self.floorRequestButtonList.append(floorRequestButton)
            buttonFloor = i+1
            floorRequestButtonID = i+1


    # User press a button inside the elevator
        # Add the floor request to the list
        # Call move()
        # Call operateDoors()
        # @param floor
    def requestFloor(self, floor):
        self.floorRequestList.append(floor)
        self.move()
        self.operateDoors()


    # Move elevator to requested floor
    def move(self):
        while len(self.floorRequestList) != 0:
            destination = self.floorRequestList[0]
            self.status = "moving"
            # Elevator position is lower than requested floor
            if self.currentFloor < destination:
                self.direction = "up"
                self.sortFloorList()

                # Elevator move when it have a request
                while self.currentFloor < destination:
                    self.currentFloor+=1
                    self.screenDisplay = self.currentFloor

            # Elevator position is higher than requested floor
            elif self.currentFloor > destination:
                self.direction = "down"
                self.sortFloorList()

                # Elevator move when it have a request
                while self.currentFloor > destination:
                    self.currentFloor-=1
                    self.screenDisplay = self.currentFloor
            self.status = "stopped"
            self.floorRequestList.pop()
        self.status = "idle"


    # Sort the list of floor requested according to elevator direction
        # @return floorRequestList
    def sortFloorList(self):
        if self.direction == 'up':
            self.floorRequestList.sort()
        else:
            self.floorRequestList.reverse()


    # Manage doors
        # opened
        # closed
    def operateDoors(self):
        self.door.status = "opened"
        if self.door.status != "overweight":
            self.door.status = "closing"
            if self.door.status != "obstruction":
                self.door.status = "closed"
            else:
                self.operateDoors()
        else:
            while self.door.status != "overweight":
                self.door.status = "closing"
            self.operateDoors()


class CallButton:
    # button to call the elevator
    def __init__(self, id, floor, direction):
        self.ID = id
        self.status = "on"
        self.floor = floor
        self.direction = direction


class FloorRequestButton:
    # button inside the elevator to go to the requested floor
    def __init__(self, id, floor):
        self.ID = id
        self.status = "OFF"
        self.floor = floor


class Door:
    def __init__(self, id):
        self.ID = id
        self.status = "closed"
