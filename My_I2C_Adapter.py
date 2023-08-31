#!/usr/bin/env python3

# Importing I2C_Adapter class
import I2C_Adapter

# Setting serial connection with buspirate
buspirate = I2C_Adapter.I2C_Adapter("/dev/ttyUSB0")

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

# Temperature sensor
print("\nTemperature of sensor: \n")
print(buspirate.read_register(76,0))

print("\nTemperature of board: \n")
print(buspirate.read_register(76,1))

# Clock chip
def clock_write(filename):

	with open(filename, 'r') as file:

		for lines in file.readlines():
			register         = str(lines.rstrip())[2:6]
			page_number      = int(register[0:2],16)
			register_address = int(register[2:4],16)
			 			
	clock_data_set   = buspirate.write_register(116, 1, page_number)
	clock_data_write = buspirate.write_register(116, page_number, register_address)
	
	return clock_data_write

print("\nClock chip: \n")
print(clock_write('s10DevkitClocks_modified.txt'))

# Power regulator
print("\nPower regulator: \n")

print("\nInput voltage: \n")
vin            = buspirate.read_register(79,136, nbyte=2, orderflag=True) # no page number
vin_bin        = bin(vin)[2:]
vin_low_11     = vin_bin[-11:]
vin_top_5      = vin_bin[:5]
vin_int_low_11 = convert_nbit(vin_low_11,11)
vin_int_top_5  = convert_nbit(vin_top_5,5)
new_vin        = vin_int_low_11*(2**vin_int_top_5)

print("\nInput voltage is: ",new_vin," Volts\n")

print("\nInput current: \n")
iin            = buspirate.read_register(79,137, nbyte=2, orderflag=True) # no page number
iin_bin        = bin(iin)[2:]
iin_low_11     = iin_bin[-11:]
iin_top_5      = iin_bin[:5]
iin_int_low_11 = convert_nbit(iin_low_11,11)
iin_int_top_5  = convert_nbit(iin_top_5,5)
new_iin        = iin_int_low_11*(2**iin_int_top_5)

print("\nInput current is: ",new_iin," Amps\n")

print("\nOutput voltage: \n")
N        = -12
vout_w   = buspirate.write_register(79, 0, 1) # set page number
vout     = buspirate.read_register(79, 139, nbyte=2, orderflag=True) # set page number
new_vout = vout*(2**N)

print("\nOutput voltage is: ",new_vout," Volts\n")

print("\nOutput current: \n")
iout_w          = buspirate.write_register(79, 0, 1) # set page number
iout            = buspirate.read_register(79, 140, nbyte=2,orderflag=True) # set page number
iout_bin        = bin(iout)[2:]
iout_low_11     = iout_bin[-11:]
iout_top_5      = iout_bin[:5]
iout_int_low_11 = convert_nbit(iout_low_11,11)
iout_int_top_5  = convert_nbit(iout_top_5,5)
new_iout        = iout_int_low_11*(2**iout_int_top_5)

print("\nOutput current is: ",new_iout," Amps\n")