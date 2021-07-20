import random
import matplotlib
import matplotlib.pyplot as plt

class Arc():
    def __init__(self, curve, length):
        self.curve = curve
        self.length = length

def parseInfo(inputs):

    parsedInputs = []
    for x in inputs:
        if "-" in inputs:
            tmp = x.split("-")
            parsedInputs.append([int(tmp[0]), int(tmp[1])])
        else:
            parsedInputs.append([int(x), int(x)])

    return parsedInputs

def generateImage(curvature, length, amount, minSeparation):
    curvature, length = parseInfo([curvature, length])

    arcs = []

    for i in range(len(amount)):
        arcCurve = random.random()*(curvature[1] - curvature[0]) + curvature[0]
        arcLength = random.random()*(length[1] - length[0]) + length[0]

        arcs.append(Arc(arcCurve, arcLength))

    return createArcs(arcs, minSeparation)

def createArcs(arcs, gridWidth = 500, gridHeight = 500, minSeparation = 5):
    fig = plt.figure(figsize = (5, 5),
                    dpi = 100)
    ax=fig.add_subplot(1,1,1)
    plt.axis('off')

    plt.plot()


    #for arc in arcs:
    x = matplotlib.patches.Arc((11,45),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color="black")        
    ax.add_patch(x)

    plt.savefig("generatedImage.png")
    return fig