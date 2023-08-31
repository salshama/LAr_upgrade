#Importing required packages

import serial

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)

# To write to the device, use:

#ser.write("yourmessage".endcode('ascii'))

# To read from the device, use:

#for line in ser.readlines():
#    print(line.decode('utf-8').strip())

print("Resetting the buspirate")

# The '#' Command resets the buspirate
ser.write("#\n".encode('ascii'))
for line in ser.readlines():
    print(line.decode('utf-8').strip())

print("Requesting the buspirate menu")

# The 'm' command opens the buspirate menu
ser.write("m\n".encode('ascii'))
for line in ser.readlines():
    print(line.decode('utf-8').strip())

print("Choosing option 4")

# Choose option '4' from the above menu
ser.write("4\n".encode('ascii'))
for line in ser.readlines():
    print(line.decode('utf-8').strip())


print("Choosing option 3")

# Now set the speed to 100kHz
ser.write("3\n".encode('ascii'))
for line in ser.readlines():
    print(line.decode('utf-8').strip())

print("Turning on buspirate power supply")

# Finally, turn the powersupply to ON
ser.write("W\n".encode('ascii'))
for line in ser.readlines():
    print(line.decode('utf-8').strip())
    
print("Printing addresses list")

# Pressing (1) on the buspirate will show a list of all devices in the I2C chain
ser.write("(1)\n".encode('ascii'))
for line in ser.readlines():
    print(line.decode('utf-8').strip())
    
print("Bringing up the macro menu")

# Pressing (0) will bring up the menu
ser.write("(0)\n".encode('ascii'))
for line in ser.readlines():
    print(line.decode('utf-8').strip())
    
# Creating a function to read the value at a given register address
def check_read_value(register):
    
    ser.write("[0xE4 0x"+str(register)+" 0x00 [0xE5 r]\n".encode('ascii'))
    
    for line in ser.readlines():

        if line[:4] == 'READ':

            print(line.decode('utf-8').strip())
        
# Creating a function to write to the register a given value
def check_write_value(register,hexdec):
    
    ser.write("[0xE4 0x"+str(register)+" 0x00 0x"+str(hexdec)+"]\n".encode('ascii'))
    
    for line in ser.readlines():

        if line[:11] == 'WRITE: 0x'+str(hexdec):

            print(line.decode('utf-8').strip()[:-3])
        
# Calling functions to check if they work
check_write_value(34,51)
check_read_value(34)