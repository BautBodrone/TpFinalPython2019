import PySimpleGUI as sg
import Configuracion as config
import Juego as juego
from Usuario import Usuario

sg.ChangeLookAndFeel('Kayak')

layout = [
    [
        sg.Text("Sopa de Letras", font="arial 40")
    ],
    [
        sg.T('')
    ],
    [
        sg.Button("Jugar", font="arial 20", key="jugar"),
    ],
    [
        sg.Button("Configuracion", font="arial 20", key="config"),
    ],
    [
        sg.Button("Salir", font="arial 20", key="salir")
    ]
]

window = sg.Window(#Propiedades
                    "Título",
                    resizable=False,
                                        
                    
                    #Diseño
                    size=(800,600),
                    #no_titlebar=True
                    
                ).Layout(layout)

usuario = Usuario()

while True:
    event, values = window.Read()

    if event is None or event == 'salir':
        break

    if event == "config":
        window.Disappear()
        config.abrir_configuracion(usuario)
        window.Reappear()
        
    if event == "jugar":
        window.Disappear()
        juego.ventanajuego()
        window.Reappear()
