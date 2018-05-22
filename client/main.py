import random

import paho.mqtt.client as mqtt
import ssl
import threading
import time
import subprocess
import os

import util.device as device
import util.location as location
import util.logger as logger

log = logger.get_logger(__name__)

receivedMessages = []
#device.print_env_values()

count = 0

def on_message(client, userdata, message):
    log.info("Received operation " + str(message.payload))
    if message.payload.startswith("510"):
        publish("s/us", "501,c8y_Restart")
        log.info("...restarting...")
        publish("s/us", "503,c8y_Restart")
        os.system('reboot')
    if message.payload.startswith("511"):
        publish("s/us", "501,c8y_Command")
        command = str(message.payload.split(',')[2])
        log.info("Received command: " + command)
        output = str(os.popen(command).read()[:200])
        log.info("Output: " + output)
        publish("s/us", "503,c8y_Command,\"" + output + "\"")
    if message.payload.startswith("516"):
        publish("s/us", "501,c8y_Software")
        url = str(message.payload.split(',')[4])
        log.info("Downloading software from URL: " + url)
        publish("s/us", "503,c8y_Software")
        subprocess.call("/home/pi/cumulocity-python-client/install.sh >> /var/log/uiot_client.log", shell=True)


def send_measurements():
    global count
    try:
        #power1 = subprocess.check_output("cat /var/log/emonhub/emonhub.log | grep 'power1 ' | tail -n 1 | awk '{print $7}'", shell=True).strip()
        power1 = str(os.popen("cat /var/log/emonhub/emonhub.log | grep 'power1 ' | tail -n 1 | awk '{print $7}'").read()).strip()
        log.info("Power: " + str(power1))
        publish("s/us", "200,c8y_CurrentSensor,T," + str(power1))
        #signal = subprocess.check_output("/sbin/iwconfig wlan0 | grep 'Link Quality' | awk '{print substr($2, 9)}'", shell=True).strip()
        signal = str(os.popen("/sbin/iwconfig wlan0 | grep 'Link Quality' | awk '{print substr($2, 9)}'").read()).strip()
        signal_split = signal.split('/')
        signal_total = int(signal_split[0]) / int(signal_split[1]) * 100 
        log.info("Signal Strength: " + str(signal_total))
        publish("s/us", "210," + str(signal_total))
        thread = threading.Timer(5, send_measurements)
        thread.daemon = True
        thread.start()
        if count == 0:
            count = count + 1
            while True:
                time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        log.info('Received keyboard interrupt, quitting ...')


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
log.info("Location: " + str(location.get_lat_long()))
publish("s/us", "112," + str(location.get_lat_long()))
publish("s/us", "114,c8y_Restart,c8y_Configuration,c8y_SoftwareList,c8y_Software,c8y_Firmware,c8y_LogfileRequest,c8y_Command")
publish("s/us", "400,c8y_ConnectionEvent,'Device connected'")
client.subscribe("s/ds")
send_measurements()
