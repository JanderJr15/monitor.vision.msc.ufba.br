"""communication module"""
from abc import ABC, abstractmethod
from typing import Optional

from paho.mqtt.client import Client, MQTTMessage


class CommunicationBase(ABC): # pylint: disable=too-few-public-methods
    """abstract class that defines the standard connection functions"""

    @abstractmethod
    def subiscribe(self) -> None:
        """subscribe function"""

    @abstractmethod
    def _work_load(self, client: Client, userdata: Optional[None], msg: MQTTMessage) -> None:
        """subscribe function"""

    @abstractmethod
    def _on_connect_fail(self, client: Client, userdata: Optional[None]) -> None:
        """subscribe function"""
