import pwmlight
import time

light = pwmlight.pwmlight(18, 50000, 1000000, 'test')

light.setBrightness(100)
light.turnOn()

time.sleep(1)

light.setBrightness(20)

time.sleep(1)

light.turnOff()

#while 1:
#       for i in range(0, 50):
#               light.setBrightness(i)
#               time.sleep(.01)
#
#       for i in range(0, 50):
#               light.setBrightness(50 - i)
#               time.sleep(.01)

#light.debug(100000)

#light.turnOff()


#light.debug(100000)

#light.turnOff()

#print(str(light.brightness))

#print(str(light.getState()))




