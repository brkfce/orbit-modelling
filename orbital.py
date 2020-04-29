# thanks to https://medium.com/@bceagan/python-n-body-orbit-simulation-be3fb6356579 for inspiring this script

import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class point:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z

class body:
    def __init__(self, position, mass, velocity, designation):
        self.position = position
        self.mass = mass
        self.velocity = velocity
        self.designation = designation

# compute the total acceleration caused by each of the other bodies in the system
def calcAccelSingleBody(bodiesList, bodiesIndex):
    gravConstant = 6.67408e-11
    acceleration = point(0,0,0)
    selectedBody = bodiesList[bodiesIndex]

    for index, otherBody in enumerate(bodiesList):
        if index != bodiesIndex:
            # calculate the distance between one body and another
            rSquare = (selectedBody.position.x - otherBody.position.x)**2 + (selectedBody.position.y - otherBody.position.y)**2 + (selectedBody.position.z - otherBody.position.z)**2
            r = math.sqrt(rSquare)

            # calculate the total force caused by the other body
            F = gravConstant * otherBody.mass / r**2

            # normalise that force into the basis vectors of x y z, summing for all the bodies in the system
            acceleration.x += F * (otherBody.position.x - selectedBody.position.x) / r
            acceleration.y += F * (otherBody.position.y - selectedBody.position.y) / r
            acceleration.z += F * (otherBody.position.z - selectedBody.position.z) / r

    
    return acceleration

# update the velocities of each body in the system, based on the calculated acceleration for a given timestep
def calcVelocity(bodiesList, timestep):

    for index, selectedBody in enumerate(bodiesList):

        acceleration = calcAccelSingleBody(bodiesList, index)

        selectedBody.velocity.x += acceleration.x * timestep
        selectedBody.velocity.y += acceleration.y * timestep
        selectedBody.velocity.z += acceleration.z * timestep

# update the positions of each body in the system, using the calculated velocities for a given timestep
def calcPosition(bodiesList, timestep):

    for selectedBody in bodiesList:

        selectedBody.position.x += selectedBody.velocity.x * timestep
        selectedBody.position.y += selectedBody.velocity.y * timestep
        selectedBody.position.z += selectedBody.velocity.z * timestep

# using the above calculation functions, update the velocities and positions of bodies in the system
def updateSystem(bodiesList, timestep):
    calcVelocity(bodiesList, timestep)
    calcPosition(bodiesList, timestep)

# define a list of bodies (this could be replaced by a function that reads body data from a file)
def createBodies():

    # body data
    Body1 = {"position":point(0,0,0), "mass":2e30, "velocity":point(0,0,0)}
    Satelite1 = {"position":point(0,1.5e11,0), "mass":6e24, "velocity":point(30000,0,0)}
    Satelite2 = {"position":point(0,-1.5e11,0), "mass":6e24, "velocity":point(15000,0,0)}

    # construct bodies based upon the above data
    bodiesList = [
        body ( position = Body1["position"], mass = Body1["mass"], velocity = Body1["velocity"], designation = "Body 1" ),
        body ( position = Satelite1["position"], mass = Satelite1["mass"], velocity = Satelite1["velocity"], designation = "Satelite 1" ),
        body ( position = Satelite2["position"], mass = Satelite2["mass"], velocity = Satelite2["velocity"], designation = "Satelite 2" )
        ]

    return bodiesList

# run a simulation
def runSim(bodiesList, timestep, stepNumber):

    # create a dict to store the positions of each body
    positionData = []
    for selectedBody in bodiesList:
        positionData.append({"Designation": selectedBody.designation, "x":[], "y":[], "z":[]})

    # run the sim step by step and store the positions of each body at each step
    for i in range(stepNumber):
        
        updateSystem(bodiesList, timestep)
        
        for index, bodies in enumerate(bodiesList):

            positionData[index]["x"].append(bodiesList[index].position.x)
            positionData[index]["y"].append(bodiesList[index].position.y)
            positionData[index]["z"].append(bodiesList[index].position.z)

    return positionData

# visualise data using matplotlib
def visualise(positionData):

    figure = plt.figure()
    ax = plt.axes(projection = '3d')
    
    for index, bodies in enumerate(positionData):
        
        xData = positionData[index]["x"]
        yData = positionData[index]["y"]
        zData = positionData[index]["z"]
        designation = positionData[index]["Designation"]
        
        ax.plot3D(xData, yData, zData, label = designation)
    
    plt.show()


# main
if __name__ == '__main__':

    bodiesList = createBodies()
    timestep = 100
    stepNumber = 320000

    positionData = runSim(bodiesList, timestep, stepNumber)
    visualise(positionData)
    


    

    
