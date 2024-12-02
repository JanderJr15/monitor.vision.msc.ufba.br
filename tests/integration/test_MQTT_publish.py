import json
import pytest
from paho.mqtt import publish as mqtt_publish
import requests

class TestFixtures:

    @staticmethod
    def mqtt_topic():
        return "visao"

    @staticmethod
    def mqtt_host():
        return "192.168.1.171"

    @staticmethod
    def dados_tipo_4():
        return {
            "device": "SALA_CAMERA_01",
            "devId": "disp009osdff95osd9fd098s",
            "productKey": "fs09s0d5s0",
            "space": "SALA",
            "message": {
                "status": {
                    "code": "url",
                    "t": 1712138400.0,
                    "value": "https://drive.google.com/file/d/13DEkxSaE31Lbwur0BusC_T1tXtyJcDDU/view?usp=sharing",
                },
                "sensorType": "camera",
                "timeStamp": "2024-04-03 07:00:00.234360",
            },
        }

    @staticmethod
    def imagem_tipo_3():
        return {
            "device": "SALA_CAMERA_01",
            "devId": "disp0990sdf09s90sdf098s",
            "productKey": "fs0s0sd9ss9",
            "space": "SALA",
            "message": {
                "status": [
                    {
                        "code": "url",
                        "t": 1712138400.0,
                        "value": "https://drive.usercontent.google.com/download?id=1PKI_L6_ec5G8MpDxyPRMGfjkIH_RTeAS",
                    }
                ],
                "sensorType": "camera",
                "timeStamp": "2024-04-03 07:00:00.233460",
            },
        }

    @staticmethod
    def imagem_tipo_2():
        return {
            "device": "SALA_CAMERA_01",
            "devId": "disp0990sdf09s90sdf098s",
            "productKey": "fs0s0sd9ss9",
            "space": "SALA",
            "message": {
                "status": [
                    {
                        "code": "url",
                        "t": 1712138400.0,
                        "value": "https://drive.usercontent.google.com/download?id=1iRnlDEurcOvOhFuvBcMSmcoCB5NXLf6v",
                    }
                ],
                "sensorType": "camera",
                "timeStamp": "2024-04-03 07:00:00.233460",
            },
        }

    @staticmethod
    def imagem_drive_camera_computador_lab():
        return {
            "device": "SALA_CAMERA_01",
            "devId": "disp0990sdf09s90sdf098s",
            "productKey": "fs0s0sd9ss9",
            "space": "SALA",
            "message": {
                "status": [
                    {
                        "code": "url",
                        "t": 1712138400.0,
                        "value": "https://drive.usercontent.google.com/download?id=1AlHK8WLaKR1ETJVXdCGOTma1JZqFtGa3&export=view&authuser=0",
                    }
                ],
                "sensorType": "camera",
                "timeStamp": "2024-04-03 07:00:00.233460",
            },
        }

    @staticmethod
    def dado_json(dados_tipo_4):
        return json.dumps(dados_tipo_4)

class TestMQTTIntegration:

    def setup_method(self):
        testFixtures = TestFixtures()
        self.mqtt_topic = testFixtures.mqtt_topic()
        self.mqtt_host = testFixtures.mqtt_host()
        self.dados_tipo_4 = testFixtures.dados_tipo_4()
        self.imagem_tipo_3 = testFixtures.imagem_tipo_3()
        self.imagem_tipo_2 = testFixtures.imagem_tipo_2()
        self.imagem_drive_camera_computador_lab = testFixtures.imagem_drive_camera_computador_lab()
        self.dado_json = testFixtures.dado_json(self.dados_tipo_4)
        self.imagem_fixture = [self.dados_tipo_4, self.imagem_tipo_2, self.imagem_drive_camera_computador_lab]

    def test_envio_mensagem_mqtt(self, mocker):
        dados_imagem = self.imagem_fixture
        self.dado_json = json.dumps(dados_imagem)

        mock_publish_single = mocker.patch("paho.mqtt.publish.single")

        def enviar_mensagem_mqtt(topic, payload, hostname):
            mqtt_publish.single(topic, payload, hostname=hostname)

        enviar_mensagem_mqtt(self.mqtt_topic, self.dado_json, self.mqtt_host)

        mock_publish_single.assert_called_once_with(
            self.mqtt_topic, self.dado_json, hostname=self.mqtt_host
        )

    def test_requests_status_ok(self):
        urls = [dados_imagem["message"]["status"][0]["value"] if isinstance(dados_imagem["message"]["status"], list) else dados_imagem["message"]["status"]["value"] for dados_imagem in self.imagem_fixture]
        responses = [requests.get(url) for url in urls]

        assert all(response.status_code == 200 for response in responses)

    def test_requests_status_not_ok(self):
        dados_imagem = self.imagem_tipo_3
        url = dados_imagem["message"]["status"][0]["value"] if isinstance(dados_imagem["message"]["status"], list) else dados_imagem["message"]["status"]["value"]

        with pytest.raises(AssertionError):
            response = requests.get(url)
            assert (
                response.status_code == 200
            ), f"Expected a non-200 status code, got {response.status_code}"