import paho.mqtt.client as mqtt
import json

# Callbacks
def on_connect(client, userdata, flags, rc):
    print("Subscriber connected with result code "+str(rc))
    client.subscribe("ece180d/test", qos=1)

def on_message(client, userdata, message):
    payload = message.payload.decode()
    print(f"Received raw message: {payload}")
    
    # Try to decode JSON if possible
    try:
        data = json.loads(payload)
        print(f"Decoded JSON: {data}")
    except:
        pass

# Create client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect_async('test.mosquitto.org')
client.loop_start()

print("Subscriber running. Waiting for messages...")

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Stopping subscriber...")
    client.loop_stop()
    client.disconnect()