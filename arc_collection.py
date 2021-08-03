import os
import datetime
import csv

class Arcs():
    def saveArcData(arcs, image, fileName = None):
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