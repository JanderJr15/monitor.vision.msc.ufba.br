## 1. Dependências de Serviços

Necessário a instalação do mosquitto e do mosquitto-clients para se inscrever e publicar no container do Mosquitto Broker que será executado com o Docker

```bash
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients
```

## 2. Variáveis de Ambiente

- **MQTT-HOST**: O endereço do host MQTT. Use "localhost" para executar o módulo localmente.
- **MQTT_MOSQUITTO_TLS_PORT**: A porta do para a conexão com TLS. Utilize 1883 por padrão.
- **MQTT_MAX_CONNECTIONS**: Número máximo de tentativas para reconectar. Utilize 3 por padrão
- **MQTT_TOPIC_VISION_SUBSCRIBE**: Tópico MQTT do conteúdo publicado pelos dispositivos, em que as requisições dos dispositivos serão exibidas ao módulo de visão. Utilize "env1234541/vision" por padrão.
- **MQTT_TOPIC_VISION_PUBLISH**: Tópico MQTT do conteúdo publicado pelo módulo de visão, em que as respostas do módulo serão exibidas aos dispositivos. Utilize "env1234541/devices" por padrão.

## 3. Instruções para a Execução do Módulo

Nesta seção, forneça os comandos necessários para criar o container Docker do módulo e executá-lo. 

### Comandos:

1. **Clonar o repositório**:

```bash
git clone https://github.com/Grupo-de-Inteligencia-Aplicada/vision-module.argus.ufba.br
```

- **Explicação**: Este comando clona o repositório Git no seu ambiente local.
- **Resultado esperado**: O código-fonte será copiado para o diretório local.

2. **Buildar o Container**:

```bash
docker build . -t vision-module
```

- **Explicação**: Constrói a imagem Docker para o módulo.
- **Resultado esperado**: Uma imagem Docker será criada com a tag vision-module.

3. **Executar o MQTT Broker**:
   Crie um terminal para o MQTT Broker e execute o seguinte comando:

```bash
docker run -it -p 1883:1883 -p 8080:8080 eclipse-mosquitto
```

- **Explicação**: Executa o container do MQTT Broker na porta 1883. Caso seja a primeira utilização a imagem do eclipse-mosquitto será baixada automaticamente.
- **Resultado esperado**:

```
<timestamp>: mosquitto version 2.0.20 starting
<timestamp>: Config loaded from /mosquitto/config/mosquitto.conf.
<timestamp>: Starting in local only mode. Connections will only be possible from clients running on this machine.
<timestamp>: Create a configuration file which defines a listener to allow remote access.
<timestamp>: For more details see https://mosquitto.org/documentation/authentication-methods/
<timestamp>: Opening ipv4 listen socket on port 1883.
<timestamp>: Opening ipv6 listen socket on port 1883.
<timestamp>: mosquitto version 2.0.20 running
```

4. **Executar o módulo de visão**:
   Crie um terminal para o módulo de visão e execute o seguinte comando:

```bash
docker run --rm --name vision-module -e MQTT_HOST=localhost -e MQTT_MOSQUITTO_TLS_PORT=1883 -e MQTT_MAX_CONNECTIONS=3 -e MQTT_TOPIC_VISION_SUBSCRIBE=env1234541/vision -e MQTT_TOPIC_VISION_PUBLISH=env1234541/devices  --network=host vision-module
```

- **Explicação**: Executa o container do módulo de visão. Nesse ponto, o módulo já está totalmente funcional.
- **Resultado esperado**: O terminal ficará executando o comando sem nenhuma saída.

5. **Inscrever nos tópicos**:
   Crie um terminal para escutar o conteúdo publicado pelos dispositivos:

```bash
mosquitto_sub -h localhost -p 1833 -t env1234541/devices
```

Crie um terminal para escutar o conteúdo publicado pelo módulo de visão:

```bash
mosquitto_sub -h localhost -p 1833 -t env1234541/vision
```

- **Explicação**: Cria uma inscrição para os tópicos utilizados pelos módulo de visão, sendo possível escutar a comunicação realizada entre o módulo e os dispositivos.
- **Resultado esperado**: Os terminais ficarão executando o comando sem nenhuma saída.

6. **Publicar no Módulo de Visão**:
   Crie um terminal para publicar no módulo de visão, simulando uma publicação realizada pelos dispositivos:

### Exemplo de Comando:

```bash
mosquitto_pub -h localhost -p 1883 -t env1234541/vision -m "{\"device\":\"SALA_CAMERA_01\",\"devId\":\"disp0990sdf09s90sdf098s\",\"productKey\":\"fs0s0sd9ss9\",\"space\":\"SALA\",\"message\":{\"status\":[{\"code\":\"url\",\"t\":1712138400.0,\"value\":\"https://drive.google.com/file/d/183gk1XoNyqKMAMpYkyTArAteGjHl_3il/view?usp=sharing\"}]},\"sensorType\":\"camera\",\"timeStamp\":\"2024-04-0307:00:00.233460\"}"
```

- **Explicação**: Cria uma publicação com uma imagem contendo 2 pessoas desconhecidas e portando uma arma.
- **Resultado esperado**:

Tópico vision:

```bash
env1234541/vision {"device":"SALA_CAMERA_01","devId":"disp0990sdf09s90sdf098s","productKey":"fs0s0sd9ss9","space":"SALA","message":{"status":[{"code":"url","t":1712138400.0,"value":"https://drive.google.com/file/d/183gk1XoNyqKMAMpYkyTArAteGjHl_3il/view?usp=sharing"}]},"sensorType":"camera","timeStamp":"2024-04-0307:00:00.233460"}
```

Tópico devices:

