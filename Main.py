import PySimpleGUI as sg
import ui as config
import tpFinal as juego

layout = [
    [sg.Text("Sopa de Letras", font="arial 40")],
    [sg.Button("Jugar", key="jugar", font="arial 20"), sg.Button("Config", key="config", font="arial 20"), sg.Button("Salir", key="salir", font="arial 20")]
]

window = sg.Window("", size=(800,600), resizable=True).Layout(layout)
while True:
    event, values = window.Read()

    if event == "config":
        config.ventanaconfig()
    if event == "jugar":
        juego.ventanajuego()
    if event is None or event == 'salir':
        break