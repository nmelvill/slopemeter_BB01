
class Response:

    accelSensitivity = 16384   
    gyroSensitivity = 131

    def __init__(self,serial_line):
        self.line = serial_line
        self.type = None
        self.value = None
        self.responselist = None

        self.parseResponse()
    
    def parseData(self,dataLine):

        dataList = dataLine.split(',')

        timeDelta = float(dataList[0])
        accelX = self.convertRawAcceleration(float(dataList[1]))
        accelY = self.convertRawAcceleration(float(dataList[2]))
        accelZ = self.convertRawAcceleration(float(dataList[3]))
        gyroX = self.convertRawRotation(float(dataList [4]))
        gyroY = self.convertRawRotation(float(dataList[5]))
        gyroZ = self.convertRawRotation(float(dataList[6]))
        temperature = float(dataList[7])

        dataDictionary = {"timeDelta": timeDelta, 
                          "accelX" : accelX, 
                          "accelY" : accelY, 
                          "accelZ" : accelZ,
                          "gyroX" : gyroX,
                          "gyroY" : gyroY,
                          "gyroZ" : gyroZ,
                          "temperature" : temperature}


        return dataDictionary


    def convertRawAcceleration(self, rawAcceleration):

        ##STORE CONVERSION VALUE IN A SETTINGS FILE/DB
        acceleration = rawAcceleration / Response.accelSensitivity

        return acceleration


    def convertRawRotation(self, rawRotation):

        ##STORE CONVERSION VALUE IN A SETTINGS FILE/DB
        angularVelocity = rawRotation / Response.gyroSensitivity

        return angularVelocity


    def parseResponse(self):
    #Takes a line from the serial monitor and parses it based on a colon and returns response type and value

        response_list = self.line.split(':')
        self.type = response_list[0]

        if len(response_list) > 1:
            self.value = response_list[1]
        else:
            self.value = None



    def routeResponse(self):
    #Performs the desired function on the response value based on the response type

        match self.type:

            case "readings":
                self.value = self.parseData(self.value)
            case "status":
                self.value = self.value
            case _:
                return "Response type can't be handled"  #ADD ERROR HERE??


    def response_handler(self):

        return self.routeResponse()
