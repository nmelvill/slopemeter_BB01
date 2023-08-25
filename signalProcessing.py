import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pywt
from scipy.signal import lfilter , butter, filtfilt
from collections import deque



class Filter:
    cutoff = .01                  #The cutoff frequency is a function of the nyquist frequncy from 0-1 
    filterOrder =  4              


    def __init__(self, order, cutoff= .01):
        
        self.order = order
        self.cutoff = cutoff
        self.b , self.a = butter(self.order, self.cutoff)



class LiveFilter(Filter):
#Processes a signal coming in real time
    
    def __init__(self, order, cutoff= .01):
        super(LiveFilter, self).__init__(order, cutoff)
        self.signalbuffer = deque([0] * len(self.b), maxlen= len(self.b))            #Using deque to store buffer for faster performance
        self.outputbuffer =  deque([0] * (len(self.a)-1), maxlen= (len(self.a)-1))    #Buffer filter output for signal processing

    
    def filterSignal(self, reading):
    #Using a difference equation for low pass filter that scales based on the filter order
    #https://www.samproell.io/posts/yarppg/yarppg-live-digital-filter/
        
        self.signalbuffer.appendleft(reading)       
        
        output = np.dot(self.b, self.signalbuffer) - np.dot(self.a[1:], self.outputbuffer)  #Difference equation in dot product (vector) form
        output = output / self.a[0]                                                     #This apparently normalizes the output to go into the buffer
        self.outputbuffer.appendleft(output)

        return output

    def movingAverage(self, reading):

        self.signalbuffer.append(reading)

        output = sum(self.signalbuffer)/len(self.signalbuffer)

        return output

class StaticFilter(Filter):
#Processes a signal that is anlready in an array form potentially saved to a csv or otherwise    


    def __init__(self, signal, samplerate):
        Filter.__init__(self)
        self.signal = signal
        self.samplerate = samplerate
        self.spectrum = np.real(np.fft.rfft(signal))                         #Perform discrete fast fourier transform and takes absolute value to get amplitude of frequencies
        self.frequencies = np.fft.rfftfreq(signal.size, d=1./samplerate)
        self.length = signal.size
        self.xarray = np.arange(0, self.length, 1)                          #Create iterable array from the size of the signal array for plotting
        #self.positivespectrum = self.spectrum[0:self.spectrum.size/2]
        self.nyquist = self.samplerate // 2

    def haarWavelet(self):

        (cA, cD) = pywt.dwt([self.signal], 'db1')

        print("cA:", cA)
        print("cD:", cD)


    def plotSpectrum(self):

        plt.plot(self.frequencies, self.spectrum)
        plt.xlabel("frequency, Hz")
        plt.ylabel("Amplitude, units")
        #plt.xlim(0,100)
        #plt.ylim(0,0.4)
        plt.show()


    def plotSignal(self):

        plt.plot(self.xarray, self.signal)
        plt.xlabel("Time, ms")
        plt.ylabel("Acceleration, g")
        plt.show()

    def plotFilteredSignal(self):

        plt.plot(self.xarray, self.filteredSignal, self.xarray, self.signal)
        plt.xlabel("Time, ms")
        plt.ylabel("Acceleration, g") 
        plt.show()

    @property
    def filteredSignal(self):
        
        b , a = butter(StaticFilter.filterOrder, StaticFilter.cutoff)                       #Creates butter worth filter of order n and cutoff at frequency 
        return lfilter(self.b, self.a, self.signal)



def importCSV(file):
     data = pd.read_csv(file)

     return data



if __name__ == '__main__':
    
    
    df = importCSV('IMUdata.csv')
    samplerate = 1000                               

    accelx = StaticFilter(df['accelX'], samplerate)
    accely = StaticFilter(df['accelY'], samplerate)
    accelz = StaticFilter(df['accelZ'], samplerate)

    accelx.plotFilteredSignal()
    