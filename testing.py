import tkinter as tk
from imageGeneration import generateImage
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)


window = tk.Tk()
window.title('Image Generation Testing')
window.geometry("800x800")

inputFrame = tk.Frame(master = window)
canvasFrame = tk.Frame(master = window)

inputFrame.grid(column=0, row=0)

canvasFrame.grid(column=0, row=2)

canvas = None
toolbar = None

def displayFigure(fig = None):
    global canvas, toolbar
    if canvas:
        canvas.get_tk_widget().destroy()

    if not fig:
        fig = Figure(figsize = (5, 5),
                    dpi = 100)
    canvas = FigureCanvasTkAgg(fig, master = canvasFrame)
    canvas.draw()
    canvas.get_tk_widget().grid(column = 1, row = 2)
    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(column = 1, row = 2)


def updateCanvas():
    curvature = curvatureEntry.get()
    length = lengthEntry.get()
    separation = separationEntry.get()
    amount = amountEntry.get()
    if curvature and length and separation and amount:
        fig = generateImage(curvature = curvature, length = length, minSeparation = separation, amount = amount)
        displayFigure(fig)
    else:
        displayFigure()

curvatureLabel = tk.Label(text = "Curvature", master = inputFrame)
curvatureEntry = tk.Entry(master = inputFrame)
curvatureLabel.grid(column = 0, row = 0)
curvatureEntry.grid(column = 0, row = 1)

lengthLabel = tk.Label(text = "Length", master = inputFrame)
lengthEntry = tk.Entry(master = inputFrame)
lengthLabel.grid(column = 1, row = 0)
lengthEntry.grid(column = 1, row = 1)

separationLabel = tk.Label(text = "Minimum Separation", master = inputFrame)
separationEntry = tk.Entry(master = inputFrame)
separationLabel.grid(column = 2, row = 0)
separationEntry.grid(column = 2, row = 1)

amountLabel = tk.Label(text = "Amount", master = inputFrame)
amountEntry = tk.Entry(master = inputFrame)
amountLabel.grid(column = 3, row = 0)
amountEntry.grid(column = 3, row = 1)


generateButton = tk.Button(inputFrame, text = "Generate", command = updateCanvas)
generateButton.grid(column = 4, row = 1)

updateCanvas()

window.mainloop()