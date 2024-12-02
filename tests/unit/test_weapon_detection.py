import pytest
import cv2
import requests
import numpy as np
from vision.components.vision.weapon_detection import WeaponDetector


class TestWeaponDetector:

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
        Set up the WeaponDetector fixture.

        GIVEN: The model path for the WeaponDetector.
        WHEN: The fixture is used.
        THEN: Initialize and return the WeaponDetector.
        """
        config = {'POSE_ESTIMATION_MODEL': "vision/models/yolov8m-pose.pt", 'WEAPON_DETECTION_MODEL': "vision/models/weapon_detector.pt"}
        return WeaponDetector(config)

    def test_weapon_detection_false(self, detector):
        """
        Test for no weapon detection in an image.

        GIVEN: An image with no weapons.
        WHEN: The image is passed to the WeaponDetector.
        THEN: Assert that no weapon is detected.
        """
        test_image_path = "vision/id_db/images/Eduardo.1.jpg"
        frame = cv2.imread(test_image_path)

        result = detector.alert(frame)

        assert result is False

    def test_weapon_detection_true(self, detector):
        """
        Test for weapon detection in an image.

        GIVEN: A URL to an image containing a weapon.
        WHEN: The image is fetched and passed to the WeaponDetector.
        THEN: Assert that a weapon is detected.
        """
        web_image_url = (
            "https://static.independent.co.uk/2023/08/10/11/newFile-6.jpg?quality=75&width=1250&crop=3"
            "%3A2%2Csmart&auto=webp"
        )
        frame = self.fetch_image_from_url(web_image_url)

        result = detector.alert(frame)

        assert result is True

    def test_rifle_detection_true(self, detector):
        """
        Test for rifle detection in an image.

        GIVEN: A URL to an image containing a rifle.
        WHEN: The image is fetched and passed to the WeaponDetector.
        THEN: Assert that a rifle is detected.
        """
        web_image_url = (
            "https://media.cnn.com/api/v1/images/stellar/prod/200120090234-03-virginia-pro-gun-rally"
            "-0120.jpg?q=w_2000,h_1333,x_0,y_0,c_fill"
        )
        frame = self.fetch_image_from_url(web_image_url)

        result = detector.alert(frame)

        assert result is True

    def test_weapon_drawing_detection(self, detector):
        """
        Test for no weapon detection in an image with a drawing of a weapon.

        GIVEN: A URL to an image containing a drawing of a weapon.
        WHEN: The image is fetched and passed to the WeaponDetector.
        THEN: Assert that no weapon is detected.
        """
        web_image_url = "https://s.abcnews.com/images/US/pro-gun-1-gty-er-180324_hpMain_16x9_992.jpg"
        frame = self.fetch_image_from_url(web_image_url)

        result = detector.alert(frame)

        assert result is False

    def test_pistol_robbery_cctv_detection(self, detector):
        """
        Test for pistol detection in a CCTV image of a robbery.

        GIVEN: A URL to a CCTV image containing a pistol during a robbery.
        WHEN: The image is fetched and passed to the WeaponDetector.
        THEN: Assert that a pistol is detected.
        """
        web_image_url = "https://e3.365dm.com/21/10/768x432/skynews-marine-veteran-disarms_5554128.jpg"
        frame = self.fetch_image_from_url(web_image_url)

        result = detector.alert(frame)

        assert result is True

    def test_revolver_robbery_cctv_detection(self, detector):
        """
        Test for revolver detection in a CCTV image of a robbery.

        GIVEN: A URL to a CCTV image containing a revolver during a robbery.
        WHEN: The image is fetched and passed to the WeaponDetector.
        THEN: Assert that a revolver is detected.
        """
        test_image_path = "tests/unit/test_images/garoto_com_revolver.png"
        frame = cv2.imread(test_image_path)

        result = detector.alert(frame)

        assert result is True

    def test_revolver_detection(self, detector):
        """
        Test for revolver detection in an image.

        GIVEN: A URL to an image containing a revolver.
        WHEN: The image is fetched and passed to the WeaponDetector.
        THEN: Assert that a revolver is detected.
        """
        web_image_url = (
            "https://images.tcdn.com.br/img/img_prod/1026992"
            "/rt_941_taurus_cal_22_magnum_578_1_c7a57332b57d754f7e7c53f3a6377c16.jpg"
        )
        frame = self.fetch_image_from_url(web_image_url)

        result = detector.alert(frame)

        assert result is True
