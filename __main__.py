import serial
import time
import dataParse
import motion
import serialManager
import signalProcessing
import csv


comport = serialManager.findPort()

def getData():

        for attempt in range(10):
            try:
                line = MPU6050.readline().decode()

            except UnicodeDecodeError:
                attempt += 1
                continue

            else:
                break

        sensorResponse = dataParse.Response(line)   #Sensor response is parsed into a 2 item tuple with a response type and response value
        sensorResponse.response_handler()

        if sensorResponse.type == 'readings':

            imuData = sensorResponse.value
                     
            filtered_signal = {"timeDelta": imuData['timeDelta'], 
                          "accelX" : accelXLowPass.filterSignal(imuData['accelX']), 
                          "accelY" : accelYLowPass.filterSignal(imuData['accelY']), 
                          "accelZ" : accelZLowPass.filterSignal(imuData['accelZ']),
                          "gyroX" : gyroXLowPass.filterSignal(imuData['gyroX']),
                          "gyroY" : gyroYLowPass.filterSignal(imuData['gyroY']),
                          "gyroZ" : gyroZLowPass.filterSignal(imuData['gyroZ']),
                          "temperature" : imuData['temperature']}
            
            IMUPosition.setMotion(filtered_signal)

            return 'readings' , filtered_signal

        else:

            return 'status' , None
              
def getInclination():
    
    inclination = round(inclinationMovingAverage.movingAverage(IMUPosition.accelPolarAngle),1)

    
    print("Inclination: {0:5} degrees".format(inclination), end='\r')  #end = '/r' prevents the terminal from scrolling
    

with serial.Serial(port = comport, baudrate = 38400, timeout = 2) as MPU6050:  
    
    time.sleep(2) #Allow time for serial connection to open
    IMUPosition = motion.Position()
    
    #Initialize the low pass filters
    accelXLowPass = signalProcessing.LiveFilter(order= 4, cutoff= .05)
    accelYLowPass = signalProcessing.LiveFilter(order= 4, cutoff= .05)
    accelZLowPass = signalProcessing.LiveFilter(order= 4, cutoff= .05)
    gyroXLowPass = signalProcessing.LiveFilter(order= 4, cutoff= .05)
    gyroYLowPass = signalProcessing.LiveFilter(order= 4, cutoff= .05)
    gyroZLowPass = signalProcessing.LiveFilter(order= 4, cutoff= .05)

    inclinationMovingAverage = signalProcessing.LiveFilter(order= 40)
    
    #Send read command to the firmware
    MPU6050.write(b'R')

    fieldnames = ["timeDelta", 
                    "accelX",
                    "accelY", 
                    "accelZ",
                    "gyroX",
                    "gyroY",
                    "gyroZ",
                    "temperature"]
    

    def processingLoop():
        
        with open('IMUdata.csv', 'w', newline='') as csvfile:
            data_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            data_writer.writeheader()

        while  True:    
            
            with open('IMUdata.csv', 'a', newline='') as csvfile:
                data_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                data = getData()            #Gets function return tuple I need to find a way to access the class instead, my context is off
                type = data[0]
                values = data[1]

                if type == 'readings':

                    data_writer.writerow(values)
                    
                    getInclination()
                    #print("Roll: ",IMUPosition.accelRoll," Pitch: ", IMUPosition.accelPitch)
       

    #with open('IMUdata.csv', 'w', newline='') as csvfile:
        #processingLoop(csvfile)

    processingLoop()