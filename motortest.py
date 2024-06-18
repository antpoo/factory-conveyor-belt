import gpiozero
import RPi.GPIO as GPIO
from time import sleep

STEP_PIN = gpiozero.OutputDevice(27)

STP_PIN = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(STP_PIN, GPIO.OUT)

STEPS = 200

# method to move the conveyor
def move_conveyor():
	for _ in range(STEPS):
		# STEP_PIN.on()
		# sleep(0.002)
		# STEP_PIN.off()
		# sleep(0.002)

		GPIO.output(STP_PIN, 1)
		sleep(0.002)
		GPIO.output(STP_PIN, 0)
		sleep(0.002)

move_conveyor()
GPIO.cleanup()