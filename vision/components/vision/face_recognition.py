"""
Facial recognition module for the computer vision system.

This module uses the DeepFace and RetinaFace libraries to recognize faces in images.
"""
import os

import numpy as np
import cv2

from deepface import DeepFace
from retinaface import RetinaFace


class FaceRecognition:
    """
    Face recognition system using RetinaFace for face detection and DeepFace for face recognition.

    This class updates a database of known faces and performs face recognition on input images.

    Attributes:
        images_path (str): Path to the reference images.
        crops_path (str): Path to the face crops.

    Methods:
        __call__(img: np.ndarray) -> list: Perform facial recognition on the provided image.
        update_db() -> None: Update the face database.
    """

    images_path: str
    """Path to the directory containing images for face database."""

    crops_path: str
    """Path to the directory where cropped face images are stored."""

    def __init__(self, images_path: str, crops_path: str) -> None:
        """
        Initialize the FaceRecognition with paths to images and face crops.

        Args:
            images_path (str): Path to the directory containing images for face database.
            crops_path (str): Path to the directory where cropped face images are stored.
        """
        self.images_path = images_path
        self.crops_path = crops_path
        self.update_db()

    def __call__(self, img: np.ndarray) -> list:
        """
        Perform facial recognition on the provided image.

        Args:
            img (np.ndarray): Image in which faces will be recognized.

        Returns:
            list: A sorted list of names of recognized individuals.
        """
        names = []
        try:
            faces = RetinaFace.extract_faces(img)

            for face in faces:
                face = face[:, :, ::-1]  # Convert BGR to RGB

                result = DeepFace.find(face, self.crops_path,
                                       enforce_detection=False,
                                       silent=True,
                                       align=False)[0]
                if not result.empty:
                    name = result.iloc[0]['identity'].split(sep='/')[-1].split(sep='.')[0]
                    names.append(name)
        except:
            print("Erro aqui!!")

        return sorted(names)

    def update_db(self):
        """
        Update the face database by extracting and saving cropped faces.

        This method reads images from `images_path`, detects faces using RetinaFace, and saves the
        cropped face images to `crops_path` if they are not already present.

        Notes:
            The line cv2.imwrite(os.path.join(self.crops_path, file), crop[:, :, ::-1])
            saves the cropped face image in BGR format, which is the standard format used by OpenCV.
             The [:, :, ::-1] operation converts the image from RGB to BGR before saving.
        """
        images = os.listdir(self.images_path)
        crops = os.listdir(self.crops_path)

        for file in images:
            if file not in crops:
                img = cv2.imread(os.path.join(self.images_path, file))
                crop = RetinaFace.extract_faces(img)[0]
                cv2.imwrite(os.path.join(self.crops_path, file), crop[:, :, ::-1])
