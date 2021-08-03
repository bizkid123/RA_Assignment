import math
import random
import sympy
from scipy.spatial  import distance
from scipy import integrate
import numpy as np
import time
import matplotlib

class Arc():
    def __init__(self, a, b, theta1, theta2, angle = 0, center = None, lw = 5, color = (0,0,0), w = 1600, h = 1600, length = None):

        self.width = w
        self.height = h

        self.a = a
        self.b = b
        self.theta1 = theta1
        self.theta2 = theta2

        self.angle = angle

        self.centerOfMass = self.getCenterOfMass()
        if center:
            self.center = sympy.Point(center)
        else:
            self.center = sympy.Point(random.randint(int(0 - self.centerOfMass.x), int(self.width - self.centerOfMass.x)),random.randint(int(0 - self.centerOfMass.y), int(self.height - self.centerOfMass.y)))
        self.lw = lw
        self.color = color

        if length:
            self.length = length
        else:
            def integrand(theta,a,b):
                return math.sqrt((a**2)*(math.sin(theta)**2) + (b**2)*(math.cos(theta)**2))

            # Calculate arcLength
            self.length = integrate.quad(integrand, theta1, theta2, args=(self.a, self.b))[0]

        self.setEllipse()

    def getCenterOfMass(self):
        print("Center of mass is undefined.")
        return self.center

    def randomizePositioning(self):
        # Approximate adjustments based on centerOfMass
        self.center = sympy.Point(random.randint(int(0 - self.centerOfMass.x), int(self.width - self.centerOfMass.x)),random.randint(int(0 - self.centerOfMass.y), int(self.height - self.centerOfMass.y)))

        totalAngle = self.theta2 - self.theta1
        self.theta1 = random.random()*2*math.pi
        self.theta2 = self.theta1 + totalAngle

        self.setEllipse()

    def getLength(self):
        # Integral formula for arc length
        def integrand(theta,a,b):
            return math.sqrt((a**2)*(math.sin(theta)**2) + (b**2)*(math.cos(theta)**2))

        return integrate.quad(integrand, self.theta1, self.theta2, args=(self.a,self.b))

    def setEllipse(self):
        self.ellipse = sympy.Ellipse(self.center, self.a, self.b)

    def pointOnArc(self, pointX, pointY):
        # ASSUMES POINT IS ON THE ELLIPSE

        # Get angle from center to point
        angle = math.atan2(float(self.center.y - pointY), float(self.center.x - pointX))

        # Convert angle from -pi to pi, to 0 to 2pi and shift it correctly
        angle += math.pi
        
        # Check if collision point is on the arc -- point angle with arc angles
        # Also check case for angle range crosses 2pi, ie. 330 degrees - 450 degrees
        if self.theta1 < angle < self.theta2 or self.theta1 < angle + math.pi*2 < self.theta2:
            return True

        return False

    def getPoint(self, angle):
        angle = angle % (2 * math.pi)
        # Derived formulas
        if 0 <= angle <= math.pi/2 or 3*math.pi/2 <= angle <= 2*math.pi:
            x = self.center.x + (self.a * self.b) / (math.sqrt(self.b**2 + self.a**2 * (math.tan(angle))**2))
            y = self.center.y + (self.a * self.b * math.tan(angle)) / (math.sqrt(self.b**2 + self.a**2 * (math.tan(angle))**2))
        else:
            x = self.center.x - (self.a * self.b) / (math.sqrt(self.b**2 + self.a**2 * (math.tan(angle))**2))
            y = self.center.y - (self.a * self.b * math.tan(angle)) / (math.sqrt(self.b**2 + self.a**2 * (math.tan(angle))**2))
        
        if self.angle != 0:
            # Rotate the point with respect to the center
            c, s = math.cos(self.angle), math.sin(self.angle)
            nx = c * (x - self.center.x) - s * (y - self.center.y) + self.center.x
            ny = s * (x - self.center.x) + c * (y - self.center.y) + self.center.y
            x, y = nx, ny
        return (x,y)

    def exactOutOfBounds(self):
        if self.angle != 0:
            raise Exception("Angle must be 0. Use fastOutOfBounds instead")
        a = self.ellipse

        # Create rectangle representing boundary
        p1, p2, p3, p4 = [(0, self.height), (0, 0), (self.width, 0), (self.width, self.height)]
        rectangle = sympy.Polygon(p1, p2, p3, p4)

        inters = a.intersection(rectangle)

        # If intersection point is on the arc then it touches the boundary
        for point in inters:
            if self.pointOnArc(point.x, point.y):
                return True

        
        # If either arc endpoint is beyond the boundary, then arc is beyond the boundary 
        for angle in [self.theta1, self.theta2]:
            x,y = self.getPoint(angle)

            if not 0<=x<=self.width or not 0<=y<=self.height:
                return True
        return False

    def exactCollision(self, arc):
        if self.angle != 0:
            raise Exception("Angle must be 0. Use fastOutOfBounds instead")
        if self == arc:
            return False

        # Get intersection points
        inters = self.ellipse.intersection(arc.ellipse)

        # A collision occurs if any intersection point is actually on the arc
        for point in inters:
            if self.pointOnArc(point.x, point.y):
                return True
    
        return False

    def subdivide(self, divisions, startTheta, endTheta): 
        # Splits arc into even sections
        points = []
        angleChange = (endTheta - startTheta) / (divisions - 1)

        for i in range(divisions):
            angle = startTheta + i*angleChange
            x,y = self.getPoint(angle)
            points.append((angle, (x, y)))
        
        return np.array(points, dtype=object)

    def fastMinimumDistance(self, arc):
        start, end = self.theta1, self.theta2
        arcStart, arcEnd = arc.theta1, arc.theta2
        
        subdivisions = self.length//7
        minDist = ("NA", "NA", float("inf"))  

        while (end - start) > 0.01 or (arcEnd - arcStart) > 0.01:
            if subdivisions > 5:
                subdivisions = int(subdivisions / 1.5)
            minDist = ("NA", "NA", float("inf"))  

            points = self.subdivide(subdivisions, start, end)
            arcPoints = arc.subdivide(subdivisions, arcStart, arcEnd)          


            distances = distance.cdist([x[1] for x in points], [x[1] for x in arcPoints], 'euclidean')
            i, j = np.argwhere(distances == np.min(distances))[0]

            if i == 0:
                start = points[i][0]
                end = points[i+1][0]
            elif i == subdivisions - 1: 
                end = points[i][0]
                start = points[i-1][0]
            else:
                start = points[i-1][0]
                end = points[i+1][0]

            if j == 0:
                arcStart = arcPoints[j][0]
                arcEnd = arcPoints[j+1][0]
            elif j == subdivisions - 1: 
                arcEnd = arcPoints[j][0]
                arcStart = arcPoints[j-1][0]
            else:
                arcStart = arcPoints[j-1][0]
                arcEnd = arcPoints[j+1][0]

        #return math.sqrt(minDist[2])
        return distances[i][j]

    def fastOutOfBounds(self):
        points = self.subdivide(int(self.length), self.theta1, self.theta2)
        # If any point is out of bounds, arc is out of bounds
        for _, point in points:
            x, y = point
            if x > self.width or x < 0 or y > self.height or y < 0: 
                return True
        return False

    def fastCollision(self, arc):
        if self.fastMinimumDistance(arc) < 1:
            return True
        return False

