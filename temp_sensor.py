# coding: utf-8

#Importing required packages

import serial

import time

from datetime import datetime

import numpy as np

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)

# To write to the device, use:

# ser.write("yourmessage".endcode('ascii'))

# To read from the device, use:

# for line in ser.readlines():
#    print(line.decode('utf-8').strip())

# Creates a file that queries temperature values at time intervals

# This function takes in a register, reads the temperature with the timestamp
# and converts it to decimal format

def read_temp_value(register):

	ser.write("[0x98 "+str(register)+" [0x99 r]\n".encode('ascii'))
	
	for line in ser.readlines():
	
	    if line[:4] == 'READ':
	    
	        print(line.decode('utf-8').strip())
	        
	        temp_val  = int(line[8:],16)
	        
	        temp_time = datetime.fromtimestamp(time.time())
				    
		if "0x{:02x}".format(register) == "0x00":
	
			print("The local temperature is {} in degrees Celsius".format(temp_val))
			
			print("The time is {} in seconds".format(temp_time))
			
			with open("query_local_temp.txt","a") as file:
			
			    line = str(temp_val)+" "+str(temp_time)+"\n"
			    
			    file.write(line)
			    
			    file.close()
			    
			    local_temp = temp_val
			    
			    local_time = temp_time
			    
		if "0x{:02x}".format(register) == "0x01":
	
			print("The remote temperature is {} in degrees Celsius".format(temp_val))
			
			print("The time is {} in seconds".format(temp_time))
			
			with open("query_remote_temp.txt","a") as file:
			
			    line = str(temp_val)+" "+str(temp_time)+"\n"
			    
			    file.write(line)
			    
			    file.close()
			    
			    remote_temp = temp_val
			    
			    remote_time = temp_time
			    
read_temp_value(0x00) # Local temperature of sensor
read_temp_value(0x01) # Remote temperature of entire board