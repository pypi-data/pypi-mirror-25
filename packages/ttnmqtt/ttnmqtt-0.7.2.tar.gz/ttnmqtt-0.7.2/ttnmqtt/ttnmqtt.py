import paho.mqtt.client as mqtt
from pydispatch import dispatcher
import json

class MQTTClient:

    def __init__(self, APPID, APPEUI, DEVID, PSW):
        self.client = mqtt.Client()
        self.APPID = APPID
        self.APPEUI = APPEUI
        self.PSW = PSW
        self.DEVID = DEVID
        self.buffer = []
        self.currentMSG = {}
        self.numberOfMsg = 0
        self.messageHandler = None

    def getLastMessage(self):
        return self.currentMSG

    def getAllMessages(self):
        return self.buffer

    def connect(self):
        self.client.on_connect = self.onConnect()
        self.client.on_publish = self.onPublish()
        self.client.on_message = self.onMessage()
        self.client.username_pw_set(self.APPID, self.PSW)
        self.client.connect('eu.thethings.network', 1883, 60)

    def onConnect(self):
        def on_connect(client, userdata, flags, rc):
            client.subscribe('+/devices/+/up'.format(self.APPEUI))
            print('CONNECTED AND SUBSCRIBED')
        return on_connect

    def onMessage(self):
        def on_message(client, userdata, msg):
            print('MESSAGE RECEIVED')
            j_msg = json.loads(msg.payload.decode('utf-8'))
            self.buffer.append(j_msg)
            self.currentMSG = j_msg
            self.numberOfMsg+=1
            dispatcher.send(signal='New Message', sender=self)
        return on_message

    def onPublish(self):
        def on_publish(client, userdata, mid):
            print('MSG PUBLISHED', mid)
        return on_publish

    def setMessageBehavior(self, message):
        self.client.on_message = message

    def setConnectBehavior(self, connect):
        self.client.on_connect = connect

    def setPublishBehavior(self, publish):
        self.client.on_publish = publish

    def setGlobalBehavior(self, connect, message, publish):
        self.client.on_connect = connect
        self.client.on_publish = publish
        self.client.on_message = message

    def setMessageHandler(self, handler):
        if self.messageHandler:
            dispatcher.disconnect(self.messageHandler, signal='New Message', sender=dispatcher.Any)
        self.messageHandler = handler
        dispatcher.connect(self.messageHandler, signal='New Message', sender=dispatcher.Any)

    def start(self):
        print('LOOP STARTED')
        self.client.loop_forever()

    def startBackground(self):
        print('LOOP STARTED BACKGROUND')
        self.client.loop_start()

    def stopBackground(self):
        print('LOOP STOPPED BACKGROUND')
        self.client.loop_stop()
        self.disconnect()

    def disconnect(self):
        print('DISCONNECTED')
        self.client.disconnect()

    def publish(self, msg):
        self.client.publish(self.APPID+'/devices/'+self.DEVID+'/down', msg)
