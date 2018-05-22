import random

import paho.mqtt.client as mqtt
import ssl
import threading
import time
import subprocess
import os

import util.device as device
import util.location as location

receivedMessages = []
device.print_env_values()

count = 0

def on_message(client, userdata, message):
    print("Received operation " + str(message.payload))
    if message.payload.startswith("510"):
        print("Simulating device restart...")
        publish("s/us", "501,c8y_Restart")
        print("...restarting...")
        time.sleep(1)
        publish("s/us", "503,c8y_Restart")
        print("...done...")


def send_measurements():
    global count
    try:
        print("Sending power measurement")
        #power1 = subprocess.check_output("cat /var/log/emonhub/emonhub.log | grep 'power1 ' | tail -n 1 | awk '{print $7}'", shell=True).strip()
        power1 = str(os.popen("cat /var/log/emonhub/emonhub.log | grep 'power1 ' | tail -n 1 | awk '{print $7}'").read()).strip()
        print "Power: " + str(power1)
        publish("s/us", "200,c8y_CurrentSensor,T," + str(power1))
        print("Sending signal strength measurement")
        #signal = subprocess.check_output("iwconfig wlan0 | grep 'Link Quality' | awk '{print substr($2, 9)}'", shell=True).strip()
        signal = str(os.popen("iwconfig wlan0 | grep 'Link Quality' | awk '{print substr($2, 9)}'").read()).strip()
        signal_split = signal.split('/')
        signal_total = int(signal_split[0]) / int(signal_split[1]) * 100 
        print "Signal Strength: " + str(signal_total)
        publish("s/us", "210," + str(signal_total))
        thread = threading.Timer(5, send_measurements)
        thread.daemon = True
        thread.start()
        if count == 0:
            count = count + 1
            while True:
                time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        print 'Received keyboard interrupt, quitting ...'


def publish(topic, message, wait_for_ack=False):
    mid = client.publish(topic, message, 2)[1]
    if wait_for_ack:
        while mid not in receivedMessages:
            time.sleep(0.25)


def on_publish(client, userdata, mid):
    receivedMessages.append(mid)


client = mqtt.Client(client_id=device.get_client_id())
client.username_pw_set(device.get_tenant() + '/' + device.get_user(), device.get_password())
client.on_message = on_message
client.on_publish = on_publish

client.connect(device.get_server_host(), 1883)
client.loop_start()
publish("s/us", "100," + device.get_client_id() + ",c8y_MQTTAgent", True)
publish("s/us", "110," + device.get_client_id() + "," + device.get_client_model() + ",Rev0.1")
print "Location: " + str(location.get_lat_long())
publish("s/us", "112," + str(location.get_lat_long()))
client.subscribe("s/ds")
send_measurements()
