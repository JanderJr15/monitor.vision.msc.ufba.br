"""
Main module for the computer vision system that detects people,
weapons, and performs facial recognition in images.

This module receives camera data sent over an MQTT topic,
processes the images, and returns the analyzed results in JSON format.
"""
from vision.components.comm.vision_comm_mqtt import VisionCommMqtt
from monitor import  task_monitor

if __name__ == '__main__':

    # Main entry point for the vision system.

    visionSubiscribe = VisionCommMqtt()
    visionSubiscribe.subiscribe()
    # task_monitor.run()
