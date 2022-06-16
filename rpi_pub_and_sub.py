"""EE 250L Lab 04 Starter Code

Team Members: Rachel Anderson
Repo Link: git@github.com:usc-ee250-fall2021/lab05-rachel5.git

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import sys
sys.path.append('../../Software/Python/')
sys.path.append('../../Software/Python/grove_rgb_lcd')
from grovepi import *
from grove_rgb_lcd import *

#LED callback - turns LED on or off accordingly
def led_callback(client, userdata, message):
    message_str = message.payload.decode("utf-8","strict")
    if message_str == "LED_ON":
        digitalWrite(4,1)     # Send HIGH to switch on LED
    elif message_str == "LED_OFF":
        digitalWrite(4,0)     # Send LOW to switch off LED
    else:
        print("ERROR")

#LCD callback - prints "w", "a", "s", or "d" to LCD depending on which key was pressed
def lcd_callback(client, userdata, message):
    setText_norefresh(message.payload.decode("utf-8", "strict"))

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("rachelan/led")
    client.message_callback_add("rachelan/led", led_callback)

    client.subscribe("rachelan/lcd")
    client.message_callback_add("rachelan/lcd", lcd_callback)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    set_bus("RPI_1")        #set I2C to use hardware bus (ultrasonic)
    pinMode(4,"OUTPUT")     #set up LED on port D4
    pinMode(7, "INPUT")     #set up button on port D7
    setText(" ")            #"clears" LCD screen
    setRGB(0,128,64)        #sets LCD screen color to blue

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        #publishes ultrasonic ranger reading
        ultrasonic_output = ultrasonicRead(3)   #ultrasonic ranger on port D3
        client.publish("rachelan/ultrasonicRanger", ultrasonic_output)

        #if button input is high, publish button pressed message
        if digitalRead(7):
            client.publish("rachelan/button", "Button pressed!")

        time.sleep(1)
