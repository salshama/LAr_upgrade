# coding: utf-8

# Importing required packages

import serial

import numpy as np

import time

# Setting up the serial connection

ser  = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)

# Creating a function that is passed file.txt to read the registers and breaks them down
# into page numbers, hexadecimal values, and register address

def clock_read(filename):

	with open(filename, 'r') as file:
	
		for lines in file.readlines():

			register             = str(lines.rstrip())[2:6]
			hexdec               = str(lines.rstrip())[9:]
			page_number          = register[0:2]
			register_address     = register[2:4]
			
			# Setting the page number given a register
			
			ser.write("[0xE8 0x01 0x"+page_number+"]\n".encode('ascii'))
			
			# Delaying by 0.2 seconds
			
			time.sleep(0.2)
			
			# Reading the value at that register address
			
			ser.write("[0xE8 0x"+register_address+" [0xE9 r]\n".encode('ascii'))
			
			# Printing the result
			
			for line in ser.readlines():
		
				if line[:4] == 'READ':
			
					print(line.decode('utf-8').strip())
            
# Creating a function that is passed file.txt to write a hexadecimal value to the
# registers and read the value obtained

def clock_write(filename):

	with open(filename, 'r') as file:

		for lines in file.readlines():
	
			register             = str(lines.rstrip())[2:6]
			hexdec               = str(lines.rstrip())[9:]
			page_number          = register[0:2]
			register_address     = register[2:4]
			
			# Setting the page number given a register
			
			ser.write("[0xE8 0x01 0x"+page_number+"]\n".encode('ascii'))
			
			# Delaying by 0.2 seconds
			
			time.sleep(0.2)
			
			# Writing to a hexadecimal value to the register address from file
			
			ser.write("[0xE8 0x"+register_address+" 0x"+hexdec+"]\n".encode('ascii'))
			
			# Printing the result

			for line in ser.readlines():
				
				if line[:11] == 'WRITE: 0x'+register:
			
					print(line.decode('utf-8').strip()[:-3])
             
# Calling functions to check if they work by passing a .txt file

clock_write('s10DevkitClocks_modified.txt')
clock_read('s10DevkitClocks_modified.txt')