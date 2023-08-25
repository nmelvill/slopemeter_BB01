import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd


class SensorPlot:

    xlength = 500
    xindex = np.arange(0,xlength,1)       #creates iterable based on the length of the x axis and how many points to display on plot

    def __init__(self):
        self.data = np.empty(1)
        self.figure = plt.figure()
        self.xdata = SensorPlot.xindex

        self.plotsetup()

    
    def plotsetup(self):

        plt.style.use('ggplot')
    
    
    def animate(self, frame):
        
        data = pd.read_csv('IMUdata.csv')
        
        datatail = (data.tail(500))

        
        plt.cla()                               #Clears the axis 
        plt.plot(SensorPlot.xindex, datatail['accelX'])        

    def showPlot(self):
        plt.show()


if __name__ == '__main__':

    
    testplot = SensorPlot()
   
    ani = FuncAnimation(plt.gcf(), testplot.animate, interval=100,frames=testplot.xdata)

    plt.show()

        




