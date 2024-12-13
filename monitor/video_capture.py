import cv2
import json
import time
import os
from prometheus_client import start_http_server, Gauge
import paho.mqtt.publish as publish
from vision.components.vision import image_processing
from mjpeg_streamer import MjpegServer, Stream
from start_streamer import start_mjpg_streamer
from monitor.get_ip_address import NetworkUtils
from task_monitor import TaskMetrics
# from dotenv import load_dotenv

# load_dotenv()

MQTT_HOST   = 'localhost'
MQTT_PORT   =  1884
MQTT_TOPIC  = 'env1234541/devices'

monitor = TaskMetrics(task_name="video_capture.py", interval=5)
monitor.start()

IP_ADDRESS = NetworkUtils.get_local_ip()
start_mjpg_streamer()
time.sleep(5)

# URL do stream
stream_url = f"http://{IP_ADDRESS}:8080/?action=stream"

# Global variable
publish_count = 0  # Count published messages
MSG_ANTERIOR = None  # Last Message published on MQTT

WIDTH = 640
LENGTH = 480
FPS = 1
# Start Image processor
image_processor = image_processing.ImageProcessing()

# Start Prometheus Server on 8000 port
# start_http_server(8000)

stream = Stream(f"Camera_001-ip-{IP_ADDRESS}", size=(WIDTH, LENGTH), quality=50, fps=FPS)
server = MjpegServer("localhost", 8080)
server.add_stream(stream)
server.start()


def capture_frames_from_stream(url: str):
    """
    Captura quadros em tempo real de um stream de vídeo.

    Args:
        url (str): URL do stream.

    Yields:
        np.ndarray: Captured Frames as NumPy arrays.
    """
    cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)  # Força FFMPEG para leitura

    if not cap.isOpened():
        print(f"Error opening the stream: {url}")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture stream frame.")
            break
        yield frame

    cap.release()

# Frames processing
for frame in capture_frames_from_stream(stream_url):
    start_time = time.time()  # Início da medição do tempo
    resized_frame = cv2.resize(frame, (WIDTH, LENGTH))  # Ajuste para a resolução desejada

    # Mostrar o stream em tempo real (opcional para debug)
    # cv2.imshow(stream.name, frame)

    state = image_processor.process(frame)

    # Cria mensagem para o MQTT
    request = {
        "device": "SALA_CAMERA_01",
        "devId": "disp0990sdf09s90sdf098s",
        "productKey": "fs0s0sd9ss9",
        "space": "SALA",
        "message": {"status": [{"code": "stream", "value": "real-time"}]},
        "sensorType": "camera",
        "timeStamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "machine": f"{IP_ADDRESS}"
    }
    message = image_processor.build_message(request, state)
    dado_json = json.dumps(message)

    try:
        if MSG_ANTERIOR != dado_json:
            MSG_ANTERIOR = dado_json
            publish.single(MQTT_TOPIC, dado_json, hostname=MQTT_HOST, port=MQTT_PORT)
            publish_count += 1  # Incrementa o contador de publicações
            print("Message published successfully:", dado_json)
    except Exception as e:
        print(f"Error publishing to MQTT: {e}")

    cycle_time = time.time() - start_time
    print(f"Frame processing time: {cycle_time:.4f} seconds")

    # Finish if press 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

monitor.stop()  # Stop monitoring on exit
