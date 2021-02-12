#!/usr/bin/python3
import minimalmodbus
import json
import paho.mqtt.publish as publish
from datetime import datetime
import config

instrument = minimalmodbus.Instrument(config.serial_dev, 1)  # port name, slave address (in decimal)
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 2
instrument.serial.timeout  = 1
instrument.address = 1  # this is the slave address number
instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
instrument.clear_buffers_before_each_transaction = True

# Charge State
chargeState = instrument.read_register(256)
chargingNone = (chargeState & 0b0000000000000000) > 0
chargingSolar = (chargeState & 0b0000000000000100) > 0
chargingEqualization = (chargeState & 0b0000000000001000) > 0
chargingBoost = (chargeState & 0b0000000000010000) > 0
chargingFloat = (chargeState & 0b0000000000100000) > 0
chargingLimited = (chargeState & 0b0000000001000000) > 0
chargingAlt = (chargeState & 0b0000000010000000) > 0

# Error Codes
errorCodesLow = instrument.read_register(257)
errorCtrlOverTemp2 = ( errorCodesLow & 0b0000000000010000) > 0
errorAltInputOverCurrent = (errorCodesLow & 0b0000000000100000) > 0
errorAltInputOverVolt = (errorCodesLow & 0b0000000100000000) > 0
errorAltPolarityReverse = (errorCodesLow & 0b0000001000000000) > 0
errorBmsOverCharge = (errorCodesLow & 0b0000010000000000) > 0
errorAuxLowTemp = (errorCodesLow & 0b0000100000000000) > 0

errorCodesHigh = instrument.read_register(258)
errorAuxOverDischarge = ( errorCodesHigh & 0b0000000000000001) > 0
errorAuxOverVolt = ( errorCodesHigh & 0b0000000000000010) > 0
errorAuxUnderVolt = ( errorCodesHigh & 0b0000000000000100) > 0
errorCtrlOverTemp = ( errorCodesHigh & 0b0000000000100000) > 0
errorAuxOverTemp = ( errorCodesHigh & 0b0000000001000000) > 0
errorSolInputTooHigh = ( errorCodesHigh & 0b0000000010000000) > 0
errorSolInputOverVolt = ( errorCodesHigh & 0b0000001000000000) > 0
errorSolReversePolarity = ( errorCodesHigh & 0b0001000000000000) > 0

mqttPublishPayload = json.dumps({
	"auxSoc": instrument.read_register(256),
	"auxVoltage": instrument.read_register(257,1),
	"maxCharge": instrument.read_register(258,2),
	"controllerTemp": instrument.read_register(259),
	"auxTemp": instrument.read_register(259),
	"altVoltage": instrument.read_register(260,1),
	"altAmps": instrument.read_register(261,2),
	"altWatts": instrument.read_register(262),
	"solVoltage": instrument.read_register(263,1),
	"solAmps": instrument.read_register(264,2),
	"solWatts": instrument.read_register(265),
	"dayCount": instrument.read_register(271),
	"chargeState": instrument.read_register(276),
	"faultBits1": instrument.read_register(277),
	"faultBits2": instrument.read_register(278),
	"timestamp": str(datetime.now()),
	"chargingNone": chargingNone,
	"chargingSolar": chargingSolar,
	"chargingEqualization": chargingEqualization,
	"chargingBoost": chargingBoost,
	"chargingFloat": chargingFloat,
	"chargingLimited": chargingLimited,
	"chargingAlt": chargingAlt,
	"errorCtrlOverTemp2": errorCtrlOverTemp2,
	"errorAltInputOverCurrent": errorAltInputOverCurrent,
	"errorAltInputOverVolt": errorAltInputOverVolt,
	"errorAltPolarityReverse ": errorAltPolarityReverse,
	"errorBmsOverCharge": errorBmsOverCharge,
	"errorAuxLowTemp": errorAuxLowTemp,
	"errorCodesHigh": errorCodesHigh,
	"errorAuxOverDischarge": errorAuxOverDischarge,
	"errorAuxOverVolt": errorAuxOverVolt,
	"errorAuxUnderVolt": errorAuxUnderVolt,
	"errorCtrlOverTemp": errorCtrlOverTemp,
	"errorAuxOverTemp": errorAuxOverTemp,
	"errorSolInputTooHigh": errorSolInputTooHigh,
	"errorSolInputOverVolt": errorSolInputOverVolt,
	"errorSolReversePolarity": errorSolReversePolarity,
})

try:
	publish.single(
		topic=config.topic,
		payload=mqttPublishPayload,
		retain=True,
        hostname=config.broker_url,
        port=config.broker_port,
        auth=config.broker_auth,
		tls=config.broker_tls,
        client_id=config.client_id,
        qos=0
	)
except:
	print ("Error")
