#!/usr/bin/python3
import minimalmodbus
import socket
import paho.mqtt.publish as publish

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # port name, slave address (in decimal)

instrument.serial.baudrate = 9600         # Baud
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 2
instrument.serial.timeout  = 1

instrument.address = 1     # this is the slave address number
instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
instrument.clear_buffers_before_each_transaction = True

# print(instrument)   # Print config

mqttPublishPayload = {
	"auxSoc" = instrument.read_register(256),
	"auxVoltage" = instrument.read_register(257)/10.0,
	"maxCharge" = instrument.read_register(258)/100.0,
	"controllerTemp" = instrument.read_register(259),
	"auxTemp" = instrument.read_register(259),
	"altVoltage" = instrument.read_register(260)/10.0,
	"altAmps" = instrument.read_register(261)/100.0,
	"altWatts" = instrument.read_register(262),
	"solVoltage" = instrument.read_register(263)/10.0,
	"solAmps" = instrument.read_register(264)/100.0,
	"solWatts" = instrument.read_register(265),
	"dayCount" = instrument.read_register(271),
	"chargeState" = instrument.read_register(276),
	"faultBits1" = instrument.read_register(277),
	"faultBits2" = instrument.read_register(278)
}

try:
	print(str(mqttPublishPayload.auxSoc) + '%')
	print(str(mqttPublishPayload.auxVoltage) + 'V')
	print(str(mqttPublishPayload.maxCharge) + 'A')
	print(str(mqttPublishPayload.controllerTemp) + '°C')
	print(str(mqttPublishPayload.auxTemp) + '°C')
	print(str(mqttPublishPayload.altVoltage) + 'V')
	print(str(mqttPublishPayload.altAmps) + 'A')
	print(str(mqttPublishPayload.altWatts) + 'W')
	print(str(mqttPublishPayload.solVoltage) + 'V')
	print(str(mqttPublishPayload.solAmps) + 'A')
	print(str(mqttPublishPayload.solWatts) + 'W')
	print(str(mqttPublishPayload.dayCount) + ' days')
	print(str(mqttPublishPayload.chargeState) + '')
	print(str(mqttPublishPayload.faultBits1) + '')
	print(str(mqttPublishPayload.faultBits2) + '')
except IOError:
	print ("Failed to read")

try:
	publish.single(
		topic="van/solar",
		payload=mqttPublishPayload,
		qos=0,
		retain=True,
		hostname="mqtt.zawyer.uk",
		port="1883",
		client_id=socket.gethostname(),
		keepalive=10,
		will={
			topic="van/status",
			payload=None,
			qos=0,
			retain=True
		},
		auth={username="sammy",password="sammy"},
		tls=None
		)
except MQTT_ERR_NO_CONN:
	print ("Not connected!")
except MQTT_ERR_QUEUE_SIZE:
	print ("Max Queued messages reached!")


