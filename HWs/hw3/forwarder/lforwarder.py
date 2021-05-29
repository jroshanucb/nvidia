import paho.mqtt.client as mqtt

LOCAL_MQTT_HOST="localhost"
LOCAL_MQTT_PORT=30789
LOCAL_MQTT_TOPIC="my_topic"
#LOCAL_MQTT_TOPIC="w251_hw3"

REMOTE_MQTT_HOST="34.223.93.188"
REMOTE_MQTT_PORT=30789
REMOTE_MQTT_TOPIC="my_topic"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)
	
def on_connect_remote(client, userdata, flags, rc):
        print("connected to remote broker with rc: " + str(rc))

def on_publish_remote(client, userdata, result):
    print("data published on the cloud queue with result: ", result)

def on_message(client,userdata, msg):
  try:
    # print("message received: ",msg.payload)
    print("message received: ")
    # if we wanted to re-publish this message, something like this should work
    msg = msg.payload
    remote_mqttclient.publish(REMOTE_MQTT_TOPIC, payload=msg, qos=0, retain=False)
    # print("mesg published to cloud queue")
  except:
    print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message

remote_mqttclient = mqtt.Client()
remote_mqttclient.on_connect = on_connect_remote
remote_mqttclient.connect(REMOTE_MQTT_HOST, REMOTE_MQTT_PORT, 60)
remote_mqttclient.on_publish = on_publish_remote

# go into a loop
local_mqttclient.loop_forever()
