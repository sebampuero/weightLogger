# code modified, tweaked and tailored from code by bertwert
# on RPi forum thread topic 91796
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
GPIO.setmode(GPIO.BCM)
#Sensortyp und GPIO festlegen
sensor = Adafruit_DHT.DHT22
gpio = 21

# GPIO ports for the 7seg pins
segments =  (11,4,23,8,7,10,18,25)
# 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline

for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 1)

# GPIO ports for the digit 0-3 pins
digits = (22,27,17,24)
# 7seg_digit_pins (12,9,8,6) digits 0-3 respectively

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 0)

num = {' ':(1,1,1,1,1,1,1),
    '0':(0,0,0,0,0,0,1),
    '1':(1,0,0,1,1,1,1),
    '2':(0,0,1,0,0,1,0),
    '3':(0,0,0,0,1,1,0),
    '4':(1,0,0,1,1,0,0),
    '5':(0,1,0,0,1,0,0),
    '6':(0,1,0,0,0,0,0),
    '7':(0,0,0,1,1,1,1),
    '8':(0,0,0,0,0,0,0),
    '9':(0,0,0,0,1,0,0),
    'c':(0,1,1,0,0,0,1),
    'h':(1,0,0,1,0,0,0)}

try:
    flag = True
    while True:
        i = 0
        outside_t = 1
        inside_t = 0
        while i < 3000:
            if flag:
            # read outside temp
               #n = (str(chumidity).replace(".","")[:3], "hum")
              # n = ("245", "hum")
            else:
                # read inside temp
              #n = (str(ctemperature).replace(".","")[:3], "tem")
              # n = ("222", "tem")
            s = str(n[0]).rjust(3)
            for digit in range(4):
                for loop in range(0,7):
                    if digit != 3:
                        GPIO.output(segments[loop], num[s[digit]][loop])
                    if digit ==1:   #imprimir el punto decimal en el digito 2
                        GPIO.output(25, 0)  #encender
                    else:
                        GPIO.output(25,1) #apagar los demas
                    if digit == 3:
                        GPIO.output(segments[loop], num['c'][loop])
                GPIO.output(digits[digit], 1)
                time.sleep(0.001)
                GPIO.output(digits[digit], 0)
            i += 1
            if outside and i == 2999:
                flag = False
            elif inside == "tem" and i == 2999:
                flag = True
finally:
    GPIO.cleanup()
