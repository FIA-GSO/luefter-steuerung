#!/usr/bin/python3
import os
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB connection details
token = "dZ-PxqwRUd3Tmlk6GFXvYM-zzoxY1at2y5vx7Vm7WPs-SbkJ-kklm_9CfABOi6kEbktHeOHmxnvbVH1fwd8TBA=="
org = "gso"
bucket = "default"

# Create an InfluxDB client
client = InfluxDBClient(url="http://localhost:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Constants
TEMP_SENSOR_PATH = '/sys/bus/iio/devices/iio:device0/in_temp_input'
HUMIDITY_SENSOR_PATH = '/sys/bus/iio/devices/iio:device0/in_humidityrelative_input'
PRESSURE_SENSOR_PATH = '/sys/bus/iio/devices/iio:device0/in_pressure_input'
INTERVAL_IN_S = 10.0
FAN_PIN = 23
LOG_FILE = 'temperature.log'

def read_sensor(sensor_path):
    """Read sensor value from file."""
    with open(sensor_path, 'r') as sensor_file:
        return sensor_file.read().strip()

def convert_temperature(temp_str):
    """Convert temperature from millidegrees Celsius to Celsius and Fahrenheit."""
    temp_celsius = float(temp_str) / 1000
    temp_fahrenheit = 1.8 * temp_celsius + 32
    return temp_celsius, temp_fahrenheit

def set_fan_state(fan_pin, state):
    """Set FAN state using pigs command."""
    os.system(f"pigs w {fan_pin} {state}")

def write_to_influxdb(celsius, fahrenheit, humidityrelative, pressure):
    """Write temperature, humidity and pressure to InfluxDB."""
    point = Point("sensor") \
        .tag("location", "serverroom") \
        .field("temperature_celsius", celsius) \
        .field("temperature_fahrenheit", fahrenheit) \
        .field("humidity_relative", humidityrelative) \
        .field("pressure", pressure) \
        .time(int(time.time() * 1000), WritePrecision.MS)

    write_api.write(bucket, org, point)

def main():
    """Main function."""
    try:
        with open(LOG_FILE, 'a') as log_file:
            while True:
                temp = read_sensor(TEMP_SENSOR_PATH)
                humidityrelative = int(float(read_sensor(HUMIDITY_SENSOR_PATH)) / 1000)
                pressure = int(float(read_sensor(PRESSURE_SENSOR_PATH)) * 10)

                if float(temp) > 25000:
                    set_fan_state(FAN_PIN, 1)  # Turn FAN on
                else:
                    set_fan_state(FAN_PIN, 0)  # Turn FAN off

                celsius, fahrenheit = convert_temperature(temp)

                write_to_influxdb(celsius, fahrenheit, humidityrelative, pressure)

                timestamp = time.strftime("%d.%m.%y %H:%M:%S")
                log_line = f'======= {timestamp} =======\n'
                log_line += "Temperature: {:.2f}°C\n".format(celsius)
                log_line += "Temperature: {:.2f}°F\n".format(fahrenheit)
                log_line += "Humidity: {}% r.F.\n".format(humidityrelative)
                log_line += "Pressure: {}hPa\n\n".format(pressure)

                print(log_line)
                log_file.write(log_line)
                log_file.flush()

                time.sleep(INTERVAL_IN_S)

    except Exception as e:
        set_fan_state(FAN_PIN, 0)  # Turn FAN off
        error_message = "Failed to read and log file: %s" % e
        print(error_message)
        log_file.write(error_message + '\n')
        log_file.flush()

if __name__ == "__main__":
    main()
