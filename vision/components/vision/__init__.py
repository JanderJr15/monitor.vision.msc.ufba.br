"""This module receives camera data sent over an MQTT topic,
processes the images, and returns the analyzed results in JSON format."""
from .person_detection import PersonDetector
from .weapon_detection import WeaponDetector
from .face_recognition import FaceRecognition
