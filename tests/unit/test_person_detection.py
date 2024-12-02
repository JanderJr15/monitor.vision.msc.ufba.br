import pytest
import cv2
import requests
import numpy as np
from vision.components.vision.person_detection import PersonDetector

class TestPersonDetector:

    def fetch_image_from_url(self, url):
        """
        Fetch an image from a given URL.

        GIVEN: A URL pointing to an image.
        WHEN: The URL is requested.
        THEN: Return the image as a NumPy array, or skip the test if fetching fails.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad responses
            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(image_array, -1)
            return frame
        except Exception as e:
            pytest.skip(f"Failed to fetch image from {url}: {e}")
    
    @pytest.fixture
    def detector(self):
        """
        Set up the PersonDetector fixture.

        GIVEN: The model path for the PersonDetector.
        WHEN: The fixture is used.
        THEN: Initialize and return the PersonDetector.
        """
        model_path = "vision/models/yolov9c.pt"
        return PersonDetector(model_path)

    def test_one_person_detection_close_angle(self, detector):
        """
        Test detection of one person in a close-angle image.

        GIVEN: An image with one person taken at a close angle.
        WHEN: The image is passed to the PersonDetector.
        THEN: Assert that one person is detected.
        """
        test_image_path = "vision/id_db/images/mayki.1.jpg"
        frame = cv2.imread(test_image_path)

        result = detector.count(frame)

        assert result == 1

    def test_one_person_detection_wide_angle(self, detector):
        """
        Test detection of one person in a wide-angle image.

        GIVEN: A URL to an image with one person taken at a wide angle.
        WHEN: The image is fetched and passed to the PersonDetector.
        THEN: Assert that one person is detected.
        """
        web_image_url = "https://drive.google.com/file/d/13DEkxSaE31Lbwur0BusC_T1tXtyJcDDU/view?usp=sharing"
        frame = self.fetch_image_from_url(web_image_url)

        result = detector.count(frame)

        assert result == 1

    def test_two_person_detection_close_angle(self, detector):
        """
        Test detection of two people in a close-angle image.

        GIVEN: A URL to an image with two people taken at a close angle.
        WHEN: The image is fetched and passed to the PersonDetector.
        THEN: Assert that two people are detected.
        """
        web_image_url = "https://drive.usercontent.google.com/download?id=1AlHK8WLaKR1ETJVXdCGOTma1JZqFtGa3&export=view&authuser=0"
        frame = self.fetch_image_from_url(web_image_url)

        result = detector.count(frame)

        assert result == 2

    def test_two_person_detection_wide_angle(self, detector):
        """
        Test detection of two people in a wide-angle image.

        GIVEN: A URL to an image with two people taken at a wide angle.
        WHEN: The image is fetched and passed to the PersonDetector.
        THEN: Assert that two people are detected.
        """
        web_image_url = "https://drive.usercontent.google.com/download?id=1iRnlDEurcOvOhFuvBcMSmcoCB5NXLf6v"
        frame = self.fetch_image_from_url(web_image_url)

        result = detector.count(frame)

        assert result == 2

    def test_empty_room(self, detector):
        """
        Test detection in an empty room image.

        GIVEN: A URL to an image of an empty room.
        WHEN: The image is fetched and passed to the PersonDetector.
        THEN: Assert that no people are detected.
        """
        web_image_url = (
            "https://img.freepik.com/free-photo/modern-empty-room_23-2150528594.jpg?w=1480&t=st"
            "=1718491056~exp=1718491656~hmac=f9333c746c1a54156801467f3a43e966144ffe10813ea933c1be6716b6b0dc4f"
        )
        frame = self.fetch_image_from_url(web_image_url)

        result = detector.count(frame)

        assert result == 0

    def test_carnaval_police(self, detector):
        """
        Test detection in an image of a crowded scene (Carnival with police).

        GIVEN: A URL to an image with many people (Carnival scene).
        WHEN: The image is fetched and passed to the PersonDetector.
        THEN: Assert that more than 10 people are detected.
        """
        web_image_url = (
            "https://api.radiosalvadorfm.com.br/fotos/gcma_noticias/126665/IMAGEM_NOTICIA_1.jpg?v"
            "=f7abebe4087b21a7eef05694cdbb8f98"
        )
        frame = self.fetch_image_from_url(web_image_url)

        result = detector.count(frame)

        assert result > 10

    def test_soccer_national_anthem(self, detector):
        """
        Test detection in an image of a soccer national anthem.

        GIVEN: A URL to an image with exactly 12 people (soccer team).
        WHEN: The image is fetched and passed to the PersonDetector.
        THEN: Assert that 12 people are detected.
        """
        web_image_url = "https://media.gazetadopovo.com.br/2012/09/90a2c66a745a3b21f72a9a4287898783-gpLarge.jpg"
        frame = self.fetch_image_from_url(web_image_url)

        result = detector.count(frame)

        assert result == 12