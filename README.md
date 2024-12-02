# Vision Module

## About

Vision module for the computer vision system that detects people,
weapons, and performs facial recognition in images.

This module receives camera images sent over an MQTT topic,
processes the images, and returns the analyzed results in JSON format.

### Vision Module Structure;

The structure of the vision module describes the purpose of each directory in the system.
Each directory is created to support specific aspects of our vision system integrated
with MQTT communication.

```plaintext
  vision/
  ├── __init__.py
  ├── __main__.py
  ├── components/
  │   ├── comm/
  │   │   └── ...
  │   └── vision/
  │       └── ...
  ├── id_db/
  │   ├── crops/
  │   │   ├── ds_model_vggface_detector_.h5
  │   │   ├── Eduardo.jpg
  │   │   ├── Mayki.jpg
  |   |   └── ...
  │   ├── images/
  │   │   ├── Eduardo.jpg
  │   │   ├── Mayki.jpg
  │   │   └── ...
  ├── models/
  │   ├── weapon_detector.pt
  │   ├── yolov8m-pose.pt
  │   ├── yolov9c.pt
  │   └── __init__.py
  └── config.yaml
```

* components/comm
  * Contains the infrastructure for setting up and managing MQTT communication. It facilitates the connection to MQTT brokers and the handling of message subscriptions and publications related to image data processing. 
* components/vision
  * Includes the core functionalities for image processing such as facial recognition, person detection, and weapon detection. This directory houses the logic to process image data and generate relevant output for security and monitoring applications.
* id_db/
  * Serves as the storage location for facial recognition data and reference images. It holds cropped images of faces for recognition purposes and original images for maintaining a comprehensive identity database.
* models/
  * Stores all the machine learning models used in the vision system. These models are crucial for detecting people and weapons.
* config.yaml
  * A configuration file that defines the paths and parameters for the models and other system settings. It ensures that the system components are easily configurable and maintainable.

| Folder           | Function                                                                |
|------------------|-------------------------------------------------------------------------|
| `vision`         | The main Python module of this project                                  |
| `test`           | In this folder should contains all `test` files                         |
| `pyproject.toml` | This file declares the python project, dependencies, and configurations |
| `pylintrc`       | This file declares the pylint configuration                             |

# How to setup dependencies

## Prerequisites

* The python dependencies **should be managed by poetry**!

## Downloading dependencies

### System Dependency

```bash
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients
```

### Python Dependency

```bash
poetry install
```

### Download Retina Face model

```bash
poetry run python vision/components/vision/download_retina_face_model.py
```
# How to run

After all dependencies have been installed, use `poetry shell` to spawn a shell environment 
with access to the dependencies specified in your pyproject.toml file.

## To run the project:

If this is the **first execution**, create the `.env` file based on the `.env.example` file, modifying the MQTT broker host and connection port: `MQTT_HOST`, `MQTT_MOSQUITTO_TLS_PORT`.

```bash
poetry run python -m vision
```

_For more information on how to use the tool check out the [Argus Coding Guidelines](https://github.com/Grupo-de-Inteligencia-Aplicada/documents.liaa.argus.ufba.br/blob/737562f788efe4d5e5f971a28127e06dcf94e2e6/docs/dependencies.md)_

<hr/>

# How to test
Use:

```bash
poetry run pytest
```

# How to lint
Use MyPy for type checking:
```bash
poetry run mypy vision
```

Use PyLint for linting:
```bash
poetry run pylint vision
```

# How to generate the documentation
Use pdoc to generate the html docs:
```bash
poetry run pdoc --output-dir docs vision
```

# Responsible

### For more details, contact one of the responsible researchers:

* alvaro.oliveira@ufba.br - Alvaro Oliveira (development)
* iarleymoraes21@gmail.com - Iarley Moraes (development)
* jorgebatista@ufba.br - Jorge Batista (development)
* marcosass@ufba.br - Marcos Silva (development)
* marcus.elias@ufba.br - Marcus Freire (development)
* guimaraes.matheus@ufba.br - Matheus Guimarães (development)
