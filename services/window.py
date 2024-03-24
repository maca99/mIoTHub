import json
import time
import paho.mqtt.client as mqtt
import random

def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
        print("This is due to an unavoidable race-condition:")
        print("* publish() return the mid of the message sent.")
        print("* mid from publish() is added to unacked_publish by the main thread")
        print("* on_publish() is called by the loop_start thread")
        print("While unlikely (because on_publish() will be called after a network round-trip),")
        print(" this is a race-condition that COULD happen")
        print("")
        print("The best solution to avoid race-condition is using the msg_info from publish()")
        print("We could also try using a list of acknowledged mid rather than removing from pending list,")
        print("but remember that mid could be re-used !")

unacked_publish = set()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish

mqttc.user_data_set(unacked_publish)
mqttc.connect("Localhost")

mqttc.loop_start()
while True:
    temp = str(random.randint(16,28));
    hum = str(random.randint(20,80));
    data = {
        "temperature": temp,
        "humidity": hum
    }

    json_data = json.dumps(data)

    msg_info = mqttc.publish("sensor/temperature", json_data, qos=2)
    unacked_publish.add(msg_info.mid)
    msg_info.wait_for_publish()
    time.sleep(5)

mqttc.disconnect()