import paho.mqtt.client as mqtt
import random
import time
import configparser
import threading

# Load MQTT configuration from file
config = configparser.ConfigParser()
config.read('config.ini')

client_address = config['mqtt']['client_address']
port = int(config['mqtt']['port'])
room = int(config['data_generation']['room'])
time_sleep = int(config['data_generation']['time_sleep'])

sensors = config['data_generation']['sensors'].split('|')

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.connect(client_address, port=port)
# Function to publish area data to MQTT broker
def publish_area_data(mqtt_client, sensors, room):
    while True:
        # Generate random sensor data
        for sensor in sensors:
            if sensor == 'temperature':
                data = round(random.uniform(0, 40), 2)
            elif sensor == 'humidity':
                data = round(random.uniform(0, 90), 2)
            elif sensor == 'air_quality':
                data = random.randint(0, 500)
            #mqtt_client.publish(topic, payload=str(data))
            topic = f"rooms/room_{room}/{sensor}"
            mqtt_client.publish(topic, f'{{"{sensor}":{data}}}')
            print(f"Published {topic}: {data}")

        time.sleep(time_sleep)

# Publish data for each sensor
threads=[]
for room in range(room):
    thread = threading.Thread(target=publish_area_data, args=(mqtt_client, sensors, room))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete (which they won't, as they're infinite loops)
for thread in threads:
    thread.join()

