import paho.mqtt.client as mqtt
import time
import numpy as np

client = mqtt.Client()
client.connect("test.mosquitto.org", 1883, 60)
client.loop_start()

for i in range(10):
    msg = float(np.random.random(1))
    print(f"Publishing: {msg}")
    client.publish("ece180d/test", msg, qos=1)
    time.sleep(1)

client.loop_stop()
client.disconnect()
print("Publisher finished.")
