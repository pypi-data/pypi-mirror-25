import paho.mqtt.publish as publish

publish.single("paho/test/single", "payload", hostname="192.168.1.148", port=8883)