import pytest
import cv2
import numpy as np
import requests
import os
from vision.components.vision.face_recognition import FaceRecognition

class TestFaceRecognition:

    def fetch_image_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(image_array, -1)
            return frame
        except Exception as e:
            pytest.skip(f"Failed to fetch image from {url}: {e}")

    @pytest.fixture(autouse=True)
    def setup_method(self):
        images_path = "vision/id_db/images"
        crops_path = "vision/id_db/crops"
        self.face_recognition = FaceRecognition(images_path, crops_path)
        self.images_path = images_path

    @pytest.mark.parametrize("image_name, expected_name", [
        ("Eduardo.1.jpg", "Eduardo"),
        ("Eduardo.2.jpg", "Eduardo"),
        ("Eduardo.3.jpg", "Eduardo"),
        ("Eduardo.4.jpg", "Eduardo"),
        ("mayki.1.jpg", "mayki"),
        ("mayki.2.jpg", "mayki"),
        ("mayki.3.jpg", "mayki"),
        ("mayki.4.jpg", "mayki")
    ])
    def test_load_and_test_image(self, image_name, expected_name):
        sample_image_path = os.path.join(self.images_path, image_name)
        assert os.path.exists(sample_image_path), f"Sample image '{sample_image_path}' not found."

        sample_image = cv2.imread(sample_image_path)
        recognized_names = self.face_recognition(sample_image)
        assert isinstance(recognized_names, list)
        base_names = [os.path.basename(name) for name in recognized_names]
        assert expected_name in base_names if expected_name else len(recognized_names) == 0

    def test_face_recognition_unrecognized_person(self):
        unrecognized_image = self.fetch_image_from_url("https://thispersondoesnotexist.com")
        recognized_names = self.face_recognition(unrecognized_image)
        assert isinstance(recognized_names, list)
        assert len(recognized_names) == 0

    def test_face_recognition_eduardo_mayki(self):
        image_url = "https://drive.usercontent.google.com/download?id=1iRnlDEurcOvOhFuvBcMSmcoCB5NXLf6v"
        combined_image = self.fetch_image_from_url(image_url)
        recognized_names = self.face_recognition(combined_image)
        assert isinstance(recognized_names, list)
        assert len(recognized_names) == 2
        expected_names = ["Eduardo", "mayki"]
        base_names = [os.path.basename(name).split(".")[0] for name in recognized_names]
        assert all(name in base_names for name in expected_names)
