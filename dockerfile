# Use uma imagem pequena do Python 3.11.9 como construtor 
FROM python:3.11.9-slim AS builder

# Configurar o diretório de trabalho no contêiner
WORKDIR /app

# Copiar os arquivos do projeto para o diretório de trabalho
COPY vision/ ./vision
COPY pyproject.toml .

# Instalar dependências do sistema operacional - a biblioteca libGL necessária para o OpenCV
RUN apt-get update \
    && apt-get install -y libgl1-mesa-glx \
    && apt-get install -y libglib2.0-0 

# Instalar o Poetry e instalar dependências do projeto sem criar um virtualenv
RUN pip install  poetry \
    && poetry install --no-root --no-interaction --no-ansi 

# Baixar os modelos do Retina Face
RUN poetry run python vision/components/vision/download_retina_face_model.py

# Use uma imagem pequena do Python 3.11.9 para a execução 
FROM python:3.11.9-slim

# Copie os dados do construtor para a execução
COPY --from=builder /app/ /app/

# definir variáveis de ambiente para o MQTT
ENV MQTT_HOST=172.30.30.52 \
    MQTT_MOSQUITTO_TLS_PORT=1884 \
    MQTT_MAX_CONNECTIONS=3 \
    MQTT_TOPIC_VISION_SUBSCRIBE=env1234541/vision \
    MQTT_TOPIC_VISION_PUBLISH=env1234541/devices

# Comando para executar a aplicação
CMD ["poetry","run","python","-m","vision"]