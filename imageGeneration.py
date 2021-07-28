import random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
from scipy import integrate, ndimage
from Arc import CircularArc, EllipticalArc
import math
from PIL import Image



def parseInfo(inputs):
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


def generateArcs(curvature, length, eccentricity, amount):
    curvature, length, eccentricity = parseInfo([curvature, length, eccentricity])
    amount = int(amount)
    arcs = []

    # Create arcs using parameters specified
    for i in range(amount):
        # Choose random value within each parameters range
        arcCurve = random.random()*(curvature[1] - curvature[0]) + curvature[0]
        arcLength = random.random()*(length[1] - length[0]) + length[0]
        arcEccentricity = random.random()*(eccentricity[1] - eccentricity[0]) + eccentricity[0]
        arcs.append(createCircularArc(curvature = arcCurve, length = arcLength))
    
    # List of finalized arcs
    finishedArcs = []

    for arc in arcs:
        count = 0

        # Any time arc is invalid, recreate it
        while arc.isOutOfBounds() or any([False] + [finishedArc.getMinimumDistance(arc)<100 for finishedArc in finishedArcs]):

        #while arc.isOutOfBounds() or any([False] + [finishedArc.checkCollision(arc) for finishedArc in finishedArcs]):
            arc.randomizePositioning()

            count +=1
            if count > 50:
                print("breaking")
                break
        else:
            print("done")
            finishedArcs.append(arc)

    for arc in finishedArcs:
        arc.printArc()
    return finishedArcs


def generateImage(arcs, minSeparation = 5, show = False, save = False):
    arcsImage = drawArcs(arcs)


    # Add noise to make image more like actual hair sample
    realisticImage = realify(arcsImage, save = True)

    return realisticImage


def addNoise(img):
    # For all white pixels, assign random light gray shade
    img = [[val if val > 80 else random.random()*30+20 for val in row] for row in img]
    return img


def blurLines(img):
    # Add randomness to dark gray/black pixels and lighten them
    img = [[val/1.5-random.random()*20 if val > 80 else val for val in row] for row in img]
    return img


def realify(fig, show = False, save = False):    
    fig.canvas.draw()

    # Save figure to memory buffer
    io_buf = io.BytesIO()
    fig.savefig(io_buf, format='png', transparent = True)
    io_buf.seek(0)

    # Open image from buffer
    im = Image.open(io_buf).convert("L")

    # Close buffer
    io_buf.close()

    imgArray = np.array(im)
    # Turn image into Reverse Grayscale for easier convolutions
        # 255 is black, 0 is white
    imgArray = [[255-val for val in row] for row in imgArray][::-1]

    # Clear previous figure from canvas to make room for blurred
    plt.draw()
    plt.clf()

    # Convolution filter to blur and lighten thick dark lines  
    # TODO: Experiment with smaller filters that may be more versatile for cases with thin lines
    k = np.array([
        [1/90,1/80,1/70,1/50,1/60,1/70,1/90],
        [1/80,1/60,1/50,1/40,1/50,1/60,1/80],
        [1/60,1/50,1/40,1/20,1/40,1/50,1/60],
        [1/50,1/40,1/20,1/10,1/20,1/40,1/50],
        [1/60,1/50,1/40,1/20,1/40,1/50,1/60],
        [1/80,1/60,1/50,1/40,1/50,1/60,1/80],
        [1/90,1/70,1/60,1/50,1/60,1/70,1/90],
    ])

    # Convolve image twice for blurring
    blurred = ndimage.convolve(imgArray, k, mode='constant', cval=0.0)
    blurred = ndimage.convolve(blurred, k, mode='constant', cval=0.0)

    blurred = addNoise(blurred)
    blurred = blurLines(blurred)

    plt.axis('off')

    # Display image onto figure
    plt.draw()



    plt.imshow(blurred, origin='lower', cmap = "gray_r", vmin = 0, vmax = 255)
    plt.draw()
    
    if show:
        plt.show()
    elif save:
        plt.savefig("generatedImage.tiff", bbox_inches='tight', pad_inches=0)
    
    return fig


def drawArcs(arcs, gridWidth = 500, gridHeight = 500):
    fig = plt.figure(figsize = (16, 16), dpi = 100, frameon = False)

    # Configure figure
    
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    
    ax.axis('off')
    ax.set_ylim(0, 1600)
    ax.set_xlim(0, 1600)
    
    fig.add_axes(ax)
    

    # Remove blank padding around figure
    for item in [fig, ax]:
        item.patch.set_visible(False)
    
    plt.style.use('grayscale')

    # Plot each arc on the figure
    for arc in arcs:
        x = matplotlib.patches.Arc(arc.center, arc.a*2, arc.b*2, theta1=arc.theta1*57.2957, theta2=arc.theta2*57.2957, color=arc.color, lw = arc.lw)        
        ax.add_patch(x)

    plt.plot()

    #plt.show()

    plt.gcf().set_size_inches(16,16)
    return fig

def createEllipticalArc(eccentricity, length):
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

    arc = EllipticalArc(a, b, theta1, theta2)
    return arc


def createCircularArc(curvature, length):
    radius = 1/curvature
    circumference = 2*math.pi*radius
    
    theta1 = random.random()*2*math.pi
    # Calculate end angle to ensure correct arc length
    theta2 = theta1 + 2*math.pi * (length/circumference) 

    arc = CircularArc(radius, theta1, theta2)
    return arc


def createArcsFromArcString(arcStrings):
    arcStrings = arcStrings.split("\n")
    arcs = []
    for arcString in arcStrings:
        center, rest = arcString.split(")")
        center = center.split(",")
        center = (int(center[0][1:].strip()), int(center[1].strip()))


        rest = list(map(float, rest.split()))

        arc = CircularArc(*rest, center)
        arcs.append(arc)

    return arcs

if __name__ == "__main__":
    """
    print("running")
    arcs = generateArcs(curvature = "0.0004 - 0.01", length = "200-500", eccentricity ="0.8-1", amount = "5")
    print("done")
    generateImage(arcs, show = True)
    #"""


    arcStrings = """(200, 200) 50 0 6.29
(271, 271) 50 1.5707 6.29"""
    arcs = createArcsFromArcString(arcStrings)
    a1, a2 = arcs

    print("Distance =", round(a2.getMinimumDistance(a1), 3))
    generateImage(arcs, show = True)


    