```bash
env1234541/devices {"device": "SALA_CAMERA_01", "devId": "disp0990sdf09s90sdf098s", "productKey": "fs0s0sd9ss9", "space": "SALA", "message": {"status": [{"code": "quant_pessoas", "value": 2}, {"code": "conhecidas", "value": []}]}, "sensorType": "camera", "timeStamp": "2024-04-0307:00:00.233460", "alert": {"status": [{"code": "invasao", "value": "pessoa armada detectada"}, {"code": "img", "value": "https://drive.google.com/file/d/183gk1XoNyqKMAMpYkyTArAteGjHl_3il/view?usp=sharing"}]}}
```

### Exemplo de Comando:

```bash
mosquitto_pub -h localhost -p 1883 -t env1234541/vision -m "{\"device\":\"SALA_CAMERA_01\",\"devId\":\"disp0990sdf09s90sdf098s\",\"productKey\":\"fs0s0sd9ss9\",\"space\":\"SALA\",\"message\":{\"status\":[{\"code\":\"url\",\"t\":1712138400.0,\"value\":\"https://drive.usercontent.google.com/download?id=1PKI_L6_ec5G8MpDxyPRMGfjkIH_RTeAS\"}]},\"sensorType\":\"camera\",\"timeStamp\":\"2024-04-0307:00:00.233460\"}"
```

- **Explicação**: Cria uma publicação com o link da imagem quebrado.
- **Resultado esperado**: O módulo de visão não faz a resposta da requisição.

Tópico vision:

```bash
env1234541/vision {"device":"SALA_CAMERA_01","devId":"disp0990sdf09s90sdf098s","productKey":"fs0s0sd9ss9","space":"SALA","message":{"status":[{"code":"url","t":1712138400.0,"value":"https://drive.usercontent.google.com/download?id=1PKI_L6_ec5G8MpDxyPRMGfjkIH_RTeAS"}]},"sensorType":"camera","timeStamp":"2024-04-0307:00:00.233460"}
```

### Exemplo de Comando:

```bash
mosquitto_pub -h localhost -p 1883 -t env1234541/vision -m "{\"device\":\"SALA_CAMERA_01\",\"devId\":\"disp0990sdf09s90sdf098s\",\"productKey\":\"fs0s0sd9ss9\",\"space\":\"SALA\",\"message\":{\"status\":[{\"code\":\"url\",\"t\":1712138400.0,\"value\":\"https://drive.usercontent.google.com/download?id=1iRnlDEurcOvOhFuvBcMSmcoCB5NXLf6v\"}]},\"sensorType\":\"camera\",\"timeStamp\":\"2024-04-0307:00:00.233460\"}"
```

- **Explicação**: Cria uma publicação com uma imagem contendo uma pessoa conhecida e outra desconhecida.
- **Resultado esperado**:

Tópico vision:

```bash
env1234541/vision {"device":"SALA_CAMERA_01","devId":"disp0990sdf09s90sdf098s","productKey":"fs0s0sd9ss9","space":"SALA","message":{"status":[{"code":"url","t":1712138400.0,"value":"https://drive.usercontent.google.com/download?id=1iRnlDEurcOvOhFuvBcMSmcoCB5NXLf6v"}]},"sensorType":"camera","timeStamp":"2024-04-0307:00:00.233460"}
```

Tópico devices:

```bash
env1234541/devices {"device": "SALA_CAMERA_01", "devId": "disp0990sdf09s90sdf098s", "productKey": "fs0s0sd9ss9", "space": "SALA", "message": {"status": [{"code": "quant_pessoas", "value": 2}, {"code": "conhecidas", "value": ["mayki"]}]}, "sensorType": "camera", "timeStamp": "2024-04-0307:00:00.233460"}
```

### Exemplo de Comando:

```bash
mosquitto_pub -h localhost -p 1883 -t env1234541/vision -m "{\"device\":\"SALA_CAMERA_01\",\"devId\":\"disp0990sdf09s90sdf098s\",\"productKey\":\"fs0s0sd9ss9\",\"space\":\"SALA\",\"message\":{\"status\":[{\"code\":\"url\",\"t\":1712138400.0,\"value\":\"https://drive.usercontent.google.com/download?id=1wnSaiHBrgvy6R1BufQgCbDWJ0SZ7VcXD\"}]},\"sensorType\":\"camera\",\"timeStamp\":\"2024-04-0307:00:00.233460\"}"
```

- **Explicação**: Cria uma publicação com uma imagem contendo uma pessoa conhecida e outra pessoa desconhecida portando uma arma.
- **Resultado esperado**:

Tópico vision:

```bash
env1234541/vision {"device":"SALA_CAMERA_01","devId":"disp0990sdf09s90sdf098s","productKey":"fs0s0sd9ss9","space":"SALA","message":{"status":[{"code":"url","t":1712138400.0,"value":"https://drive.usercontent.google.com/download?id=1wnSaiHBrgvy6R1BufQgCbDWJ0SZ7VcXD"}]},"sensorType":"camera","timeStamp":"2024-04-0307:00:00.233460"}
```

Tópico devices:

```bash
env1234541/devices {"device": "SALA_CAMERA_01", "devId": "disp0990sdf09s90sdf098s", "productKey": "fs0s0sd9ss9", "space": "SALA", "message": {"status": [{"code": "quant_pessoas", "value": 2}, {"code": "conhecidas", "value": ["mayki"]}]}, "sensorType": "camera", "timeStamp": "2024-04-0307:00:00.233460", "alert": {"status": [{"code": "invasao", "value": "pessoa armada detectada"}, {"code": "img", "value": "https://drive.usercontent.google.com/download?id=1wnSaiHBrgvy6R1BufQgCbDWJ0SZ7VcXD"}]}}
```
