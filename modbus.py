#!/usr/bin/python3
import minimalmodbus

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

auxSoc = instrument.read_register(256)
auxVoltage = instrument.read_register(257)/10.0
maxCharge = instrument.read_register(258)/100.0
controllerTemp = instrument.read_register(259)
auxTemp = instrument.read_register(259)
altVoltage = instrument.read_register(260)/10.0
altAmps = instrument.read_register(261)/100.0
altWatts = instrument.read_register(262)
solVoltage = instrument.read_register(263)/10.0
solAmps = instrument.read_register(264)/100.0
solWatts = instrument.read_register(265)
dayCount = instrument.read_register(271)
chargeState = instrument.read_register(276)
faultBits1 = instrument.read_register(277)
faultBits2 = instrument.read_register(278)

try:
	print(str(auxSoc) + '%')
	print(str(auxVoltage) + 'V')
	print(str(maxCharge) + 'A')
	print(str(controllerTemp) + '°C')
	print(str(auxTemp) + '°C')
	print(str(altVoltage) + 'V')
	print(str(altAmps) + 'A')
	print(str(altWatts) + 'W')
	print(str(solVoltage) + 'V')
	print(str(solAmps) + 'A')
	print(str(solWatts) + 'W')
	print(str(dayCount) + ' days')
	print(str(chargeState) + '')
	print(str(faultBits1) + '')
	print(str(faultBits2) + '')
except IOError:
	print ("Failed to read")
