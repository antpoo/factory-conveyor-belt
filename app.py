# importing required dependencies
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_apscheduler import APScheduler
from time import sleep
from flask_socketio import SocketIO, emit
import RPi.GPIO as GPIO
import gpiozero
import serial

# creating flask objects
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['MQTT_BROKER_URL'] = '192.168.1.25'  # Change this to the broker address if needed
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_USERNAME'] = ""
app.config['MQTT_PASSWORD'] = ""
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_CLEAN_SESSION'] = True


socketio = SocketIO(app)
mqtt = Mqtt(app)

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


# MQTT event handlers
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    for i in range(1, 7):
        mqtt.subscribe(COMPONENTS[i])

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
	topic = message.topic
	msg = message.payload.decode('utf-8').strip()

	print(topic, msg, "test")

	if msg == "OK":
		status[topic] = 1
		socketio.emit(topic, {"status": "ready to begin"})

	elif msg == "START":
		status[topic] = 0.5
		socketio.emit(topic, {"status": "running"})

	elif msg == "ERROR":
		status[topic] = -1
		socketio.emit(topic, {"status": "error!"})



# create serial connection for Arduino
ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
ser.reset_input_buffer()

# method to move the conveyor
def move_conveyor():
	print("test")
	ser.write(b"start\n")
	
	mqtt.publish("conveyor", payload="begin")

# threading method to update status of conveyor
def check_conveyor():
	if ser.in_waiting > 0:
		message = ser.readline().strip()
		print(message)
		# update its status
		if message == "running":
			status["conveyor"] = 1
			socketio.emit("conveyor", {"status": "running"})
		elif message == "stopped":
			status["conveyor"] = 0
			socketio.emit("conveyor", {"status": "stopped"})

# threading method to constantly check if all components are good
def check_all():

	print(status)

	for i in range(1, 7):
		msg = status[COMPONENTS[i]]
		if msg == 1:
			socketio.emit(COMPONENTS[i], {"status": "ready to begin"})

		elif msg == 0.5:
			socketio.emit(COMPONENTS[i], {"status": "running"})

		elif msg == -1:
			socketio.emit(COMPONENTS[i], {"status": "error!"})

	# assume everything is good
	all_good = 1
	# if even a single one is not good then they are not good (AND with them to check)
	for i in range(1, 7):
		all_good &= status[COMPONENTS[i]] == 1
	
	# if everything is still good, then run the stepper motor/conveyor
	if all_good:
		# set everything to 0.5 as it's a new cycle
		for i in range(1, 7):
			status[COMPONENTS[i]] = 0.5

		# move the conveyor
		move_conveyor()


# main page
@app.route("/")
def index():
	# move_conveyor()
	return render_template("index.html")


# main app 
if __name__ == '__main__':

	# create the threading scheduler
	scheduler = APScheduler()
	# adding the check methods to the threader
	scheduler.add_job(func=check_all, trigger="interval", id="job", seconds=1)
	scheduler.add_job(func=check_conveyor, trigger="interval", id="job1", seconds=0.01, max_instances=10000)
	# start the threader
	scheduler.start()


	# tell components to start

	
    # start the Flask app
	app.run(host = "0.0.0.0", port=5000)

	