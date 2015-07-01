#!/usr/bin/env python
 
import sys, time
from datetime import datetime
from daemon import Daemon

import eSSP
import time

# k = eSSP.eSSP('/dev/tty.usbmodemfa131')
k = eSSP.eSSP('/dev/ttyACM0')
# print k.sync()
# print k.serial_number()
# print k.enable()
# print k.bulb_on()
# print k.bulb_off()
# print k.enable_higher_protocol()
# print k.poll()
# print k.set_inhibits('0xFF', '0xFF')
# print k.set_inhibits(k.easy_inhibit([1, 0, 1]), '0x00')
# print k.unit_data()
# print k.setup_request();
# k.disable();
# k.reset();
# print k.channel_security();
# print k.channel_values();
# print k.channel_reteach();

print k.sync()
print k.enable_higher_protocol()
# Original
print k.set_inhibits(k.easy_inhibit([1, 0, 1]), '0x00')
# print k.set_inhibits(k.easy_inhibit([0, 1, 1, 1]), '0x00')
print k.enable()
var = 1
i = 0
cc = 0
# Bill <--> CHANNEL
bills = [1,5,10,20]

class MyDaemon(Daemon):
                
        def run(self):
                i = 0
                bills = [1,5,10,20]
                print "***************************"
                print var
                while True:
                        poll = k.poll()
                        waiting = "Waiting..."
                        # print poll
                        # print waiting

                        if len(poll) > 1:
                                # print poll
                                if len(poll[1]) == 2:
                                        # Try to make this so it displays the reason for the rejection.
                                        
                                        # if poll[1][0] == '0xef':
                                        #         if poll[1][1] == 1 or poll[1][1] == 2 or poll[1][1] == 3:
                                        #                 print "Hold for processing..." 
                                        #                 while i < 3:
                                        #                         k.hold()
                                        #                         # print "Hold " + str(i)
                                        #                         time.sleep(0.5)

                                        #                         i += 1
                                        if poll[1][0] == '0xee':
                                                # print "Credit on Channel " + str(poll[1][1])
                                                rn = datetime.now()
                                                print "Accepted $%s on %s-%s-%s at %s:%s" % ( str(bills[poll[1][1] - 1 ]), rn.month, rn.day, rn.year, rn.hour, rn.minute )
                                                i = 0
                                                
                        time.sleep(0.5)

 
if __name__ == "__main__":
        daemon = MyDaemon('/tmp/accepting-bills.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)
