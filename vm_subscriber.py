"""EE 250L Lab 04 Starter Code

Team Members: Rachel Anderson
Repo Link: git@github.com:usc-ee250-fall2021/lab05-rachel5.git

Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time

#Ultrasonic ranger callback - receives and prints ranger output
def ultrasonic_callback(client, userdata, message):
    print("VM: " + message.payload.decode("utf-8","strict") + " cm")

#Button callback - prints "Button pressed!" if button is pressed
def button_callback(client, userdata, message):
    print(message.payload.decode("utf-8", "strict"))

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to the ultrasonic ranger topic here
    client.subscribe("rachelan/ultrasonicRanger")
     #specify what to do when messages are received on this topic
    client.message_callback_add("rachelan/ultrasonicRanger", ultrasonic_callback)

    #subscribe to button topic
    client.subscribe("rachelan/button")
    client.message_callback_add("rachelan/button", button_callback)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)
