import csv
import RPi.GPIO as GPIO
import time

from os import write
from datetime import datetime
from mfrc522 import SimpleMFRC522
from pathlib import Path
from gpiozero import LED

ID = "0X7BE9F095F7" # my UPC card uid

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

    red_led = LED(6)
    green_led = LED(5)
    red_led.on()
    green_led.off()
    
    try: 
        while True:
            uid = rfid.read_uid()
            if authentication(uid):

                green_led.on()
                red_led.off()

                data["date"] = datetime.now()
                data["ID"] = uid
                write_to_csv()
                print(f'Usuario autorizado con uid: { uid }')

            else:
                red_led.blink(0.2,0.2)
                print("Usuario no autorizado")

            time.sleep(2)
            green_led.off()
            red_led.on()

    finally:
        GPIO.cleanup()


if __name__ == '__main__': main()