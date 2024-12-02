"""
Person detection module for the computer vision system.

This module uses the YOLO model to detect people in images.
"""
import numpy as np
from ultralytics import YOLO


class PersonDetector:
    """
    Person detector using the YOLO model to count the number of people in an image.

    This class uses the YOLO model to detect people in the provided image frame.

    Attributes:
        model (YOLO): YOLO model for person detection.

    Methods:
        __init__(path: str) -> None: Initialize the PersonDetector with the path to the YOLO model.
        boxes(frame: np.ndarray) -> list: Get bounding boxes for detected people in the image frame.
        count(frame: np.ndarray) -> int: Detect the number of people in the provided image frame.
    """

    model: YOLO
    """YOLO model used for person detection."""

    def __init__(self, path: str) -> None:
        """
        Initialize the PersonDetector with the path to the YOLO model.

        Args:
            path (str): Path to the pre-trained YOLO model.
        """
        self.model = YOLO(path)

    def boxes(self, frame: np.ndarray) -> list:
        """
        Get bounding boxes for detected people in the image frame.

        Args:
            frame (np.ndarray): The image frame to be analyzed.

        Returns:
            list: A list of bounding boxes for detected people.
        """
        results = self.model(frame, classes=[0], verbose=False)[0].boxes

        return results

    def count(self, frame: np.ndarray) -> int:
        """
        Detect the number of people in the provided image frame.

        Args:
            frame (np.ndarray): The image frame in which to detect people.

        Returns:
            int: The number of people detected in the image frame.
        """

        count = len(self.boxes(frame))

        return count
