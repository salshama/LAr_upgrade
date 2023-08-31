#!/usr/bin/env python3

"""Class for serial communication with lpGBT using  buspirate.

This class is for a general write address and read address (given a device address).
It could be used for any general device.

It's also coded to write to the buspirate as
[0x<device_address> 0x<register_address> 0x<data>]
where 0x<register_address> is a single byte in hexadecimal format

The method "write_register" performs this. The write method can also be used to "set" a
page using 0x00, for example, to a specific page number, 0x01 for example. The read method
can then be used to read the value off that specific page number for that register.

It also reads data using this buspirate command:
[0x<device_register> 0x<register_address> [0x<read_address> r]
where 0x<register_address> is a single byte in hexadecimal format as before.

It currently only reads out one byte.

The method "read_register" performs this

"""

import re
import sys
from time import sleep
from typing import List, Optional

import serial
import serial.tools.list_ports
from serial.serialutil import SerialException, SerialTimeoutException

#have a for loop that goes over page numbers
#set page number, read current and then voltage
#next loop comes around, and reads the next readings

# Setting up the I2C_Adapter class

class I2C_Adapter():

    """Write registers to lpGBT using buspirate"""
    
    def __init__(self, serial_device: str):
    
        self._device = serial_device
        
        try:
            self._conn = serial.Serial(self._device, 115200, timeout=0.1)
        
        except SerialException as inst:
            print(STR_ERR + "Connection to serial device failed:")
            print(inst.strerror)
            sys.exit(1)

        # buspirate setup
        self.send("#") # reset bus pirate (slow, maybe not needed)
        self.send("m") # change mode (goal is to get away from HiZ)
        self.send("4") # 4 is I2C
        self.send("3") # 3 is 100kHz
        self.send("W") # turn power supply to ON. Lowercase w for OFF.
        
        self._conn.timeout      = 0.25
        self._conn.write_timout = 1

    def write_register(self, device: int, register: int, value: int, check: bool = True) -> None:
        
        """Sets value of the register `register` to `value`."""
        
        if value < 0:
            print(STR_ERR + f"Can't write {value} to register 0x{register:04X}")
            return
        
        device_hex       = f"{device:02X}"
        device_int_write = (device << 1)
        device_hex_write = f"{device_int_write:02X}"
        
        # Convert the integer register address to hexadecimal
        register_hex = f"{register:02X}"

        # Convert the integer data to hexadecimal
        value_hex = f"{value:02X}"

        # Format the command
        command = "[0x"+device_hex_write[0:2]+" 0x"+register_hex[0:2]+" 0x"+value_hex+"]"
        print("Command sent to buspirate: "+command)

        result = self.send(command)
        print("Response from buspirate: ")
        print(result)

        # Check that the write command wrote correctly by reading it back
        if check:
            for line in result:
                if "NACK" in result:
                    err_str = "I2C adapter didn't complete operation successfully."
                    raise Exception(err_str)


            read_value = self.read_register(device,register)

            if read_value != value:
                err_str = "Readback false, " \
                           f"wrote 0x{value:02X} (0b{value:08b}) " \
                           f"to register 0x{register:04X}, " \
                           f"read 0x{read_value:02X} (0b{read_value:08b})"
                raise Exception(err_str)

    def read_register(self, device: int, register: int, nbyte = 1, orderflag=False) -> int:
        
        """Returns value of the register `register`."""
        
        rbyte = ""
        for byte in range(nbyte):
            rbyte = rbyte + "r"
        
        device_int_read  = (device << 1) + 1
        device_int_write = (device << 1)
        device_hex       = f"{device:02X}"
        device_hex_read  = f"{device_int_read:02X}"
        device_hex_write = f"{device_int_write:02X}"
        
        # convert the integer register address to hexadecimal
        command = f"{register:02X}"
        print("Register address converted to hex: "+command)
        
        command_bp = "[0x"+device_hex_write[0:2]+" 0x"+command[0:2]+" [0x"+device_hex_read[0:2]+" "+str(rbyte)+"]"
        print("Command sent to buspirate: "+command_bp)
        message = self.send(command_bp)
        print("Response from buspirate: ")
        print(message)
        num=""

        # Parse output
        li = []
        for line in message:
        
            if "READ:  ACK" in line:
                print(line)
                li.append(line.replace("READ:  ACK 0x",""))
                    
            elif "READ" in line:
                print(line)
                li.append(line.replace("READ: 0x",""))
        
        if nbyte == 2: # can be generalized for arbitrary numbers
        
            if orderflag==True:
                num = "0x"+li[1]+li[0]
            else:
                num = "0x"+li[0]+li[1]
                
        else:
            num = "0x"+li[0]
            
        print("ORDER: ",num)

        # return the result converted to integer (assuming unsigned!)
        return int(num, base=16)

    # This method does the actual communication with the buspirate
    def send(self, command: str) -> str:
    
        """Sends a single command over serial port and returns the of
        reply.

        `command` must not include line endings. Line endings are not included
        in the return value as well.
        """
        
        try:
            self._conn.write(str(command+'\n').encode('ascii')) # send our command
            result = []
            for line in self._conn.readlines(): # while there's a response
                result.append(line.decode('utf-8').strip())

        except SerialTimeoutException as inst:
            print(STR_ERR + "Connection timed out")
            print(inst.strerror)
            sys.exit(1)

        return result

    def __del__(self):
        if hasattr(self, "_conn"):
            print("Closed serial connection")
            self._conn.close()