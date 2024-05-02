#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import logging

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

interval_in_s = 10.0

while True:
    try:
        with open('/sys/bus/iio/devices/iio:device0/in_temp_input', 'r') as temp_file:
            temp = temp_file.read().strip()
        with open('/sys/bus/iio/devices/iio:device0/in_humidityrelative_input', 'r') as humidityrelative_file:
            humidityrelative = humidityrelative_file.read().strip()
        with open('/sys/bus/iio/devices/iio:device0/in_pressure_input', 'r') as pressure_file:
            pressure = pressure_file.read().strip()

        if float(temp) > 25000:
            GPIO.output(23, GPIO.HIGH)
        else:
            GPIO.output(23, GPIO.LOW)

        state = "an" if GPIO.input(23) else "aus"

        print(f'======= {time.strftime("%d.%m.%y %H:%M:%S") }=======')

        print("Temperatur: " + str(float(temp) / 1000) + "°C")

        print("Luftfeuchtigkeit: " + str(int(float(humidityrelative) / 1000)) + "% r.F.")

        print("Luftdruck: " + str(int(float(pressure) * 10)) + "hPa")

        print("\n")

        time.sleep(interval_in_s)

    except Exception as e:
        GPIO.output(23, GPIO.LOW)
        logging.error("Failed to read and log file: %s", e)