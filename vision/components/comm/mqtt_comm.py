"""communication module"""
import os
from abc import abstractmethod
from typing import Optional

import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from paho.mqtt.client import Client, MQTTMessage

from vision.components.comm.communication_base import CommunicationBase


class MqttComm(CommunicationBase):  # pylint: disable=too-few-public-methods
    """class responsible for connecting to the MQTT broker"""

    def __init__(self) -> None:
        load_dotenv()
        self.mqtt_topic_subscribe = os.getenv("MQTT_TOPIC_VISION_SUBSCRIBE")
        if not self.mqtt_topic_subscribe:
            raise ValueError("A variável de ambiente 'MQTT_TOPIC_SUBSCRIBE' não está definida")
        self.mqtt_topic_publish = os.getenv("MQTT_TOPIC_VISION_PUBLISH")
        mqtt_host_str = os.getenv('MQTT_HOST')
        if mqtt_host_str is None:
            raise ValueError("A variável de ambiente 'MQTT_MOSQUITTO_HOST' não está definida")

        self.mqtt_host = mqtt_host_str
        mqtt_port_str = os.getenv('MQTT_MOSQUITTO_TLS_PORT', '1883')
        try:
            self.mqtt_port = int(mqtt_port_str)
        except ValueError as exc:
            raise ValueError(f"Valor de porta inválido: {mqtt_port_str}") from exc

        mqtt_max_connections_str = os.getenv('MQTT_MAX_CONNECTIONS', '3')
        try:
            self.mqtt_max_connections = int(mqtt_max_connections_str)
        except ValueError as exc:
            raise ValueError(f"Valor inválido para o "
                             f"máximo de conexões: {mqtt_max_connections_str}") from exc

        self.count_connections = 0
        # self.client: mqtt.Client = None

    def subiscribe(self) -> None:
        """register on a specific MQTT broker topic"""
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.on_message = self._work_load
        client.on_connect_fail = self._on_connect_fail
        client.connect(self.mqtt_host, self.mqtt_port)
        print("Connected to MQTT Broker!")
        assert self.mqtt_topic_subscribe is not None
        client.subscribe(self.mqtt_topic_subscribe)
        client.loop_forever()

    @abstractmethod
    def _work_load(self, client: Client, userdata: Optional[None], msg: MQTTMessage) -> None:
        """
        function executed every time a new message is received from the MQTT broker
            Parameters:
                client (Client): the client instance for this callback
                userdata (NoneType): the private user data as set in Client() or user_data_set()
                msg (MQTTMessage): the received message.
        """

    def _on_connect_fail(self, client: Client, userdata: Optional[None]) -> None:
        """
        function executed to control connection attempts with the MQTT broker
        Parameters:
            client (Client): the client instance for this callback
            userdata (NoneType): the private user data as set in Client() or user_data_set()
            msg (MQTTMessage): the received message.
        """
        self.count_connections += 1
        print(f"Reconecting from MQTT Broker! atempt: {self.count_connections}")
        if self.count_connections >= self.mqtt_max_connections:
            client.loop_stop()
            client.disconnect()
            print("Disconnected from MQTT Broker!")
