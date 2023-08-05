import RPi.GPIO as GPIO
import time
import socket
import sys
import traceback
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BCM)


class Switch:
    gpio = None
    topic_status = None

    def __init__(self, gpio, topic_status):
        self.gpio = gpio
        self.topic_status = topic_status
        GPIO.setup(self.gpio, GPIO.OUT)
        self.off()

    def on(self):
        GPIO.output(self.gpio, GPIO.HIGH)

    def off(self):
        GPIO.output(self.gpio, GPIO.LOW)


class Switcher:
    config = None
    mqtt_client = None
    mqtt_connected = False
    switches = {}

    def __init__(self, config):
        self.config = config
        for switch_cfg in self.config['switches']:
            self.switches[switch_cfg['topic_set']] = Switch(int(switch_cfg['gpio']), switch_cfg['topic_status'])

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
            self.mqtt_client.on_message = self.mqtt_on_message

            try:
                self.mqtt_client.connect(self.config['mqtt_host'], int(self.config['mqtt_port']), 10)
                for switch_cfg in self.config['switches']:
                    self.mqtt_client.subscribe(switch_cfg['topic_set'], 0)
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

    def mqtt_on_message(self, client, userdata, message):
        self.verbose(message.topic)

        if message.topic in self.switches:
            value = str(message.payload)
            if value == 'on':
                self.switches[message.topic].on()
                self.publish_status(self.switches[message.topic].topic_status, 'on')
            elif value == 'off':
                self.switches[message.topic].off()
                self.publish_status(self.switches[message.topic].topic_status, 'off')
            elif value == 'reset':
                self.switches[message.topic].off()
                self.publish_status(self.switches[message.topic].topic_status, 'off')
                time.sleep(2)
                self.switches[message.topic].on()
                self.publish_status(self.switches[message.topic].topic_status, 'on')

    def publish_status(self, topic, status):
        if self.mqtt_connected:
            self.verbose('Publishing: ' + str(status))
            self.mqtt_client.publish(topic, str(status), 0, True)

    def start(self):
        self.mqtt_connect()
