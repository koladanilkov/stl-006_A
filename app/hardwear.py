import ubinascii
import machine
from machine import Pin, PWM


koef_brightnes = 1
power = 100
nowPower = 100
p13 = Pin(13, Pin.OUT)   
p13.off()                
pwm17 = PWM(Pin(17), freq=1000, duty=power*10)
client_id = ubinascii.hexlify(machine.unique_id())
def setPower(value):
    global power
    power = value
    
def setKoefBrightnes(value):
    global koef_brightnes
    koef_brightnes = value
    
def getPower():
    return power
    
def brightnesCorecting():
    global power, nowPower, pwm17, koef_brightnes
    if nowPower < power-koef_brightnes or nowPower > power+koef_brightnes:
        if nowPower > power:
            nowPower -= koef_brightnes
            pwm17.duty(nowPower*10)
        
        if nowPower < power:
            nowPower += koef_brightnes
            pwm17.duty(nowPower*10)
        print('%s \n' % (nowPower))
        

