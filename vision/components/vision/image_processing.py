"""This module provides the ImageProcessing class, which integrates functionalities
for detecting persons, weapons, and recognizing faces within images."""
import os
import urllib
import re
from typing import Optional, Any

import validators
import numpy as np

import yaml

from cv2 import imdecode, imread

from vision.components.vision.person_detection import PersonDetector
from vision.components.vision.weapon_detection import WeaponDetector
from vision.components.vision.face_recognition import FaceRecognition

from monitor.task_monitor import TaskMetrics




class ImageProcessing:
    """
        Provides functionalities for processing
        images to detect persons, weapons, and recognize faces.

        Attributes:
            person_detector (PersonDetector): The person detection model.
            weapon_detector (WeaponDetector): The weapon detection model.
            face_recognition (FaceRecognition): The face recognition model and image crops.

        Methods:
            process: Processes the image and detects persons, weapons, and recognizes faces.
            build_message: Constructs a message based on detection results.
            load_image_from_source: Loads an image from a local path or a URL.
    """

    def __init__(self) -> None:
        """
            Initializes the ImageProcessing class by loading configuration settings from a YAML file
            and initializing detection models.
        """
        with open(f'../vision/components/config.yaml', 'r', encoding="utf-8") as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)

        self.person_detector = PersonDetector(config['PERSON_DETECTION_MODEL'])
        self.weapon_detector = WeaponDetector(config)
        self.face_recognition = FaceRecognition(config['FACE_RECOGNITION_IMAGES'],
                                                config['FACE_RECOGNITION_CROPS'])

    def process(self, img: np.ndarray) -> dict[str, Any]:
        """
            Processes an image to detect persons, weapons, and recognize faces.

            Args:
                img (np.ndarray): The image to be processed.

            Returns:
                dict: A dictionary containing the detection results.
        """

        new_state = {'n_detected_people': self.person_detector.count(img),
                     'recognized_people': self.face_recognition(img),
                     'weapon_detected': self.weapon_detector.alert(img)}

        monitor_url = "http://localhost:9091"
        # TaskMetrics.collect_metrics(process, monitor_url)

        return new_state

    @staticmethod
    def build_message(request: dict, state: dict) -> dict:
        """
        Build a message payload based on the request and state.

        Args:
            request (dict): The original request dictionary.
            state (dict): The state dictionary containing information about detected and
                          recognized people, and weapon detection status.

        Returns:
            dict: The response message dictionary including status and alert information.

        Constructs a response dictionary by copying the request and adding status and alert
        information based on the state. If a weapon is detected, an alert is added to the response.
        """
        response = request.copy()

        response['message'] = {'status': []}
        response['message']['status'].append({'code': 'quant_pessoas',
                                              'value': state['n_detected_people']})
        response['message']['status'].append({'code': 'conhecidas',
                                              'value': state['recognized_people']})

        if state['weapon_detected']:
            response['alert'] = {'status': []}
            response['alert']['status'].append({'code': 'invasao',
                                                'value': 'pessoa armada detectada'})
            response['alert']['status'].append({'code': 'img',
                                                'value': request['message']['status'][0]['value']})

        return response

    @staticmethod
    def load_image_from_source(path: str) -> Optional[np.ndarray]:
        """
        Load an image from a given file path or URL.

        This function supports loading images from local file paths or URLs. For Google Drive URLs,
        it converts the sharing URL to a direct download URL. It uses the OpenCV function `imdecode`
        to decode the image from the URL response.

        Args:
            path (str): The file path or URL to the image.

        Returns:
            np.ndarray: The loaded image as a NumPy array, or None if an error occurs.

        Raises:
            urllib.error.URLError: If there is an error opening the URL.
            ValueError: If the URL is invalid.
        """
        try:
            if validators.url(path):
                if path.startswith("https://drive.google.com"):
                    match = re.search(r'/file/d/(.*?)/', path)
                    if match is not None:  # Verificar se match não é None antes de acessar group
                        path = f'https://drive.google.com/uc?id={match.group(1)}'
                    else:
                        raise ValueError("Invalid Google Drive URL")
                with urllib.request.urlopen(path) as url_response:
                    img = imdecode(np.array(bytearray(url_response.read()), dtype=np.uint8), -1)

            else:
                img = imread(path)

            return img
        except (urllib.error.URLError, ValueError) as e:
            print(f"Error loading image from source: {e}")
            return None
