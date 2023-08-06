
import telnetGPIO.telnetGPIO as tg
import time
import sys

if len(sys.argv) < 3:
    raise Exception("Not enough input arguments")



conn = tg.telnetGPIOHandler("192.168.1.148", 8883, "telnetA", "192.168.1.171")
conn.initializeConn()

while(1 == 1):
    print(conn.newState)
    conn.read()
    conn.updateBinary()

    if(conn.newState != conn.oldState):
        conn.writeChange()

    time.sleep(.1)
