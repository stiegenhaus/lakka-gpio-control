import sys
sys.path.append('/storage/lib/')
import RPi.GPIO as GPIO
import os
import time
from multiprocessing import Process

#initialize pins
poweroffPin = 26
resetPin = 21
ejectPin = 20

#initialize GPIO settings
def init():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(poweroffPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(resetPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(ejectPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setwarnings(False)

def poweroff():
  oldState = True
  while True:
    GPIO.wait_for_edge(poweroffPin, GPIO.FALLING)

    state = GPIO.input(poweroffPin)
    if state != oldState and state == False:

      # print 'poweroff'
      os.system("shutdown -h now")
      time.sleep(1)
    

def reset():
  oldState = True
  while True:
    GPIO.wait_for_edge(resetPin, GPIO.FALLING)

    state = GPIO.input(resetPin)
    if state != oldState and state == False:

      # print 'reset'
      os.system("pkill retroarch")
      time.sleep(1)
    


def eject():
  oldState = True
  while True:
    GPIO.wait_for_edge(ejectPin, GPIO.FALLING)

    state = GPIO.input(ejectPin)
    if state != oldState and state == False:

      # print 'eject' 
      os.system("shutdown -r now")
      time.sleep(1)
    


if __name__ == "__main__":
  #initialize GPIO settings
  init()
  #create a multiprocessing.Process instance for each function to enable parallelism 
  poweroffProcess = Process(target = poweroff)
  poweroffProcess.start()
  resetProcess = Process(target = reset)
  resetProcess.start()
  ejectProcess = Process(target = eject)
  ejectProcess.start()

  poweroffProcess.join()
  resetProcess.join()
  ejectProcess.join()

  GPIO.cleanup()