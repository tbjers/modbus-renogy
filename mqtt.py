#!/usr/bin/python3
import main
import paho.mqtt.publish as publish
import configMqtt as config

try:
    publish.single(
    topic=config.topic,
    payload=main.payload,
    retain=True,
    hostname=config.broker_url,
    port=config.broker_port,
    auth=config.broker_auth,
    # tls=config.broker_tls, # Disable if TLS not enabled on MQTT otherwise will error
    client_id=config.client_id,
    qos=0
    )
except Exception as e:
    print (e)
