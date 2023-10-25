# Attempt to grab the FTDI device
import ftd2xx as ftd; # Communicating the the UM232R FTDI chip for triggering
d = ftd.open(0);
print(d.getDeviceInfo());
OP = 0x07;           # Bit mask for output D0
d.setBitMode(OP, 1);  # Set pin as output, and async bitbang mode
    
state = 0x07
d.write(str(state));      # Init state: 0 0 1
print("sent high");

input();

state = 0x00
d.write(str(state));      # Init state: 0 0 1
print("sent low");

input();

state = 0x07
d.write(str(state));      # Init state: 0 0 1
print("sent high");

input();

state = 0x00
d.write(str(state));      # Init state: 0 0 1
print("sent low");


input();

d.close();