# Renogy-DCC50S-modbus

This project is to pull stats out of a Renogy DCC50S solar charge controller.

The connection will be made via modbus/RS485. 

The end state will be to pull required stats and formatted into a payload for ingestion into an InfluxDb instance.

## main.py
`main.py` drags the stats out of the controller into a json format.

## mqtt.py
Copy `configMqtt.py.example` to `configMqtt.py` and configure your own variables.

Use `mqtt.py` to pull the stats from `main.py` and send them to an mqtt topic.
