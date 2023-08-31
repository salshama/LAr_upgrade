# coding: utf-8

# Importing required packages

import serial

import numpy as np

import time

from datetime import datetime

# Setting up the serial connection

ser  = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)

# We will be reading values from: READ_VIN, READ_VOUT, READ_IIN, and READ_IOUT

# READ_VIN: read-only command has 2 bytes and is formatted in Linear_5s_11s format; 0x88

# READ_VOUT: read-only command has 2 bytes and is formatted in Linear_16u format; 0x8B

# READ_IIN: read-only command has 2 bytes and is formatted in Linear_5s_11s format; 0x89

# READ_IOUT: read-only command has 2 bytes and is formatted in Linear_5s_11s format; 0x8C

# READ_VOUT and READ_IOUT are paged. Set page: 0x00. Pages: 0x00 or 0x01

page_numbers = [0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F']

# Defining a function that converts an "n bit" number

def convert_nbit(str, nbits, tcflag=True):

    n = int(str, 2)
    
    if n > (2**nbits)-1:
    
        print("Not a the required bit number string")
        
        return 0
        
    else:
    
        if tcflag:
        
            if n < 2**(nbits-1):
            
                return n
                
            else:
            
                return (n-2**nbits)
        else:
        
            return n

# Defining a function that reads a string and carries certain conversions

def power_read(string,filenametag="",appendflag=False):

    given_time = datetime.fromtimestamp(time.time())

    if string == "read_vin":
    
        print("\nReading input voltage:\n")
    
        # Reading the value at that register address
        
        ser.write("[0x9E 0x88 [0x9F rr]\n".encode('ascii'))
        
        # Printing the result
            
        li = []
    
        for line in ser.readlines():
        
            if line[:4] == 'READ':
            
                value = line.decode('utf-8').strip()[-2:]
                
                li.append(value)
                
        binary_value = bin(int("0x{}{}".format(li[1],li[0]),16))[2:]
             
        low_11       = binary_value[-11:]
     
        top_5        = binary_value[:5]

        int_low_11 = convert_nbit(low_11,11)
        int_top_5  = convert_nbit(top_5,5)

        new_vin = int_low_11*(2**int_top_5)
         
        print("Input voltage is: ",new_vin," Volts")
        
        with open("input_voltage"+filenametag+".txt",("a" if appendflag else "w")) as file:
			
			    line = str(new_vin)+" "+str(given_time)+"\n"
			    
			    file.write(line)
			    
			    file.close()
        
        return new_vin

    if string == "read_iin":
    
        print("\nReading input current:\n")
    
        # Reading the value at that register address
        
        ser.write("[0x9E 0x89 [0x9F rr]\n".encode('ascii'))
 
        # Printing the result
            
        li = []
    
        for line in ser.readlines():
        
            if line[:4] == 'READ':
            
                value = line.decode('utf-8').strip()[-2:]
                
                li.append(value)
                
        binary_value = bin(int("0x{}{}".format(li[1],li[0]),16))[2:]
             
        low_11       = binary_value[-11:]
             
        top_5        = binary_value[:5]
    
        int_low_11 = convert_nbit(low_11,11)
        int_top_5  = convert_nbit(top_5,5)
    
        new_iin = int_low_11*(2**int_top_5)
                 
        #print("Input current is: ",new_iin," Amps")
        
        with open("input_current"+filenametag+".txt",("a" if appendflag else "w")) as file:
			
			    line = str(new_iin)+" "+str(given_time)+"\n"
			    
			    file.write(line)
			    
			    file.close()
			    
			    print("Input current:",line)
        
        return new_iin
                 
    if string == "read_vout":
    
        N = -12
        
        print("\nReading output voltage:\n")
        
        # Setting the page number given a register
        
        for number in page_numbers:
         
            ser.write("[0x9E 0x00 0x"+str(number)+"]\n".encode('ascii'))
             
            # Delaying by 0.2 seconds
             
            time.sleep(0.2)
             
            # Reading the value at that register address
             
            ser.write("[0x9E 0x8B [0x9F rr]\n".encode('ascii'))
             
            # Printing the result
             
            li = []
             
            for line in ser.readlines():
             
                if line[:4] == 'READ':

                    value = line.decode('utf-8').strip()[-2:]
                     
                    #print(value)
                     
                    li.append(value)
                     
                    # Voltage = Y * 2^N
                     
            register_value = int("0x{}{}".format(li[1],li[0]),16)
                
            #print(register_value)
                     
            new_vout = register_value*(2**N)
             
            #print("Output voltage is: ",new_vout," Volts")
            
            open_option = "w" if ((not appendflag) and (number == page_numbers[0])) else "a"
            
            with open("output_voltage"+filenametag+".txt",open_option) as file:
			
			    line = str(number)+" "+str(new_vout)+" "+str(given_time)+"\n"
			    
			    file.write(line)
			    
			    file.close()
			    
			    print("Output voltage: ",line)
            
        return new_vout
            
    if string == "read_iout":
    
        print("\nReading output current:\n")
        
        # Setting the page number given a register
        
        for number in page_numbers:
        
            ser.write("[0x9E 0x00 0x0"+str(number)+"]\n".encode('ascii'))
        
            # Delaying by 0.2 seconds
        
            time.sleep(0.2)
        
            # Reading the value at that register address
        
            ser.write("[0x9E 0x8C [0x9F rr]\n".encode('ascii'))
        
            # Printing the result
            
            li = []
        
            for line in ser.readlines():
            
                if line[:4] == 'READ':
                    
                    value  = line.decode('utf-8').strip()[-2:]
                    
                    li.append(value)
                                        
                    # X = Y * 2^N
                    
            binary_value = bin(int("0x{}{}".format(li[1],li[0]),16))[2:]
                     
            low_11       = binary_value[-11:]
                     
            top_5        = binary_value[:5]
            
            int_low_11 = convert_nbit(low_11,11)
            int_top_5  = convert_nbit(top_5,5)
            
            new_iout = int_low_11*(2**int_top_5)
                     
            #print("Output current is: ",new_iout," Amps")
            
            open_option = "w" if ((not appendflag) and (number == page_numbers[0])) else "a"
            
            with open("output_current"+filenametag+".txt",open_option) as file:
			
			    line = str(number)+" "+str(new_iout)+" "+str(given_time)+"\n"
			    
			    file.write(line)
			    
			    file.close()
			    
			    print("Output current: ",line)
            
        return new_iout

# Calculating input and output powers

power_read('read_vin',appendflag=True)
power_read('read_vout',appendflag=True)
power_read('read_iin',appendflag=True)
power_read("read_iout",appendflag=True)

power_in  = power_read('read_vin',appendflag=True) * power_read('read_iin',appendflag=True)
power_out = power_read('read_vout',appendflag=True) * power_read('read_iout',appendflag=True)

print("The input power is: ",power_in," Watts")
print("The output power is: ",power_out," Watts")