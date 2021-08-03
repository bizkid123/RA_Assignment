import sympy 
import matplotlib 
import random


class Ellipse():
    def __init__(self, a, b, angle = 0, center = None, color = (0,0,0), width = 1600, height = 1600):
        self.a = a
        self.b = b
        self.angle = angle
        self.color = color
        self.width = width
        self.height = height
        self.type = "Ellipse"
        if center:
            self.center = center
        else:
            self.center = self.createCenter()

    def createCenter(self):
        dist = max(self.a, self.b)
        # Ensure it will never be out of bounds by placing in inner rectangle
        center = sympy.Point(random.randint(int(0 + dist), int(self.width - dist)),random.randint(int(0 + dist), int(self.height - dist)))
        return center

    def getDrawing(self):
        return matplotlib.patches.Ellipse(self.center, self.a*2, self.b*2, angle = self.angle, color=self.color)

    def getTitles(self):
        return ["Type", "a", "b", "Rotation", "Center"]

    def printShape(self):
        return self.type, self.a, self.b, self.angle, (self.center.x, self.center.y)

