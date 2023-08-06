import lanrelay as ar
import time

rl1 = ar.EightChanRelay("192.168.1.166", 1234, 8)

for relay in rl1.relays:
    relay.turnOn()
    print(relay.getStatus())
    time.sleep(.01)
    relay.turnOff()
    print(relay.getStatus())
