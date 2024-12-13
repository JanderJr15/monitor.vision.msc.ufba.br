import os
import psutil
import json
import threading
import time
import paho.mqtt.client as mqtt


MQTT_HOST = "localhost"
MQTT_PORT = 1884
MQTT_TOPIC = "env1234541/monitor/vision"


class TaskMetrics:
    def __init__(self, task_name=None, mqtt_host=MQTT_HOST, mqtt_port=MQTT_PORT, mqtt_topic=MQTT_TOPIC, interval=5):
        """
        Inicializa a instância do Monitor.

        :param task_name: nome da aplicação ou script a ser monitorado.
        :param mqtt_host: nome do host do broker MQTT.
        :param mqtt_port: porta do broker MQTT.
        :param mqtt_topic: tópico MQTT para publicação de métricas.
        :param interval: Intervalo de monitoramento em segundos.
        """
        self.task_name = task_name or os.path.basename(__file__)
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic
        self.interval = interval
        self.mqtt_client = mqtt.Client()
        self.process = psutil.Process(os.getpid())  # Monitor the current process
        self.running = False

    def connect_mqtt(self):
        """Connect on MQTT broker."""
        try:
            self.mqtt_client.connect(self.mqtt_host, self.mqtt_port)
            print(f"Conectado ao broker MQTT em {self.mqtt_host}:{self.mqtt_port}")
        except Exception as e:
            print(f"Falhou ao se conectar ao broker: {e}")

    def collect_and_publish_metrics(self):
        """Coleta e publica metricas do processo atual."""
        while self.running:
            try:
                cpu_usage = self.process.cpu_percent(interval=1)
                memory_usage = self.process.memory_info().rss
                message = {
                    "task_name": self.task_name,
                    "pid": self.process.pid,
                    "cpu_usage": cpu_usage,
                    "memory_usage": memory_usage
                }
                self.mqtt_client.publish(self.mqtt_topic, json.dumps(message))

                print(f"Metricas publicadas para {self.mqtt_topic}: {message}")
            except Exception as e:
                print(f"Erro ao coletar as metricas: {e}")
            time.sleep(self.interval)

    def start(self):
        """Comeca a monitorar o processo atual."""
        self.running = True
        self.connect_mqtt()
        monitor_thread = threading.Thread(target=self.collect_and_publish_metrics, daemon=True)
        monitor_thread.start()

    def stop(self):
        """Para monitoramento."""
        self.running = False
