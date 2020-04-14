from paho.mqtt.client import Client

import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def ping(host, i=10):
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

client = Client(client_id="net_tracker")

def on_connect(client, userdata, flags, rc):
    print("Connesso con successo")

def on_message(client, userdata, message):
    message = message.payload.decode()
    publish_topic = f'net_tracker/device/{message}'
    print(publish_topic)
    payload = 0
    print(message)
    if config['ips'][message]:
        payload = ping(config['ips'][message])
    print(payload)
    client.publish(publish_topic, payload=payload, qos=2)

client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(config['mqtt']['user'], password=config['mqtt']['pwd'])
client.connect(config['mqtt']['host'])
client.subscribe("net_tracker/scan", qos=2)
client.loop_forever()
