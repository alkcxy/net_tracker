from paho.mqtt.client import Client
import configparser
import os
import platform    # For getting the operating system name
import subprocess  # For executing a shell command

def ping(host, i):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    i = i - 1
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    if subprocess.call(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL) == 0:
        return 1
    elif i == 0:
        return 0
    return ping(host, i)

def on_connect(client, userdata, flags, rc):
    print("Connesso con successo")

def on_message(client, userdata, message):
    message = message.payload.decode()
    publish_topic = f'net_tracker/device/{message}'
    print(publish_topic)
    payload = 0
    print(message)
    if config['ips'][message]:
        payload = ping(config['ips'][message], ping_retry)
    print(payload)
    client.publish(publish_topic, payload=payload, qos=2)


config = configparser.ConfigParser()
config.read('config.ini')

if os.environ.get('PING_RETRY'):
    ping_retry = os.environ.get('PING_RETRY')
else:
    ping_retry = 10

if os.environ.get('MQTT_HOST'):
    mqtt_host = os.environ.get('MQTT_HOST')
else:
    mqtt_host = config['mqtt']['host']

if os.environ.get('MQTT_USER'):
    mqtt_user = os.environ.get('MQTT_USER')
else:
    mqtt_user = config['mqtt']['user']

if os.environ.get('MQTT_PWD'):
    mqtt_password = os.environ.get('MQTT_PWD')
else:
    mqtt_password = config['mqtt']['pwd']

client = Client(client_id="net_tracker")
client.on_connect = on_connect
client.on_message = on_message

if mqtt_user and mqtt_password:
    client.username_pw_set(mqtt_user, password=mqtt_password)

client.connect(mqtt_host)
client.subscribe("net_tracker/scan", qos=2)
client.loop_forever()
