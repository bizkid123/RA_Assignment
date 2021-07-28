import math
import random
import sympy
from scipy import integrate
import time


class Arc():
    def __init__(self, a, b, theta1, theta2, center = None, lw = 7, color = (0,0,0)):
        self.a = a
        self.b = b
        self.theta1 = theta1
        self.theta2 = theta2

        if center:
            self.center = sympy.Point(center)
        else:
            self.center = sympy.Point(random.randint(0 - self.centerOfMass.x, 1600 - self.centerOfMass.x),random.randint(0 - self.centerOfMass.y, 1600 - self.centerOfMass.y))
        self.lw = lw
        self.color = color

        self.centerOfMass = self.getCenterOfMass()

        self.setEllipse()

    def getCenterOfMass(self):
        print("center of mass is undefined")
        return sympy.Point(0,0)

    def randomizePositioning(self):
        self.center = sympy.Point(random.randint(0 - self.centerOfMass.x, 1600 - self.centerOfMass.x),random.randint(0 - self.centerOfMass.y, 1600 - self.centerOfMass.y))

        totalAngle = self.theta2 - self.theta1
        self.theta1 = random.random()*2*math.pi
        self.theta2 = self.theta1 + totalAngle

        self.setEllipse()

    def getLength():
        # Integral formula for arc length
        def integrand(theta,a,b):
            return math.sqrt((a**2)*(math.sin(theta)**2) + (b**2)*(math.cos(theta)**2))

        return integrate.quad(integrand, self.theta1, self.theta2, args=(self.a,self.b))


    def setEllipse(self):
        print(self.center, self.a, self.b)
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
        if 0 <= angle <= math.pi/2 or 3*math.pi/2 <= angle <= 2*math.pi:
            x = self.center.x + (self.a * self.b) / (math.sqrt(self.b**2 + self.a**2 * (math.tan(angle))**2))
            y = self.center.y + (self.a * self.b * math.tan(angle)) / (math.sqrt(self.b**2 + self.a**2 * (math.tan(angle))**2))
        else:
            x = self.center.x - (self.a * self.b) / (math.sqrt(self.b**2 + self.a**2 * (math.tan(angle))**2))
            y = self.center.y - (self.a * self.b * math.tan(angle)) / (math.sqrt(self.b**2 + self.a**2 * (math.tan(angle))**2))

        return sympy.Point(x,y)

    def isOutOfBounds(self, w = 1600, h = 1600):
        a = self.ellipse

        # Create rectangle representing boundary
        w, h = 1600, 1600
        p1, p2, p3, p4 = [(0, h), (0, 0), (w, 0), (w, h)]
        rectangle = sympy.Polygon(p1, p2, p3, p4)

        inters = a.intersection(rectangle)

        # If intersection point is on the arc then it touches the boundary
        for point in inters:
            if self.pointOnArc(point.x, point.y):
                return True

        
        # If either arc endpoint is beyond the boundary, then arc is beyond the boundary 
        for angle in [self.theta1, self.theta2]:
            x,y = self.getPoint(angle)

            if not 0<=x<=w or not 0<=y<=h:
                return True
        return False

    def checkCollision(self, arc):
        if self == arc:
            return False

        start = time.perf_counter()

        inters = self.ellipse.intersection(arc.ellipse)

        end = time.perf_counter()
        #print(end - start)

        #print(inters)
        for point in inters:
            if self.pointOnArc(point.x, point.y):
                return True
    
        return False

class EllipticalArc(Arc):
    def __init__(self, a, b, theta1, theta2, center = None, lw = 7, color = (0,0,0)):
        super().__init__(a, b, theta1, theta2, center, lw, color)

    def getMinimumDistance(self, arc):
        print("Minimum distance is undefined for elliptical arcs right now")

    def printArc(self):
        return (self.center.x, self.center.y), self.a, self.b, self.theta1, self.theta2

class CircularArc(Arc):
    def __init__(self, radius, theta1, theta2, center = None, lw = 7, color = (0,0,0)):
        self.radius = radius # redundant for readability later
        super().__init__(radius, radius, theta1, theta2, center, lw, color)

    def getCenterOfMass(self):
        x = self.radius * (math.sin(self.theta2) - math.sin(self.theta1))/(self.theta1 + self.theta2)
        y = self.radius * (-math.cos(self.theta2) + math.cos(self.theta1))/(self.theta1 + self.theta2)
        return sympy.Point(x,y)

    def getMinimumDistance(self, arc):
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
            point = self.getPoint(angle)
            line = sympy.Line(arc.center, point)

            possiblePoints = line.intersection(arc.ellipse)

            for possiblePoint in possiblePoints:
                if self.pointOnArc(possiblePoint.x, possiblePoint.y):
                    #print(round(possiblePoint.x,3), round(possiblePoint.y,3))
                    #print(round(point.x,3), round(point.y,3))
                    dist = point.distance(possiblePoint)
                    #print(round(dist,3), "\n")

                    minDist = min(dist, minDist)
        # Arc endpoints
        for angle in [arc.theta1, arc.theta2]:
            point = arc.getPoint(angle)
            line = sympy.Line(self.center, point)

            possiblePoints = line.intersection(self.ellipse)

            for possiblePoint in possiblePoints:
                if arc.pointOnArc(possiblePoint.x, possiblePoint.y):
                    dist = point.distance(possiblePoint)
                    minDist = min(dist, minDist)
        print(round(minDist,3))


        # Case 3
        for angle1 in [self.theta1, self.theta2]:
            point1 = self.getPoint(angle1)
            for angle2 in [arc.theta1, arc.theta2]:
                point2 = arc.getPoint(angle2)
                dist = point1.distance(point2)
                minDist = min(dist, minDist)

        print(round(minDist,3))

        # Case 4
        line = sympy.Line(self.center, arc.center)
        
        arc1Points = line.intersection(self.ellipse)
        arc1Points = [point for point in arc1Points if self.pointOnArc(point.x, point.y)]
        arc2Points = line.intersection(arc.ellipse)
        arc2Points = [point for point in arc2Points if arc.pointOnArc(point.x, point.y)]


        #print(round(arc1Point[0].x,3), round(arc1Point[0].y,3))
        #print(round(arc2Point[0].x,3), round(arc2Point[0].y,3))
        for point1 in arc1Points:
            for point2 in arc2Points:
                dist = point1.distance(point2)
                minDist = min(dist, minDist)


        print(round(minDist,3))
        return minDist


    def printArc(self):
         return (self.center.x, self.center.y), self.radius, self.theta1, self.theta2










    
