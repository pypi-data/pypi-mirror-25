import paho.mqtt.client as mqtt
import time

class MQTTClient:

    def __init__(self, APPID, DEVID, PSW):
        self.client = mqtt.Client()
        self.APPID = APPID
        self.PSW = PSW
        self.DEVID = DEVID

    def connect(self):
        self.client.username_pw_set(self.APPID, self.PSW)
        self.client.connect('eu.thethings.network', 1883, 60)

    def setBehavior(self, connect, message, publish):
        self.client.on_connect = connect
        self.client.on_publish = publish
        self.client.on_message = message

    def start(self):
        print('LOOP STARTED')
        self.client.loop_forever()

    def startBackground(self):
        print('LOOP STARTED BACKGROUND')
        self.client.loop_start()

    def stopBackground(self):
        print('LOOP STOPPED BACKGROUND')
        time.sleep(2000)
        self.client.loop_stop()

    def stop(self):
        print('LOOP STOPPED')
        self.client.disconnect()

    def publish(self, msg):
        self.client.publish(self.APPID+'/devices/'+self.DEVID+'/down', msg)
