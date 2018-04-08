import random

import paho.mqtt.client as mqtt
import ssl
import threading
import time

import util.device as device
import util.location as location

receivedMessages = []
device.print_env_values()


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
    try:
        print("Sending temperature measurement")
        publish("s/us", "211," + str(random.randint(20, 35)))
        print("Sending signal strength measurement")
        publish("s/us", "210," + str(random.randint(45, 50)))
        print("Sending battery measurement")
        publish("s/us", "212," + str(random.randint(460, 830)))
        thread = threading.Timer(3, send_measurements)
        thread.daemon = True
        thread.start()
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
publish("s/us", "110," + device.get_client_id() + "," + device.get_client_model())
print location.get_lat_long()
publish("s/us", location.get_lat_long())
client.subscribe("s/ds")
send_measurements()
