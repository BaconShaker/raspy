#!/envs/bills/bin/python

# This is the main script for the laundry room program. 

# Start the bill acceptor daemon.

# Start RFID daemon. 

# Start washer daemon. 

# Start dryer daemon.

# On card swipe at STATION:
# 	Decode stored information. 
# 	Verify it matches what we have. 
# 	If it does, 
# 		Add the value
# 	Else
# 		Don't add the value?

# On card sipe at washer[i]:
# 	

from evdev import InputDevice, list_devices

devices = [InputDevice(fn) for fn in list_devices()]

for dev in devices:
	print(dev.fn, dev.name, dev.phys)
