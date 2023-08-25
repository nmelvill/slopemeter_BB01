import numpy as np
from math import pi as pi
import signalProcessing


class Position:

    def __init__(self):
        self.acceleration = np.zeros((3))
        self.angularVelocity = np.zeros((3))
        self.previousAcceleration = np.zeros((3))
        self.previousAngularVelocity = np.zeros((3))
        self.timeDelta = 0.250 / 1000                       # Convert from ms to seconds
        self.previousAngle = 0
        self.accelerationBuffer = np.zeros(shape=(50,3))
        self.angularVelocityBuffer = np.zeros(shape=(50,3))


    def setMotion(self,imuData):
    #Updates the position of    
        self.acceleration = np.array([imuData['accelX'], imuData['accelY'], imuData['accelZ']])
        
        self.angularVelocity = np.array([imuData['gyroX'], imuData['gyroY'], imuData['gyroZ']])
        
        self.timeDelta = imuData['timeDelta']

        self.bufferdata(100)


    def storePreviousValue(self):
    #Stores the current data to the previous data variables

        self.previousAcceleration = self.acceleration
        self.previousAngularVelocity = self.angularVelocity


    def bufferdata(self, n):
    #Buffers n number of data point in an 3 x n array for signal processing

        self.accelerationBuffer = np.append(self.accelerationBuffer, self.acceleration[None,:], axis=0)
        self.angularVelocityBuffer = np.append(self.angularVelocityBuffer, self.angularVelocity[None,:], axis=0)

        self.accelerationBuffer = self.accelerationBuffer[-n:,:]
        self.angularVelocityBuffer = self.angularVelocityBuffer[-n:,:]
        
    @property
    def linearPosition(self):
    #Integrates the linear acceleration data into a position    
        pass


    @property
    def angularPosition(self):
    #Integrates the angular velocity into an angular position

        self.previousAngle += 0.5 * (self.angularVelocity + self.previousAngularVelocity) * self.timeDelta  #Trapazoidal integration

        return self.previousAngle


    @property
    def accelPolarAngle(self):
    #Convert cartesian accelerometer data to spherical coordinates, specifically the polar angle or inclination.
        
        accelPolarAngle = (np.arccos(self.acceleration[2]/
                                    (np.sqrt(self.acceleration[0]**2 + self.acceleration[1]**2 + self.acceleration[2]**2)))) * 180 / pi

        return accelPolarAngle


    @property
    def accelRoll(self):
    #Roll = arctan(accelY/accelZ)

        roll = np.arctan(self.acceleration[1]/self.acceleration[2]) * 180 / pi

        return roll


    @property
    def accelPitch(self):
    #Pitch = arcsin(accelX/ sqrt(accelX^2 + accelY^2 + accelZ^2)) My sensor is currently oriented with x in the short direction so it seems opposite
        
        pitch = np.arcsin(self.acceleration[0]/
                          (np.sqrt(self.acceleration[0]**2 + self.acceleration[1]**2 + self.acceleration[2]**2))) * 180 / pi

        return pitch


        


        






### TESTING ###
def unitTest():

    testData = {'timeDelta': 250.0, 
                'accelX': 0.099853515625, 
                'accelY': -0.104248046875, 
                'accelZ': 0.9912109375, 
                'gyroX': -4.877862595419847, 
                'gyroY': -0.061068702290076333, 
                'gyroZ': 0.44274809160305345, 
                'temperature': 22.22}

    testPosition = Position()

    testPosition.setMotion(testData)
    print('Acceleration Vector', testPosition.acceleration)
    print('Angular Velocity Vector', testPosition.angularVelocity)

    print(testPosition.accelPolarAngle)




if __name__ == "__main__":
    print("Running Direct")

    unitTest()