class EllipticalArc(Arc):
    def __init__(self, a, b, theta1, theta2, angle = 0, center = None, lw = 5, color = (0,0,0), width = 1600, height = 1600, length = None):
        self.type = "Elliptical Arc"
        super().__init__(a, b, theta1, theta2, angle, center, lw, color, width, height, length)

    def getCenterOfMass(self):
        # Very approximate
        # Average of circles created from each axis
        x = (self.a+self.b)/2 * (math.sin(self.theta2+self.angle) - math.sin(self.theta1+self.angle))/(self.theta1+self.angle + self.theta2+self.angle)
        y = (self.a+self.b)/2 * (-math.cos(self.theta2+self.angle) + math.cos(self.theta1+self.angle))/(self.theta1+self.angle + self.theta2+self.angle)

        return sympy.Point(x,y)

    def getDrawing(self):
        return matplotlib.patches.Arc(self.center, self.a*2, self.b*2, angle = self.angle*57.2957, theta1=self.theta1*57.2957, theta2=self.theta2*57.2957, color=self.color, lw = self.lw)

    def getTitles(self):
        return ["Type", "a", "b", "Start Angle", "End Angle", "Rotation", "Center"]

    def printShape(self):
        return self.type, self.a, self.b, self.theta1, self.theta2, self.angle, (self.center.x, self.center.y)

