import serial.tools.list_ports

def findPort():
#Finds the correct com port based on the VID : PID of the desired device

    vidPid = '1A86:7523'

    #Creates a regular expressoin to look for the VID : PID of the device.
    regex = '(USB VID:PID={})'.format(vidPid)
    
    #list_ports.grep finds a port using a regular expression that has the VID : PID listed above and returns a generator
    #next takes the next value in the generator, there should only ever be one item in the generator since VID : PID are unique?
    port = next(serial.tools.list_ports.grep(regex))        

    return port.device

