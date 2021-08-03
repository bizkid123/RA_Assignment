import math
import random
from scipy import integrate
from arcs import CircularArc, EllipticalArc


class ArcGenerator():
    def __init__(self, width = 1600, height = 1600):
        self.width = width
        self.height = height

    def parseInfo(self, inputs):
        parsedInputs = []

        for x in inputs:
            # Allows for inputs to have a range, of the form 'x-y'
            if "-" in x:
                tmp = x.split("-")
                parsedInputs.append([float(tmp[0]), float(tmp[1])])
            else:
                # If there is no range, create a fake range with identical start and end for use in generateArcs
                parsedInputs.append([float(x), float(x)])

        return parsedInputs

    def placeArcs(self, toPrint = False):
        # List of finalized arcs
        finishedArcs = []

        for i, arc in enumerate(self.arcs):
            count = 0

            # Any time arc is invalid, recreate it
            while arc.fastOutOfBounds() or any([False] + [math.floor(finishedArc.fastMinimumDistance(arc))<self.minDist for finishedArc in finishedArcs]):
                arc.randomizePositioning()

                count += 1
                if count > 100:
                    break
            else:
                finishedArcs.append(arc)

        if toPrint:
            for arc in finishedArcs:
                print(arc.printShape())
        
        self.arcs = finishedArcs
        return finishedArcs


class EllipticalArcGenerator(ArcGenerator):
    def __init__(self, eccentricity, length, angle, minDist, width, height):
        self.minDist = minDist
        self.eccentricity = eccentricity
        self.length = length
        self.angle = angle
        super().__init__(width, height)

    def createArc(self, eccentricity, length, angle):
        # Calculate b/a using e = sqrt(1-b^2/a^2)
        axisRatio = math.sqrt(1 - eccentricity**2)

        # Initialize start angle randomly
        theta1 = random.random()*2*math.pi

        # Make end angle so arc is between 30 and 330 degrees
        theta2 = theta1 + random.random()*5/3*math.pi + math.pi/6

        # Integral formula for arc length
        def integrand(theta,a,b):
            return math.sqrt((a**2)*(math.sin(theta)**2) + (b**2)*(math.cos(theta)**2))

        # Initialize axis in correct ratio 
        a = 1
        b = 1*axisRatio

        # Calculate arcLength
        arcLengthIntegral = integrate.quad(integrand, theta1, theta2, args=(a,b))
        arcLength = arcLengthIntegral[0]

        # Scale axes to correct size
        a *= length / arcLength
        b *= length / arcLength

        arc = EllipticalArc(a, b, theta1, theta2, angle, width = self.width, height = self.height, length = length)
        return arc

    def generateArcs(self, amount = 1):
        self.eccentricity, self.length, self.angle = self.parseInfo([self.eccentricity, self.length, self.angle])
        amount = int(amount)
        self.arcs = []

        # Create arcs using parameters specified
        for i in range(amount):
            # Choose random value within each parameters range
            arcLength = random.random()*(self.length[1] - self.length[0]) + self.length[0]
            arcEccentricity = random.random()*(self.eccentricity[1] - self.eccentricity[0]) + self.eccentricity[0]
            arcAngle = random.random()*(self.angle[1] - self.angle[0]) + self.angle[0]

            # Create the arc
            self.arcs.append(self.createArc(eccentricity = arcEccentricity, length = arcLength, angle = arcAngle))

        self.placeArcs()
        return self.arcs


class CircularArcGenerator(ArcGenerator):
    def __init__(self, curvature, length, minDist, width, height):
        self.minDist = minDist
        self.curvature = curvature
        self.length = length
        super().__init__(width, height)

    def createArc(self, curvature, length):
        radius = 1/curvature
        circumference = 2*math.pi*radius
        
        theta1 = random.random()*2*math.pi
        # Calculate end angle to ensure correct arc length
        theta2 = theta1 + 2*math.pi * (length/circumference) 

        arc = CircularArc(radius, theta1, theta2, width = self.width, height = self.height, length = length)
        return arc

    def generateArcs(self, amount = 1):
        self.length, self.curvature = self.parseInfo([self.length, self.curvature])
        amount = int(amount)
        self.arcs = []

        # Create arcs using parameters specified
        for i in range(amount):
            # Choose random value within each parameters range
            arcCurve = random.random()*(self.curvature[1] - self.curvature[0]) + self.curvature[0]
            arcLength = random.random()*(self.length[1] - self.length[0]) + self.length[0]

            # Create the arc
            self.arcs.append(self.createArc(curvature = arcCurve, length = arcLength))

        self.placeArcs()


