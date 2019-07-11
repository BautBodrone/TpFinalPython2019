import time
import PySimpleGUI as sg
from datetime import date
import json

layout = [
    [
        sg.Button("Guardar Temperatura", font=('arial', '20', 'bold'), key="guardar"),
        sg.Button("Salir", font=('arial', '20', 'bold'), key="salir")
    ]
]


#temporizador = 3
oficina = sg.PopupGetText('Datos Oficina', 'Ingrese el numero/nombre de la oficina: ')

arch = open("dato-oficinas.json", "w+")
try:
    dato_arch = json.load(arch)
    print("ENTRO")
except ValueError:
    dato_arch = {}

if oficina is not None:
    window = sg.Window("Registro").Layout(layout)
    while True:
        event, values = window.Read()
        if event == "guardar":
            event, values = window.Read()
            datos = {
                'temperatura': "tst",
                'humedad': "tst",
                'fecha': date.today().strftime("%d/%m/%Y")
            }
            try:
                print("codigo")
                dato_arch[oficina].append(datos)
            except KeyError:
                dato_arch[oficina] = [datos]
                print("nuevo")
            #time.sleep(temporizador)
        if event is None or event == 'salir':
            break
    json.dump(dato_arch, arch)
arch.close()
