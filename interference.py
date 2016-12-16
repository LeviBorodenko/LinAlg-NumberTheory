from math import sin, pi, sqrt
import matplotlib.pyplot as plt
import numpy as np


class canvas(object):
    """[summary]
    The Canvas - basically a coordinate system. We will add our light sources to it
    so we can see pretty interference pictures.
    Arguments: x and y - see description!
    [description]
    Initialized by giving the Manhattan radius of your canvas
    Arguments:
    	x {[int]} -- length of the positive and negative x-axis
    	y {[int]} -- length of the positive and negative y-axis
    See test() for an example.
    """

    def __init__(self, x, y):
        super(canvas, self).__init__()
        self.x = x
        self.y = y
        self.baseL = (2 * pi) / (self.x + self.y)
        self.lightSources = []

    def addSource(self, x, y, Hz, Amp):
    	"""[summary]
    	Main feature. Using this you can add arbitrarily many light sources
    	to our canvas.
    	[description]
    	
    	Arguments:
    		x {[int]} -- xCoordinate of the light source
    		y {[int]} -- yCoordinate of the light source
    		Hz {[float / int]} -- Number of periods that the wave function will have in our canvas 
    		Amp {[float / int]} -- Amplitude of our wave
    	"""
        data = {"x": x, "y": y, "Hz": Hz, "Amp": Amp}
        self.lightSources.append(data)

    def waveFunction(self, xCord, yCord, data):
    	"""[summary]
    	Calculates the value of the wave function relative to a certain light source at (x, y)
    	[description]
    	The mathematical core
    	Arguments:
    		xCord {[int]} -- x coordinate
    		yCord {[int]} -- y coordinate
    		data {[dict]} -- the dict created by addSource that specifies the characteristics
    						 of an added light source.
    	
    	Returns:
    		[float] -- Value of the wave function
    	"""
        x = data["x"]
        y = data["y"]
        Hz = data["Hz"] * self.baseL
        Amp = data["Amp"]
        dist = sqrt((x - xCord)**2 + (y - yCord)**2)
        return Amp * sin(Hz * dist)

    def wave(self, x, y):
    	"""[summary]
    	Adds all relative wave functions together at a point (x, y) 
    	[description]
    	
    
    	Returns:
    		[float] -- value of the global wave function
    	"""
        Sum = 0
        for init in self.lightSources:
            Sum += self.waveFunction(x, y, init)
        return Sum

    def draw(self):
    	"""[summary]
    	Use this to generate your pretty picture.
    	[description]
    	Uses matplotlib. See test() to look at it in action.
    	"""
        data = []

        for x in range(-self.x, self.x + 1):
            row = []
            for y in range(-self.y, self.y + 1):
                row.append(self.wave(x, y))
            data.append(row)
        data = np.array(data)
        plt.imshow(data, interpolation="nearest")
        plt.show()


def test():
    c = canvas(200, 200)
    c.addSource(50, -80, 10, 1)
    c.addSource(50, 80, 10, 1)
    c.draw()
if __name__ == '__main__':
    test()
