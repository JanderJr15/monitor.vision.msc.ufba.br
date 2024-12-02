# import cv2
# import json, os
# import paho.mqtt.publish as publish
# from vision.components.vision import image_processing
#
# from prometheus_client import start_http_server, Gauge
# import psutil
# import time
# import threading
#
# stream_url = "http://localhost:8090/?action=stream"
#
#
# # Criando métricas com Prometheus
# cpu_usage = Gauge("script_cpu_usage_percent", "CPU usage of the script in percent")
# memory_usage = Gauge("script_memory_usage_mb", "Memory usage of the script in MB")
# mqtt_publish_count = Gauge("mqtt_publish_count", "Number of MQTT messages published")
# #
# publish_count = 0  # Contador para mensagens publicadas
#
# # Initialize the image processor
# image_processor = image_processing.ImageProcessing()
#
# MQTT_HOST = "192.168.1.192"
# MQTT_PORT = 1884
# MQTT_TOPIC = "env1234541/devices"
# MSG_ANTERIOR = None
#
# start_http_server(8000)  # Exemplo: Prometheus coleta as métricas na porta 8000
#
#
#
# def collect_metrics():
#     """Função que coleta métricas do sistema periodicamente."""
#     while True:
#         # Coleta o uso de CPU e memória do processo atual
#         process = psutil.Process()
#         cpu_usage.set(process.cpu_percent(interval=1))
#         memory_usage.set(process.memory_info().rss / (1024 * 1024))  # Em MB
#         # mqtt_publish_count.set(publish_count)
#
#         time.sleep(1)
#
# def capture_frames_from_stream(url: str):
#     """
#     Captura quadros em tempo real de um stream de vídeo.
#
#     Args:
#         url (str): URL do stream.
#
#     Yields:
#         np.ndarray: Quadros capturados como arrays NumPy.
#     """
#     cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)  # Forçar FFMPEG
#     if not cap.isOpened():
#         print(f"Erro ao abrir o stream: {url}")
#         return
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Erro ao capturar quadro do stream.")
#             break
#         yield frame
#
#     cap.release()
#
#
# # Captura e processamento
# for frame in capture_frames_from_stream(stream_url):
#     # Mostrar o stream em tempo real
#     cv2.imshow("Stream", frame)
#
#     # Processar o quadro
#     state = image_processor.process(frame)
#
#     # Criar mensagem com base no estado processado
#     request = {
#         "device": "SALA_CAMERA_01",
#         "devId": "disp0990sdf09s90sdf098s",
#         "productKey": "fs0s0sd9ss9",
#         "space": "SALA",
#         "message": {"status": [{"code": "stream", "value": "real-time"}]},
#         "sensorType": "camera",
#         "timeStamp": "2024-04-03 07:00:00.233460"
#     }
#     message = image_processor.build_message(request, state)
#
#     # Publicar mensagem no tópico MQTT
#     dado_json = json.dumps(message)
#     # start_http_server(8000)  # Exemplo: Prometheus coleta as métricas na porta 8000
#     # metrics_thread = threading.Thread(target=collect_metrics, daemon=True)
#     # metrics_thread.start()
#     try:
#
#         if MSG_ANTERIOR != dado_json:
#             metrics_thread = threading.Thread(target=collect_metrics, daemon=True)
#             metrics_thread.start()
#             MSG_ANTERIOR = dado_json
#             publish.single(MQTT_TOPIC, dado_json, hostname=MQTT_HOST, port=MQTT_PORT)
#             publish_count += 1  # Incrementar o contador de publicações
#             mqtt_publish_count.set(publish_count)
#             print(dado_json)
#             print("Mensagem publicada com sucesso.")
#     except Exception as e:
#         print(f"Erro ao publicar no MQTT: {e}")
#
#     # Finalizar com 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
#
#
# cv2.destroyAllWindows()


import cv2
import json
import time
import psutil
import threading
from prometheus_client import start_http_server, Gauge
import paho.mqtt.publish as publish
from vision.components.vision import image_processing

