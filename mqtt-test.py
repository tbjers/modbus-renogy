#!/usr/bin/python3
import socket
import json
import paho.mqtt.publish as mqtt

broker_url = '192.168.69.106'
broker_port = 1883


mqttPublishPayload = {
	"test1":"value"
}

mqttPublishPayload = json.dumps(mqttPublishPayload)

#client = mqtt.Client()
#client.connect(broker_url, broker_port)
mqtt.single(
	"van/solar",
	payload=mqttPublishPayload,
	qos=0,
	retain=True,
	hostname='mqtt.zawyer.uk',
	port=1833,
#	client_id=socket.gethostname(),
	keepalive=10,
	auth={'username':"sammy",'password':"sammy"},
	tls=None
)
#except:
#	print ("Error")
#except MQTT_ERR_NO_CONN:
#	print ("Not connected!")
#except MQTT_ERR_QUEUE_SIZE:
#	print ("Max Queued messages reached!")


