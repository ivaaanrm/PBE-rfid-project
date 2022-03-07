
""" 
Ivan Romero Moreno,
PBE Puzzle 1
* Programa que imprime por consola el uid (user identifier de la tarjeta de la UPC)
* El uid se imprime en mayusculas y en hexadecimal

Extras:
* Se guarda en un csv el uid con la hora de cada registro
* Se un led verde y uno rojo para indicar si el uid es correcto

"""

import csv
import RPi.GPIO as GPIO
import time

from datetime import datetime
from mfrc522 import SimpleMFRC522
from pathlib import Path
from gpiozero import LED

ID = "0X7BE9F095F7" # my UPC card uid

RED_LED = LED(6)
GREEN_LED = LED(5)

path_csv = Path("loggs.csv")
data = {
    "date": None,
    "ID": None,
}

class Rfid:
    def __init__(self):
        self.reader = SimpleMFRC522()
        self.id = None

    def read_uid(self):
        try:
            self.id = int(self.reader.read_id())
            self.id = hex(self.id).upper()
        except Exception as e:
            print("Error reading rfid" + e)
        
        return self.id
        

def write_to_csv():
    first_write = not path_csv.is_file()
    with open(path_csv, "a") as f:
        field_names = data.keys()
        writer = csv.DictWriter(f, field_names)
        if first_write:
            writer.writeheader()

        writer.writerow(data)


def authentication(id):
    return id == ID


def main():
    rfid = Rfid()
    RED_LED.on()
    GREEN_LED.off()
    try: 
        while True:
            uid = rfid.read_uid()
            if authentication(uid):
                GREEN_LED.on()
                RED_LED.off()
                data["date"] = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                data["ID"] = uid
                write_to_csv()
                print(f'Usuario autorizado con uid: { uid }')

            else:
                RED_LED.blink(0.2,0.2)
                print("Usuario no autorizado")

            time.sleep(2)
            GREEN_LED.off()
            RED_LED.on()

    finally:
        GPIO.cleanup()


if __name__ == '__main__': main()
