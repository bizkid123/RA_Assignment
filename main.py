from arcs import CircularArc, EllipticalArc
from arc_generation import CircularArcGenerator, EllipticalArcGenerator
from hair_images import HairImage
from ellipses import Ellipse
import os
import datetime
import csv

def millimetersToPixels(millimeters, dpi=100):
    # 1 inch = 25.4 mm
    # 1 inch = dpi*1 pixels
    return millimeters/25.4*dpi

def saveShapeData(shapes, image, fileName = None):
    if not fileName:
        # Default fileName is date-time
        currentTime = datetime.datetime.now()
        date = currentTime.strftime("%x").replace("/","")
        time = currentTime.strftime("%X").replace(":","")
        fileName = date + "-" + time

    folderName = "hairTests"

    # Create folder if it doesn't yet exist
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    
    if type(shapes) != list: # For Ellipse it will be element instead
        shapes = [shapes]

    csvTitles = shapes[0].getTitles()
    csvInfo = [[*shape.printShape()] for shape in shapes]

    image.savefig(f"{folderName}/{fileName}.tiff", bbox_inches='tight', pad_inches=0)

    with open(f"{folderName}/{fileName}.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csvTitles)
        writer.writerows(csvInfo)

def loadShapeData(filePath, width = 800, height = 800):
    with open(filePath, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        header = next(csvReader)

        shapes = []

        for row in csvReader:
            # Center is always the last column
            center = row[-1].replace("(","").replace(")","").split(",") # (a, b) format handling
            center = (float(center[0].strip()), float(center[1].strip()))
            rowInfo = [float(val) for val in row[1:-1]] + [center]

            if row[0] == "Ellipse":
                img = HairImage(width, height, 100)
                shapes.append(Ellipse(*rowInfo))
            elif row[0] == "Circular Arc":
                img = HairImage(width, height, 100)
                shapes.append(CircularArc(*rowInfo))
            elif row[0] == "Elliptical Arc":
                img = HairImage(width, height, 100)
                shapes.append(EllipticalArc(*rowInfo))

        img.draw(shapes)
        img.realify(show = True)

    return shapes

if __name__ == "__main__":
    method = input("Select method - 'Load file', 'Cross-section', or 'Curves': ").lower()
    if method in ["load file", "'load file'"]:
        fileName = input("Enter file path: ")
        print("For below properties enter a number or press enter to use the default")
        width = input("Enter image width - [default: 800]") or 800
        height = input("Enter image height - [default: 800]") or 800
        loadShapeData(fileName, width, height)
    elif method in ["cross section", "'cross section'", "cross-section", "'cross-section'"]:
        a = input("Enter semi-major axis: ")
        b = input("Enter semi-minor axis: ")
        angle = input("Enter angle (in radians): ")
        
        print("For below properties enter a number or press enter to use the default")
        width = input("Enter image width - [default: 800]: ") or 800
        height = input("Enter image height - [default: 800]: ") or 800
    
        a, b, angle, width, height = int(a), int(b), float(angle), int(width), int(height)

        ellipse = Ellipse(a = a, b = b, angle = angle, width = 800, height = 800)
        img = HairImage(width, height, 100)
        img.draw([ellipse])
        img.realify()
        saveShapeData([ellipse], img.fig)
    elif method in ["curves", "'curves'"]:
        methodType = input("Select arc type - 'Circular Arc', 'Elliptical Arc': ").lower()
        if methodType in ["circular arc", "'circular arc'"]:
            print("For below properties give input as a float or a range separarated by a dash like a-b")
            curvature = input("Enter curvature: ")
            length = input("Enter length (in pixels): ")

            print("For below properties enter a number or press enter to use the default")
            minDist = input("Enter minimum separation - [default: 10]: ") or 10
            amount = input("Enter number of arcs - [default: 10]: ") or 10
            width = input("Enter image width - [default: 800]: ") or 800
            height = input("Enter image height - [default: 800]: ") or 800

            minDist, amount, width, height = int(minDist), int(amount), int(width), int(height)

            generator = CircularArcGenerator(curvature = curvature, length = length, minDist = minDist, width = width, height = height)      
            generator.generateArcs(amount)
            img = HairImage(width, height, 100)
            img.draw(generator.arcs)
            img.realify()
            saveShapeData(generator.arcs, img.fig)
        elif methodType in ["elliptical arc", "'elliptical arc'"]:
            print("For below properties give input as a float or a range separarated by a dash like 0-1")
            eccentricity = input("Enter eccentricity: ")
            length = input("Enter length (in pixels): ")
            angle = input("Enter angle (in radians): ")

            print("For below properties enter a number or press enter to use the default")
            minDist = input("Enter minimum separation - [default: 10]: ") or 10
            amount = input("Enter number of arcs - [default: 10]: ") or 10
            width = input("Enter image width - [default: 800]: ") or 800
            height = input("Enter image height - [default: 800]: ") or 800

            minDist, amount, width, height = int(minDist), int(amount), int(width), int(height)

            generator = EllipticalArcGenerator(eccentricity = eccentricity, length = length, angle = angle, minDist = minDist, width = width, height = height)      
            generator.generateArcs(amount)
            img = HairImage(width, height, 100)
            img.draw(generator.arcs)
            img.realify()
            saveShapeData(generator.arcs, img.fig)
        else:
            raise Exception("Invalid type")            
    else:
        raise Exception("Invalid method")
    