from gpiozero import LED
from signal import pause


red = LED(6)
green = LED(5)

red.blink()
green.blink()


pause()
    