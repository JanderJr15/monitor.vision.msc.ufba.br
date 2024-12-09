import psutil
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


class TaskMetrics:
    def __init__(self, task_name, monitor_url):
        """
        Inicializa o módulo de métricas.

        :param task_name: Nome ou identificação da tarefa
        :param monitor_url: URL do módulo monitor (Prometheus Pushgateway)
        """
        self.cpu_usage1 = Gauge("script_cpu_usage_percent", "CPU usage of the script in percent")

        self.task_name = task_name
        self.monitor_url = monitor_url
        self.registry = CollectorRegistry()
        self.cpu_gauge = Gauge(
            f'{task_name}_cpu_usage',
            'CPU usage of the task in percentage',
            registry=self.registry
        )
        self.memory_gauge = Gauge(
            f'{task_name}_memory_usage',
            'Memory usage of the task in bytes',
            registry=self.registry
        )

    def collect_metrics(self):
        """
        Coleta as métricas de CPU e memória da tarefa.
        """
        try:

            # Coleta informações do processo pela identificação do nome
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                print(proc)
                if self.task_name in proc.info['name']:
                    cpu_usage = proc.info['cpu_percent']
                    memory_usage = proc.info['memory_info'].rss  # RSS (Resident Set Size)
                    # cpu_usage1 = proc.cpu_percent(interval=1)
                    print(cpu_usage, memory_usage)
                    # Atualiza os valores das métricas
                    # self.cpu_usage1.set(process.cpu_percent(interval=1))
                    self.cpu_gauge.set(cpu_usage)
                    self.memory_gauge.set(memory_usage)
                    return cpu_usage, memory_usage
        except Exception as e:
            print(f"Erro ao coletar métricas: {e}")
        return None, None

    def push_metrics(self):
        """
        Envia as métricas coletadas para o módulo monitor.
        """
        try:
            push_to_gateway(self.monitor_url, job=self.task_name, registry=self.registry)
            print(f"Métricas enviadas com sucesso para {self.monitor_url}.")
        except Exception as e:
            print(f"Erro ao enviar métricas: {e}")


# Exemplo de uso
if __name__ == "__main__":
    # Nome da tarefa (por exemplo, "Task 1") e URL do monitor (Prometheus Pushgateway)
    task_name = "mjpg_streamer"
    tasks = ["mjpg_streamer", "kworker/u17:3-uvcvideo", "python"]
    monitor_url = "http://localhost:9091"

    # Instância do monitor de métricas
    task_metrics = TaskMetrics(task_name, monitor_url)

    # Coleta e envia métricas em loop (simulando monitoramento contínuo)
    import time

    while True:
        cpu, memory = task_metrics.collect_metrics()
        if cpu is not None:
            print(f"CPU: {cpu}%, Memória: {memory} bytes")
            task_metrics.push_metrics()
        else:
            print("Tarefa não encontrada.")
        time.sleep(5)  # Intervalo entre as coletas
