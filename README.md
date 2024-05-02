# Lüftersteuerung mit Raspberry Pi
## Tischgruppe 4 - Lara, Farsat, Vathu, Kevin, Moritz

Dieses Python-Skript liest die Temperaturdaten von einem Sensor, der an einem Raspberry Pi angeschlossen ist, und steuert einen GPIO-Pin basierend auf den gelesenen Daten.

Dieses Python-Skript liest die Temperaturdaten von einem Sensor, der an einem Raspberry Pi angeschlossen ist, und steuert einen GPIO-Pin basierend auf den gelesenen Daten.

1. Zuerst wird der GPIO-Modus auf BCM gesetzt und der GPIO-Pin 23 als Ausgang konfiguriert.
```python
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
```
2. Das Skript tritt dann in eine Endlosschleife ein, in der es versucht, die Temperaturdaten zu lesen und zu verarbeiten.
```python
while True:
    try:
        ...
    except Exception as e:
        ...
```
3. Innerhalb der Schleife wird die Datei /sys/bus/iio/devices/iio:device0/in_temp_input geöffnet und die Daten werden gelesen und getrimmt.
```python
with open('/sys/bus/iio/devices/iio:device0/in_temp_input', 'r') as file:
    data = file.read().strip()
```
4. Die gelesenen Daten werden dann auf der Konsole ausgegeben.
```python
print(f"Temperature: {data} Status: {state}")
```
5. Basierend auf den gelesenen Daten wird der GPIO-Pin 23 entweder auf HIGH oder auf LOW gesetzt.
```python
if float(data) > 26000:
    GPIO.output(23, GPIO.HIGH)
else:
    GPIO.output(23, GPIO.LOW)
```
6. Im Falle eines Fehlers beim Lesen der Datei wird der GPIO-Pin 23 auf LOW gesetzt und eine Fehlermeldung wird auf der Konsole ausgegeben.
```python
except Exception as e:
    GPIO.output(23, GPIO.LOW)
    print(f"Failed to read file: {e}")
```