class CircularArc(Arc):
    def __init__(self, radius, theta1, theta2, center = None, angle = 0, lw = 5, color = (0,0,0), width = 1600, height = 1600, length = None):
        self.radius = radius # redundant for readability later
        self.type = "Circular Arc"
        super().__init__(radius, radius, theta1, theta2, angle, center, lw, color, width, height, length)

    def getCenterOfMass(self):
        # Derived formulas
        x = self.radius * (math.sin(self.theta2) - math.sin(self.theta1))/(self.theta1 + self.theta2)
        y = self.radius * (-math.cos(self.theta2) + math.cos(self.theta1))/(self.theta1 + self.theta2)
        return sympy.Point(x,y)

    def exactMinimumDistance(self, arc):
        # Four cases
        # 1. Endpoints on each arc (4 options)
        # 2. Endpoint of one arc and intersection of line from center of the other to endpoint (4 options)
        # 3. Points along line between centers of intersection of both arcs (1 option)
        # 4. Collision points - Assumed to be distance -1 
        
        # Case 1
        collisions = self.checkCollision(arc)
        if collisions:
            return -1
    
        minDist = float("inf")

        # Case 2
        for angle in [self.theta1, self.theta2]:
            point = sympy.Point(self.getPoint(angle))
            line = sympy.Line(arc.center, point)

            possiblePoints = line.intersection(arc.ellipse)

            for possiblePoint in possiblePoints:
                if self.pointOnArc(possiblePoint.x, possiblePoint.y):
                    dist = point.distance(possiblePoint)
                    minDist = min(dist, minDist)

        # Arc endpoints
        for angle in [arc.theta1, arc.theta2]:
            point = sympy.Point(arc.getPoint(angle))
            line = sympy.Line(self.center, point)

            possiblePoints = line.intersection(self.ellipse)

            for possiblePoint in possiblePoints:
                if arc.pointOnArc(possiblePoint.x, possiblePoint.y):
                    dist = point.distance(possiblePoint)
                    minDist = min(dist, minDist)

        # Case 3
        for angle1 in [self.theta1, self.theta2]:
            point1 = sympy.Point(self.getPoint(angle1))
            for angle2 in [arc.theta1, arc.theta2]:
                point2 = sympy.Point(arc.getPoint(angle2))
                dist = point1.distance(point2)
                minDist = min(dist, minDist)

        # Case 4
        line = sympy.Line(self.center, arc.center)
        
        arc1Points = line.intersection(self.ellipse)
        arc1Points = [point for point in arc1Points if self.pointOnArc(point.x, point.y)]
        arc2Points = line.intersection(arc.ellipse)
        arc2Points = [point for point in arc2Points if arc.pointOnArc(point.x, point.y)]

        for point1 in arc1Points:
            for point2 in arc2Points:
                dist = point1.distance(point2)
                minDist = min(dist, minDist)

        return minDist

    def getDrawing(self):
        return matplotlib.patches.Arc(self.center, self.a*2, self.b*2, theta1=self.theta1*57.2957, theta2=self.theta2*57.2957, color=self.color, lw = self.lw)

    def getTitles(self):
        return ["Type", "Radius", "Start Angle", "End Angle", "Center"]

    def printShape(self):
        return self.type, self.radius, self.theta1, self.theta2, (self.center.x, self.center.y)











    
