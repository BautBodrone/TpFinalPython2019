import time
import Adafruit_DHT
import RPi.GPIO as GPIO
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


class Matriz:
    def __init__(self, numero_matrices=1, orientacion=0, rotacion=0, ancho=8, alto=8):
        self.font = [CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT]
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, width=ancho, height=alto, cascaded=numero_matrices, rotate=rotacion)

    def mostrar_mensaje(self, msg, delay=0.1, font=1):
        show_message(self.device, msg, fill="white", font=proportional(self.font[font]), scroll_delay=delay)


class Sonido:
    def __init__(self, canal=22):
        self._canal = canal
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._canal, GPIO.IN)
        # Desactivo las warnings por tener más de un circuito en la GPIO
        GPIO.setwarnings(False)
        GPIO.add_event_detect(self._canal, GPIO.RISING)

    def evento_detectado(self, funcion):
        if GPIO.event_detected(self._canal):
            funcion()


class Temperatura:

    def __init__(self, pin=17, sensor=Adafruit_DHT.DHT11):
        # Usamos el DHT11 que es compatible con el DHT12
        self._sensor = sensor
        self._data_pin = pin

    def datos_sensor(self):
        humedad, temperatura = Adafruit_DHT.read_retry(self.
        _sensor, self._data_pin)
        return {'temperatura': temperatura, 'humedad': humedad}


temp = Temperatura()
datos = temp.datos_sensor()
starttime=time.time()
sonido = Sonido()
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width, height, cascaded, rotate)
matriz = Matriz(numero_matrices=2, ancho=16)


while True:
    print('Temperatura = {0:0.1f°}C Humedad = {1:0.1f} %'.format
          (datos['temperatura'], datos['humedad']))
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
    sonido.evento_detectado(matriz.mostrar_mensaje(temp.datos_sensor()), delay=0.3)

