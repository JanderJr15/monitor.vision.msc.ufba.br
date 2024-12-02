import sys
sys.path.append('/app')

import yaml

from vision.components.vision.face_recognition import FaceRecognition

with open('vision/components/config.yaml', 'r', encoding="utf-8") as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)

face_recognition = FaceRecognition(config['FACE_RECOGNITION_IMAGES'],
                                                config['FACE_RECOGNITION_CROPS'])

result = face_recognition("vision/id_db/images/mayki.2.jpg")