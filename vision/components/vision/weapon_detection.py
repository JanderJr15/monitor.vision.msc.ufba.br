"""
Weapon detection module for the computer vision system.

This module uses the YOLO model to detect weapons in images.
"""
import numpy as np
from ultralytics import YOLO
import cv2


class WeaponDetector:
    """
    Weapon detector using the YOLO model to identify firearms in an image.

    This class uses a pre-trained YOLO model to detect firearms in the provided image frame
    with a minimum confidence threshold of 0.59.

    Attributes:
        pose_model (YOLO): YOLO model used for pose estimation.
        weapon_model (YOLO): YOLO model used for weapon detection.
        conf (float): Confidence threshold for weapon detection.

    Methods:
        __init__(config: dict) -> None: Initialize the WeaponDetector with the given configuration.
        boxes(frame: np.ndarray) -> list: Get bounding boxes for detected weapons
                                          in the image frame.
        keypoints(frame: np.ndarray) -> list: Get keypoints for detected people
                                              in the image frame.
        plot(frame: np.ndarray) -> np.ndarray: Annotate the image with detected
                                               weapons and keypoints.
        alert(frame: np.ndarray) -> bool: Check if any weapons are detected in the image frame.
    """

    #YOLO model used for pose estimation.
    pose_model: YOLO

    #YOLO model used for weapon detection.
    weapon_model: YOLO

    def __init__(self, config: dict) -> None:
        """
        Initialize the WeaponDetector with the given configuration.

        Args:
            config (dict): Configuration dictionary containing paths to the YOLO models.
                - POSE_ESTIMATION_MODEL (str): Path to the YOLO model for pose estimation.
                - WEAPON_DETECTION_MODEL (str): Path to the YOLO model for weapon detection.
        """
        self.pose_model = YOLO(config['POSE_ESTIMATION_MODEL'])
        self.weapon_model = YOLO(config['WEAPON_DETECTION_MODEL'])
        self.conf = 0.439

    def boxes(self, frame: np.ndarray) -> list:
        """
        Get bounding boxes for detected weapons in the image frame.

        Args:
            frame (np.ndarray): The image frame to be analyzed.

        Returns:
            list: A list of bounding boxes for detected weapons.
        """
        imgsz = min(max(frame.shape[0], frame.shape[1]), 4000)
        imgsz -= imgsz % 32

        results = self.weapon_model(frame, imgsz=imgsz, conf=self.conf,
                                    iou=0.3, verbose=False)[0].boxes
        results = [x[0] + [x[1]] for x in zip(results.xyxyn.cpu().tolist(),
                                              results.conf.cpu().tolist())]
        keypoints = self.keypoints(frame)

        boxes = []
        for detection in results:
            for keypoint in keypoints:
                if (detection[0] <= keypoint[0] <= detection[2] and
                        detection[1] <= keypoint[1] <= detection[3]):
                    boxes.append(detection)
                    break

        return boxes

    def keypoints(self, frame: np.ndarray) -> list:
        """
         Get keypoints for detected people in the image frame.

         Args:
             frame (np.ndarray): The image frame to be analyzed.

         Returns:
             list: A list of keypoints for detected people.
         """
        results = self.pose_model(frame, verbose=False)[0].keypoints.xyn.cpu().tolist()
        hand_keypoints = []
        ratio = 0.3

        for person in results:
            if person:
                hand1 = [person[9][0] + (person[9][0] - person[7][0]) *
                         ratio, person[9][1] + (person[9][1] - person[7][1]) * ratio]
                hand2 = [person[10][0] + (person[10][0] - person[8][0]) *
                         ratio, person[10][1] + (person[10][1] - person[8][1]) * ratio]
                hand_keypoints.append(hand1)
                hand_keypoints.append(hand2)

        return hand_keypoints

    def plot(self, frame: np.ndarray) -> np.ndarray:
        """
        Annotate the image with detected weapons and keypoints.

        Args:
            frame (np.ndarray): The image frame to be annotated.

        Returns:
            np.ndarray: The annotated image frame.
        """
        boxes = self.boxes(frame)
        keypoints = self.keypoints(frame)

        height = frame.shape[0]
        width = frame.shape[1]

        for box in boxes:
            pt1 = (round(box[0] * width), round(box[1] * height))
            pt2 = (round(box[2] * width), round(box[3] * height))
            frame = cv2.rectangle(frame, pt1, pt2, (0, 0, 255), 10)

        for keypoint in keypoints:
            center = (round(keypoint[0] * width), round(keypoint[1] * height))
            frame = cv2.circle(frame, center, 20, (0, 255, 0), -1)

        return frame

    def alert(self, frame):
        """
        Check if any weapons are detected in the image frame.

        Args:
            frame (np.ndarray): The image frame to be analyzed.

        Returns:
            bool: True if weapons are detected, False otherwise.
        """
        return len(self.boxes(frame)) > 0
