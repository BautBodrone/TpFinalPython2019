import time
import Adafruit_DHT
import PySimpleGUI as sg
from datetime import date
import json


class Temperatura:

    def __init__(self, pin=17, sensor=Adafruit_DHT.DHT11):
        self._sensor = sensor
        self._data_pin = pin

    def datos_sensor(self):
        humedad, temperatura = Adafruit_DHT.read_retry(self._sensor, self._data_pin)
        return {'temperatura': temperatura, 'humedad': humedad, 'fecha': date.today().strftime("%d/%m/%Y")}


layout = [
        sg.Button("Terminar lectura", font=('arial', '20', 'bold'), key="salir")
]


temp = Temperatura()
temporizador = 60*1000  # cantidad de segundo * milisegundo
oficina = sg.PopupGetText('Datos Oficina', 'Ingrese el numero/nombre de la oficina: ')

try:
    arch = open("dato-oficinas.json", "x")
    ini = {}
    json.dump(ini, arch)
    arch.close()
except FileExistsError:
    pass

with open("dato-oficinas.json", "r") as arch:
    dato_arch = json.load(arch)
with open("dato-oficinas.json", "w+") as arch:
    if oficina is not None:
        window = sg.Window("Oficina "+str(oficina)).Layout(layout)
        while True:
            event, values = window.Read(timeout=temporizador)
            datos = temp.datos_sensor()
            dato_arch = json.load(arch)
            try:
                dato_arch[oficina].append(datos)
            except KeyError:
                dato_arch[oficina] = [datos]
            if event is None or event == "salir":
                break

