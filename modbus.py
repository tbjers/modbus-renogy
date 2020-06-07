#!/usr/bin/python3
import minimalmodbus
import socket
import json
import paho.mqtt.client as mqtt

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # port name, slave address (in decimal)

instrument.serial.baudrate = 9600         # Baud
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 2
instrument.serial.timeout  = 1

instrument.address = 1     # this is the slave address number
instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
instrument.clear_buffers_before_each_transaction = True

broker_url = '192.168.69.106'
broker_port = 1883

# print(instrument)   # Print config

mqttPublishPayload = {
	"auxSoc": instrument.read_register(256),
	"auxVoltage": instrument.read_register(257)/10.0,
	"maxCharge": instrument.read_register(258)/100.0,
	"controllerTemp": instrument.read_register(259),
	"auxTemp": instrument.read_register(259),
	"altVoltage": instrument.read_register(260)/10.0,
	"altAmps": instrument.read_register(261)/100.0,
	"altWatts": instrument.read_register(262),
	"solVoltage": instrument.read_register(263)/10.0,
	"solAmps": instrument.read_register(264)/100.0,
	"solWatts": instrument.read_register(265),
	"dayCount": instrument.read_register(271),
	"chargeState": instrument.read_register(276),
	"faultBits1": instrument.read_register(277),
	"faultBits2": instrument.read_register(278)
}

try:
	print(str(mqttPublishPayload['auxSoc']) + '% auxSoc')
	print(str(mqttPublishPayload['auxVoltage']) + 'V auxVoltage')
	print(str(mqttPublishPayload['maxCharge']) + 'A maxCharge')
	print(str(mqttPublishPayload['controllerTemp']) + '°C controllerTemp')
	print(str(mqttPublishPayload['auxTemp']) + '°C auxTemp')
	print(str(mqttPublishPayload['altVoltage']) + 'V altVoltage')
	print(str(mqttPublishPayload['altAmps']) + 'A altAmps')
	print(str(mqttPublishPayload['altWatts']) + 'W altWatts')
	print(str(mqttPublishPayload['solVoltage']) + 'V solVoltage')
	print(str(mqttPublishPayload['solAmps']) + 'A solAmps')
	print(str(mqttPublishPayload['solWatts']) + 'W solWatts')
	print(str(mqttPublishPayload['dayCount']) + ' days')
	print(str(mqttPublishPayload['chargeState']) + ' chargeState')
	print(str(mqttPublishPayload['faultBits1']) + ' faultBits1')
	print(str(mqttPublishPayload['faultBits2']) + ' faultBits2')
except IOError:
	print ("Failed to read")

mqttPublishPayload = json.dumps(mqttPublishPayload)

try:
	client = mqtt.Client()
	client.connect(broker_url, broker_port)
	client.publish(
		topic="van/solar",
		payload=mqttPublishPayload,
		qos=0,
		retain=True,
		client_id=socket.gethostname(),
		keepalive=10,
		auth={'username':"sammy",'password':"sammy"},
		tls=None
	)
except:
	print ("Error")
#except MQTT_ERR_NO_CONN:
#	print ("Not connected!")
#except MQTT_ERR_QUEUE_SIZE:
#	print ("Max Queued messages reached!")


