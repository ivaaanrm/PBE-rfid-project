import RPi.GPIO as gpio
from mfrc522 import SimpleMFRC522

reader_ = SimpleMFRC522()

try:
    id, text = reader_.read()
    print(id)
    print(text)
finally:
    gpio.cleanup()