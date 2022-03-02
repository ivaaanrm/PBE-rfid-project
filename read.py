import csv
from os import write
import RPi.GPIO as GPIO
import time

from datetime import datetime
from mfrc522 import SimpleMFRC522
from pathlib import Path
from gpiozero import LED

ID = 532205835767

path_csv = Path("loggs.csv")
log_ = {
    "date": None,
    "ID": None,
    "text": None,
}

def write_to_csv():
    first_write = not path_csv.is_file()

    with open(path_csv, "a") as f:
        field_names = log_.keys()
        writer = csv.DictWriter(f, field_names)
        if first_write:
            writer.writeheader()
        writer.writerow(log_)


def authentication(id):
    return id == ID

    
def main():
    reader_ = SimpleMFRC522()
    while True:
        try:
            id, text = reader_.read()
            if authentication(int(id)):
                log_["date"] = datetime.now()
                log_["ID"] = id
                write_to_csv()
                print(f'Usuario autorizado con uid: {hex(ID).upper()}')

            else:
                print("Usuario no autorizado")
            
            time.sleep(2)
        except Exception as e:
            print(e)
        finally:
            GPIO.cleanup()


if __name__ == '__main__': main()