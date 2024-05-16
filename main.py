#!/usr/bin/python3
import os
import time

# Constants
TEMP_SENSOR_PATH = '/sys/bus/iio/devices/iio:device0/in_temp_input'
HUMIDITY_SENSOR_PATH = '/sys/bus/iio/devices/iio:device0/in_humidityrelative_input'
PRESSURE_SENSOR_PATH = '/sys/bus/iio/devices/iio:device0/in_pressure_input'
INTERVAL_IN_S = 10.0
LED_PIN = 23

def read_sensor(sensor_path):
    """Read sensor value from file."""
    with open(sensor_path, 'r') as sensor_file:
        return sensor_file.read().strip()

def convert_temperature(temp_str):
    """Convert temperature from millidegrees Celsius to Celsius and Fahrenheit."""
    temp_celsius = float(temp_str) / 1000
    temp_fahrenheit = 1.8 * temp_celsius + 32
    return temp_celsius, temp_fahrenheit

def set_led_state(led_pin, state):
    """Set LED state using pigs command."""
    os.system(f"pigs w {led_pin} {state}")

def main():
    """Main function."""
    try:
        while True:
            temp = read_sensor(TEMP_SENSOR_PATH)
            humidityrelative = read_sensor(HUMIDITY_SENSOR_PATH)
            pressure = read_sensor(PRESSURE_SENSOR_PATH)

            if float(temp) > 25000:
                set_led_state(LED_PIN, 1)  # Turn LED on
            else:
                set_led_state(LED_PIN, 0)  # Turn LED off

            celsius, fahrenheit = convert_temperature(temp)

            print(f'======= {time.strftime("%d.%m.%y %H:%M:%S") }=======')
            print("Temperature: {:.2f}°C".format(celsius))
            print("Temperature: {:.2f}°F".format(fahrenheit))
            print("Humidity: {}% r.F.".format(int(float(humidityrelative) / 1000)))
            print("Pressure: {}hPa".format(int(float(pressure) * 10)))
            print("\n")

            time.sleep(INTERVAL_IN_S)

    except Exception as e:
        set_led_state(LED_PIN, 0)  # Turn LED off
        print("Failed to read and log file: %s", e)

if __name__ == "__main__":
    main()
