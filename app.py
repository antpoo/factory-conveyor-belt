# importing required dependencies
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from time import sleep
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# creating flask objects
app = Flask(__name__)

# a list to store each component's name
COMPONENTS = ["conveyor", "measuring", "mixing", "baking", "topping", "packaging", "cleaning"]

# a dictionary to store each component's status, 1 means good, 0 means bad
status = {
	"conveyor": 0,
	"measuring": 0,
	"mixing": 0,
	"baking": 0,
	"topping": 0,
	"packaging": 0,
	"cleaning": 0
}

# creating mqtt object
m_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "andrew_pi")

# method for connecting and subscribing to each component
def on_connect(client, userdata, flags, reason_code, properties):
	print(f"Connected with result code {reason_code}")

	for i in range(1, 7):
		client.subscribe(COMPONENTS[i])


# method for receiving MQTT messages
def on_message(client, userdata, message):

	# get the topic (i.e. who sent it)
	topic = message.topic

	# get the message itself
	msg = message.payload.decode("utf-8").strip()

	# if the component is okay, set its status to 1
	if msg == "OK":
		status[topic] = 1
	# if the component started, set to 0.5
	elif msg == "START":
		status[topic] = 0.5
	# if the component has an error, set to -1
	elif msg == "ERROR":
		status[topic] = -1
	

# set its connection and message callback functions
m_client.on_connect = on_connect
m_client.on_message = on_message

# connect to broker
m_client.connect("localhost")

# set up GPIO pins for the motor
STEP_PIN = 5
MS1_PIN = 6
MS2_PIN = 13
MS3_PIN = 19

GPIO.setmode(GPIO.BCM)

GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(MS1_PIN, GPIO.OUT)
GPIO.setup(MS2_PIN, GPIO.OUT)
GPIO.setup(MS3_PIN, GPIO.OUT)


# method to move the conveyor
def move_conveyor():
	pass

# threading method to constantly check if all components are good
def check_all():

	# assume everything is good
	all_good = 1
	# if even a single one is not good then they are not good (AND with them to check)
	for i in range(1, 7):
		all_good &= status[COMPONENTS[i]] == 1
	
	# if everything is still good, then run the stepper motor/conveyor
	if all_good:
		# set everything to 0 as it's a new cycle
		for i in range(1, 7):
			status[COMPONENTS[i]] = 0

		# move the conveyor
		move_conveyor()


# main page
@app.route("/")
def index():
	return render_template("index.html")


# main app 
if __name__ == '__main__':

	# create the threading scheduler
	scheduler = APScheduler()
	# adding the check method to the threader
	scheduler.add_job(func=check_all, trigger="interval", id="job", seconds=1)
	# start the threader
	scheduler.start()
	
    # start the Flask app
	app.run(host = "0.0.0.0", port=5000)