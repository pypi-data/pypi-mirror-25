import time
import re
import socket
import sys
import Adafruit_DHT
import traceback

import paho.mqtt.client as mqtt
from threading import Thread

class DHT22Logger:
    config = None
    mqtt_client = None
    mqtt_connected = False
    worker = None
    temperature = None
    humidity = None

    def __init__(self, config):
        self.config = config

    def verbose(self, message):
        if self.config and 'verbose' in self.config and self.config['verbose'] == 'true':
            sys.stdout.write('VERBOSE: ' + message + '\n')
            sys.stdout.flush()

    def error(self, message):
        sys.stderr.write('ERROR: ' + message + '\n')
        sys.stderr.flush()

    def mqtt_connect(self):
        if self.mqtt_broker_reachable():
            self.verbose('Connecting to ' + self.config['mqtt_host'] + ':' + self.config['mqtt_port'])
            self.mqtt_client = mqtt.Client(self.config['mqtt_client_id'])
            if 'mqtt_user' in self.config and 'mqtt_password' in self.config:
                self.mqtt_client.username_pw_set(self.config['mqtt_user'], self.config['mqtt_password'])

            self.mqtt_client.on_connect = self.mqtt_on_connect
            self.mqtt_client.on_disconnect = self.mqtt_on_disconnect

            try:
                self.mqtt_client.connect(self.config['mqtt_host'], int(self.config['mqtt_port']), 60)
                self.mqtt_client.loop_forever()
            except:
                self.error(traceback.format_exc())
                self.mqtt_client = None
        else:
            self.error(self.config['mqtt_host'] + ':' + self.config['mqtt_port'] + ' not reachable!')

    def mqtt_on_connect(self, mqtt_client, userdata, flags, rc):
        self.mqtt_connected = True
        self.verbose('...mqtt_connected!')

    def mqtt_on_disconnect(self, mqtt_client, userdata, rc):
        self.mqtt_connected = False
        self.verbose('Diconnected! will reconnect! ...')
        if rc is 0:
            self.mqtt_connect()
        else:
            time.sleep(5)
            while not self.mqtt_broker_reachable():
                time.sleep(10)
            self.mqtt_client.reconnect()

    def mqtt_broker_reachable(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        try:
            s.connect((self.config['mqtt_host'], int(self.config['mqtt_port'])))
            s.close()
            return True
        except socket.error:
            return False

    def update(self):
        while True:
            raw_humidity, raw_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, int(self.config['gpio']))
            humidity = round(raw_humidity)
            temperature = round(raw_temperature)
            self.verbose('Temperature: ' + str(temperature))
            self.verbose('Humidity: ' + str(humidity))
            if humidity != self.humidity:
                self.humidity = humidity
                self.publish_humidity(humidity)
            if temperature != self.temperature:
                self.temperature = temperature
                self.publish_temperature(temperature)

            time.sleep(300)

    def publish_humidity(self, humidity):
        if self.mqtt_connected:
            self.verbose('Publishing humidity: ' + str(humidity))
            self.mqtt_client.publish(self.config['topics']['humidity'], str(humidity), 0, True)

    def publish_temperature(self, temperature):
        if self.mqtt_connected:
            self.verbose('Publishing temperature: ' + str(temperature))
            self.mqtt_client.publish(self.config['topics']['temperature'], str(temperature), 0, True)

    def start(self):
        self.worker = Thread(target=self.update)
        self.worker.setDaemon(True)
        self.worker.start()
        self.mqtt_connect()
