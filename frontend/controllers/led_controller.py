from gpiozero import LED
from threading import Thread
import time


class LEDController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LEDController, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, pin=6):
        if not hasattr(self, "led"):
            self.led = LED(pin)
            self.blinking = False

    def start_blinking(self, interval=0.5):
        self.blinking = True

        def blink():
            while self.blinking:
                print("psicando!")
                self.led.on()
                time.sleep(interval)
                self.led.off()
                time.sleep(interval)

        Thread(target=blink, daemon=True).start()

    def stop_blinking(self):
        self.blinking = False
        self.led.off()
