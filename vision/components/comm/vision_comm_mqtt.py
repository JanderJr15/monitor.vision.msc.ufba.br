"""MQTT client for connecting to a broker, subscribing to topics, and publishing messages."""
from typing import Any, Optional

import json

from paho.mqtt import publish
from paho.mqtt.client import Client, MQTTMessage

from vision.components.comm.mqtt_comm import MqttComm
from vision.components.vision.image_processing import ImageProcessing


class VisionCommMqtt(MqttComm):
    """
        This class extends the paho-mqtt Client class and includes additional functionality
        for managing connection attempts and loading images from various sources.

        Attributes:
            config (dict): Configuration dictionary containing MQTT settings.
            count_connections (int): Counter for the number of connection attempts.
            state (dict): Dictionary to hold the current state information.
        """

    config: dict
    """Configuration dictionary containing MQTT settings."""

    count_connections: int
    """Counter for the number of connection attempts."""

    state: dict
    """Dictionary to hold the current state information."""

    def __init__(self):
        super().__init__()
        self.state = {}
        self.image_processing = ImageProcessing()

    def _work_load(self, client: Client, userdata: Optional[None], msg: MQTTMessage) -> None:
        """
        Callback function for handling incoming MQTT messages.

        This function is triggered when a message is received on the
        subscribed topic. It loads the image from the URL provided in
        the message, performs detection and recognition tasks, and publishes the
        results back to the MQTT broker if there are changes in the state.

        Args:
            client (MQTTClient): The MQTT client instance.
            userdata: Private user data. User-defined data of
                      any type that is passed to callbacks.
            msg: The MQTT message received from the broker.
        """
        request = json.loads(msg.payload.decode('utf-8'))

        img = self.image_processing.load_image_from_source(request['message']['status'][0]['value'])

        if img is not None:
            new_state = self.image_processing.process(img)

            if new_state != self.state:
                self.state = new_state.copy()
                response = self.image_processing.build_message(request, new_state)
                self.publish(json.dumps(response))

    def publish(self, data: Any) -> None:
        """
        Publishes data to the MQTT topic.
        Args:
            data (Any): The data to publish.
            Raises: ValueError: If the MQTT publish topic is not defined.
        """
        if not self.mqtt_topic_publish:
            raise ValueError("MQTT publish topic is not defined")

        publish.single(self.mqtt_topic_publish, data, hostname=self.mqtt_host, port=self.mqtt_port)
