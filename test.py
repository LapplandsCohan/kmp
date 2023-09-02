import ipaddress
from kmp import *
from time import sleep

HOST = ipaddress.ip_address('192.168.1.91')
myHeater = kmp.KMPHeater(HOST)
print(myHeater.readData())
print(myHeater.get_targetTemp())
#myHeater.power_toggle()
#myHeater.temperature_down()
#myHeater.set_temperature(10)
#print("Sleeping…")
#sleep(5)
#myHeater.temperature_up()
#myHeater.power_toggle()
#myHeater.set_temperature(17)