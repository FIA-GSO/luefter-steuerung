#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import logging

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
interval_in_s = 10.0

while True:
    try:
        with open('/sys/bus/iio/devices/iio:device0/in_temp_input', 'r') as file:
            data = file.read().strip()

        logging.info(data)
        if float(data) > 25000:
            GPIO.output(23, GPIO.HIGH)
        else:
            GPIO.output(23, GPIO.LOW)

        state = "an" if GPIO.input(23) else "aus"
        print(f"Temperature: {data} Status: {state}")

    except Exception as e:
        GPIO.output(23, GPIO.LOW)
        logging.error("Failed to read and log file: %s", e)