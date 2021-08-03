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
import datetime
import os
import csv

def saveCircularArcData(arcs, image, fileName = None):
    if not fileName:
        # default fileName is date-time
        currentTime = datetime.datetime.now()
        date = currentTime.strftime("%x").replace("/","")
        time = currentTime.strftime("%X").replace(":","")
        fileName = date + "-" + time

    folderName = "hairTests"

    # Create folder if it doesn't yet exist
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    
    csvTitles = ["Number", "Center", "Radius", "Theta1", "Theta2"]
    csvInfo = [[i, *arc.printArc()] for i, arc in enumerate(arcs)]

    image.savefig(f"{folderName}/{fileName}.tiff", bbox_inches='tight', pad_inches=0)

    with open(f"{folderName}/{fileName}.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csvTitles)
        writer.writerows(csvInfo)



if __name__ == "__main__":
    """
    print("running")
    arcs = generateArcs(curvature = "0.0004 - 0.01", length = "200-500", eccentricity ="0.8-1", amount = "5")
    print("done")
    generateImage(arcs, show = True)
    #"""

    arcStrings = """(200, 200) 50 0 6.28
(271, 271) 50 1.5707 6.29"""
    arcs = createArcsFromArcString(arcStrings, width = 800, height = 800)
    img = generateImage(arcs, width = 800, height = 800)

    saveCircularArcData(arcs, img)


