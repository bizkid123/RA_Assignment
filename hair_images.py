import io
import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy import ndimage


class HairImage():
    def __init__(self, width = 1600, height = 1600, dpi = 100):
        self.width = width
        self.height = height
        self.dpi = dpi
        self.setupImage()

    def draw(self, shapes):
        # Plot each arc on the figure
        for shape in shapes:        
            self.ax.add_patch(shape.getDrawing())

        plt.plot()

        plt.gcf().set_size_inches(self.width/self.dpi, self.width/self.dpi)
        return self.fig

    def setupImage(self):
        self.fig = plt.figure(figsize = (self.width/self.dpi, self.height/self.dpi), dpi = self.dpi, frameon = False)

        # Configure figure
        
        self.ax = plt.Axes(self.fig, [0., 0., 1., 1.])
        
        self.ax.axis('off')
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        
        self.fig.add_axes(self.ax)
        

        # Remove blank padding around figure
        for item in [self.fig, self.ax]:
            item.patch.set_visible(False)
        
        plt.style.use('grayscale')

    def realify(self, show = False, save = False):    
        self.fig.canvas.draw()

        # Save figure to memory buffer
        io_buf = io.BytesIO()
        self.fig.savefig(io_buf, format='png', transparent = True)
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
        # Arbitrary but should add to slightly below 1 to lighten
        k = np.array([
            [1/30, 1/25, 1/20, 1/20, 1/20],
            [1/30, 1/25, 1/20, 1/20, 1/20],
            [1/30, 1/25, 1/25, 1/20, 1/20],
            [1/35, 1/30, 1/25, 1/25, 1/25],
            [1/35, 1/35, 1/30, 1/30, 1/30]
        ])

        # Convolve image twice for blurring
        blurred = ndimage.convolve(imgArray, k, mode='constant', cval=0.0)
        blurred = ndimage.convolve(blurred, k, mode='constant', cval=0.0)
        blurred = self.blurLines(blurred)
        blurred = ndimage.convolve(imgArray, k, mode='constant', cval=0.0)
        blurred = ndimage.convolve(blurred, k, mode='constant', cval=0.0)
        blurred = self.blurLines(blurred)

        blurred = self.addNoise(blurred)

        plt.axis('off')

        # Display image onto figure
        plt.draw()

        plt.imshow(blurred, origin='lower', cmap = "gray_r", vmin = 0, vmax = 255)
        plt.draw()
        
        if show:
            plt.show()
        elif save:
            plt.savefig("generatedImage.tiff", bbox_inches='tight', pad_inches=0)
        
        return self.fig

    def addNoise(self, img):
        # For all white pixels, assign random light gray shade
        img = [[val if val > 50 else val/2+random.random()*30+20 for val in row] for row in img]
        return img

    def blurLines(self, img):
        # Add randomness to dark gray/black pixels and lighten them
        img = [[val/1.4-random.random()*40+25 if val > 80 else val for val in row] for row in img]
        return img
