import tkinter as tk
from imageGeneration import generateArcs, generateImage
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)


window = tk.Tk()
window.title('Image Generation Testing')
window.geometry("800x800")

inputFrame = tk.Frame(master = window)
canvasFrame = tk.Frame(master = window)

inputFrame.grid(column=0, row=0)

canvasFrame.grid(column=0, row=1)

canvas = None
toolbar = None

def displayFigure(fig = None):
    global canvas, toolbar
    if canvas:
        canvas.get_tk_widget().destroy()

    if not fig:
        fig = Figure(figsize = (8, 8),
                    dpi = 200)

    canvas = FigureCanvasTkAgg(fig, master = canvasFrame)

    ax = fig.gca()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)

    canvas.draw()
    canvas.get_tk_widget().grid(column = 1, row = 2)
    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(column = 1, row = 2)

def initializeCanvas():
    displayFigure()


def updateCanvas():
    curvature = curvatureEntry.get()
    length = lengthEntry.get()
    eccentricity = eccentricityEntry.get()

    separation = separationEntry.get()
    amount = amountEntry.get()
    if curvature and length and separation and amount:
        arcs = generateArcs(curvature = curvature, length = length, eccentricity = eccentricity, amount = amount)
        fig = generateImage(arcs, minSeparation = separation)
        displayFigure(fig)
    else:
        displayFigure()

curvatureLabel = tk.Label(text = "Curvature", master = inputFrame)
curvatureEntry = tk.Entry(master = inputFrame)
curvatureEntry.insert(0, "0.002-0.01")
curvatureLabel.grid(column = 0, row = 0)
curvatureEntry.grid(column = 0, row = 1)

lengthLabel = tk.Label(text = "Length", master = inputFrame)
lengthEntry = tk.Entry(master = inputFrame)
lengthEntry.insert(0, "100-500")
lengthLabel.grid(column = 1, row = 0)
lengthEntry.grid(column = 1, row = 1)

eccentricityLabel = tk.Label(text = "Eccentricity", master = inputFrame)
eccentricityEntry = tk.Entry(master = inputFrame)
eccentricityEntry.insert(0, "1")
eccentricityLabel.grid(column = 2, row = 0)
eccentricityEntry.grid(column = 2, row = 1)

amountLabel = tk.Label(text = "Amount", master = inputFrame)
amountEntry = tk.Entry(master = inputFrame)
amountEntry.insert(0, "10")
amountLabel.grid(column = 3, row = 0)
amountEntry.grid(column = 3, row = 1)

separationLabel = tk.Label(text = "Minimum Separation", master = inputFrame)
separationEntry = tk.Entry(master = inputFrame)
separationEntry.insert(0, "5")
separationLabel.grid(column = 4, row = 0)
separationEntry.grid(column = 4, row = 1)

generateButton = tk.Button(inputFrame, text = "Generate", command = updateCanvas)
generateButton.grid(column = 5, row = 1)

initializeCanvas()

window.mainloop()