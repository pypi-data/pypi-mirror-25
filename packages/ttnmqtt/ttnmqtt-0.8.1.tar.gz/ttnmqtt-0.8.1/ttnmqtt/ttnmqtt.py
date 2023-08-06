import paho.mqtt.client as mqtt
from pydispatch import dispatcher
import json

class MQTTClient:

    def __init__(self, APPID, APPEUI, DEVID, PSW):
        self.__client = mqtt.Client()
        self.__APPID = APPID
        self.__APPEUI = APPEUI
        self.__PSW = PSW
        self._DEVID = DEVID
        self._buffer = []
        self._currentMSG = {}
        self._numberOfMsg = 0
        self._messageHandler = None

    def setDeviceID(self, devid):
        self._DEVID = devid

    def getLastMessage(self):
        return self._currentMSG

    def getAllMessages(self):
        return self._buffer

    def connect(self):
        self.__client.on_connect = self.onConnect()
        self.__client.on_publish = self.onPublish()
        self.__client.on_message = self.onMessage()
        self.__client.username_pw_set(self.__APPID, self.__PSW)
        self.__client.connect('eu.thethings.network', 1883, 60)

    def onConnect(self):
        def on_connect(client, userdata, flags, rc):
            client.subscribe('+/devices/+/up'.format(self.__APPEUI))
            print('CONNECTED AND SUBSCRIBED')
        return on_connect

    def onMessage(self):
        def on_message(client, userdata, msg):
            print('MESSAGE RECEIVED')
            j_msg = json.loads(msg.payload.decode('utf-8'))
            self._buffer.append(j_msg)
            self._currentMSG = j_msg
            self._numberOfMsg+=1
            dispatcher.send(signal='New Message', sender=self)
        return on_message

    def onPublish(self):
        def on_publish(client, userdata, mid):
            print('MSG PUBLISHED', mid)
        return on_publish

    def setMessageBehavior(self, message):
        self.__client.on_message = message

    def setConnectBehavior(self, connect):
        self.__client.on_connect = connect

    def setPublishBehavior(self, publish):
        self.__client.on_publish = publish

    def setGlobalBehavior(self, connect, message, publish):
        self.__client.on_connect = connect
        self.__client.on_publish = publish
        self.__client.on_message = message

    def setMessageHandler(self, handler):
        if self._messageHandler:
            dispatcher.disconnect(self._messageHandler, signal='New Message', sender=dispatcher.Any)
        self._messageHandler = handler
        dispatcher.connect(self._messageHandler, signal='New Message', sender=dispatcher.Any)

    def start(self):
        print('LOOP STARTED')
        self.__client.loop_forever()

    def startBackground(self):
        print('LOOP STARTED BACKGROUND')
        self.__client.loop_start()

    def stopBackground(self):
        print('LOOP STOPPED BACKGROUND')
        self.__client.loop_stop()
        self.disconnect()

    def disconnect(self):
        print('DISCONNECTED')
        self.__client.disconnect()

    def publish(self, msg):
        self.__client.publish(self.__APPID+'/devices/'+self._DEVID+'/down', msg)