# URL do stream
stream_url = "http://100.94.101.86:8080/?action=stream"
# stream_url = "http://localhost:8080/?action=stream"

# Criando métricas do Prometheus
cpu_usage = Gauge("script_cpu_usage_percent", "CPU usage of the script in percent")
memory_usage = Gauge("script_memory_usage_mb", "Memory usage of the script in MB")
mqtt_publish_count = Gauge("mqtt_publish_count", "Number of MQTT messages published")
frame_processing_time = Gauge("frame_processing_time", "Time taken to process each frame in seconds")

# global MSG_ANTERIOR, publish_count


# Variáveis globais
publish_count = 0  # Contador para mensagens publicadas
MSG_ANTERIOR = None  # Última mensagem publicada no MQTT

# Inicializa o processador de imagem
image_processor = image_processing.ImageProcessing()

# Configuração MQTT
MQTT_HOST = "192.168.1.192"
MQTT_PORT = 1884
MQTT_TOPIC = "env1234541/devices"

# Iniciar o servidor Prometheus na porta 8000
start_http_server(8000)

def collect_metrics():
    """Coleta métricas do sistema periodicamente."""
    while True:
        process = psutil.Process()
        cpu_usage.set(process.cpu_percent(interval=1))
        memory_usage.set(process.memory_info().rss / (1024 * 1024))  # Memória em MB
        time.sleep(1)  # Coleta de métricas a cada segundo

def capture_frames_from_stream(url: str):
    """
    Captura quadros em tempo real de um stream de vídeo.

    Args:
        url (str): URL do stream.

    Yields:
        np.ndarray: Quadros capturados como arrays NumPy.
    """
    cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)  # Força FFMPEG para leitura
    if not cap.isOpened():
        print(f"Erro ao abrir o stream: {url}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar quadro do stream.")
            break
        yield frame

    cap.release()

# Inicia a coleta de métricas do sistema em uma thread separada
metrics_thread = threading.Thread(target=collect_metrics, daemon=True)
metrics_thread.start()

# Processamento de quadros
for frame in capture_frames_from_stream(stream_url):
    start_time = time.time()  # Início da medição do tempo
    resized_frame = cv2.resize(frame, (640, 360))  # Ajuste para a resolução desejada
    # Mostrar o stream em tempo real (opcional para debug)
    cv2.imshow("Stream", frame)

    # Processa o quadro
    state = image_processor.process(frame)

    # Cria mensagem para o MQTT
    request = {
        "device": "SALA_CAMERA_01",
        "devId": "disp0990sdf09s90sdf098s",
        "productKey": "fs0s0sd9ss9",
        "space": "SALA",
        "message": {"status": [{"code": "stream", "value": "real-time"}]},
        "sensorType": "camera",
        "timeStamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    message = image_processor.build_message(request, state)
    dado_json = json.dumps(message)

    try:
        # Publica no MQTT apenas se a mensagem for diferente da anterior
        # global MSG_ANTERIOR, publish_count
        if MSG_ANTERIOR != dado_json:
            MSG_ANTERIOR = dado_json
            publish.single(MQTT_TOPIC, dado_json, hostname=MQTT_HOST, port=MQTT_PORT)
            publish_count += 1  # Incrementa o contador de publicações
            mqtt_publish_count.set(publish_count)  # Atualiza métrica no Prometheus
            print("Mensagem publicada com sucesso:", dado_json)
    except Exception as e:
        print(f"Erro ao publicar no MQTT: {e}")

    # Tempo de execução do ciclo
    cycle_time = time.time() - start_time
    frame_processing_time.set(cycle_time)  # Atualiza métrica do Prometheus
    print(f"Tempo de processamento do frame: {cycle_time:.4f} segundos")

    # Finaliza se pressionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()



# Tempo de processamento do frame: 4.0917 segundos
# Tempo de processamento do frame: 4.2864 segundos
# Tempo de processamento do frame: 4.4914 segundos
# Tempo de processamento do frame: 4.5541 segundos