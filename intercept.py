# this script will calculate the change in velocity required to change orbit
# such that it will intercept with a target body, and the second velocity change
# required to match orbit
# assuming the two bodies are in stable circular orbits around a third body
# polar coordinates will be used

import math
import random


# the following class structure is similar to the orbital script, and so later
# versions may share these classes depending on the integration between scripts
class point:
    def __init__(self, r, t):
        self.r = r
        self.t = t

class body:
    def __init__(self, position, initRadius, mass, velocity, designation):
        self.position = position
        self.initRadius = initRadius
        self.mass = mass
        self.velocity = velocity
        self.designation = designation

# by assuming that the bodies start in stable orbits, the orbital radius is
# equal to the length of the position vector
def createOrbits(radius1, radius2, gravConstant, centralMass):

    # in this implementation, index 0 will be the central body, 1 will be the target
    # and 2 will be the body that changes orbit to intercept 1

    # given the radii, compute the corresponding velocities
    speed1 = math.sqrt( gravConstant * centralMass / radius1 )
    speed2 = math.sqrt( gravConstant * centralMass / radius2 )
    angularV1 = speed1 / radius1
    angularV2 = speed2 / radius2

    # create the bodies, using the orbital data above
    bodiesList = [
        body ( position = point(0,0), initRadius = 0, mass = centralMass, velocity = point(0,0), designation = "Central" ),
        body ( position = point(radius1, 6.28 * random.random()), initRadius = radius1, mass = 1, velocity = point(0, angularV1), designation = "Stable" ),
        body ( position = point(radius2, 6.28 * random.random()), initRadius = radius2, mass = 1, velocity = point(0, angularV2), designation = "Interceptor" )
        ]

    return bodiesList

# given the orbital velocites calculated when constructing the bodies, this
# computes the change of velocity necessary to make the orbits intercept
# the change in kinetic energy of the body on one side of the orbit will
# change the potential energy of the body on the other side of the orbit
# causing a corresponding change in orbital radius
# note that this assumes that the change in velocity is instant, which is unrealistic
# future versions will account for limited thrust capabilities
def calcInterceptVelocity(bodiesList, gravConstant):
    radiusChange = bodiesList[1].initRadius - bodiesList[2].initRadius
    potentialChange = ( gravConstant * bodiesList[0].mass * bodiesList[2].mass ) / radiusChange
    vChange = math.sqrt( 2 * potentialChange / bodiesList[2].mass )
    return vChange

# calculate the time it will take for the interceptor to complete half of its new
# orbit, when it will intercept the orbit of the other object
def calcEllipsePeriod(radius1, radius2, gravConstant, centralMass):
    semiMajor = (radius1 + radius2) / 2
    pSquared = (4 * 3.14**2)(semiMajor)**3 / (gravConstant * centralMass)
    period = math.sqrt(pSquared)
    return period

# the stable object must be interceptTime * velocity away from the intercept
# point at the time of the velocity change. Hence, the relative angle between
# the objects must be the difference between pi (the angle covered by the
# interceptor to intercept) and the angle swept out by the stable object in
# time interceptTime
def relativeAngle(interceptTime, bodiesData):
    interceptorSweepAngle = 3.14
    stableSweepAngle = interceptTime * bodiesData[1].velocity.t
    relative = interceptorSweepAngle - stableSweepAngle


if __name__ == '__main__':

    # system constants
    gravConstant = 6.67408e-11
    radius1 = 1000
    radius2 = 100000
    centralMass = 1e6

    bodiesData = createOrbits(radius1, radius2, gravConstant, centralMass)
    velocityChange = calcInterceptVelocity(bodiesData, gravConstant)
    interceptTime = calcEllipsePeriod(radius1, radius2, gravConstant, centralMass) / 2
    # note that the relative angle is measured from the interceptor to the stable object
    # at the correct time to change the velocity of the interceptor
    angle = relativeAngle(interceptTime, bodiesData)

    print("Change in velocity required: " + velocityChange)
    print("Relative angle at burn time: " + angle)
