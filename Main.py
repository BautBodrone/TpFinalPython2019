import PySimpleGUI as sg
import GUI_Configuracion as gui_configuracion
import JuegoTest as juego
import Configuracion.Configuracion as Configuracion

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

while True:
    event, values = window.Read()

    if event is None or event == 'salir':
        break

    if event == "config":
        window.Disappear()
        gui_configuracion.abrir_configuracion()
        window.Reappear()
        
    if event == "jugar":
        window.Disappear()
        juego.ventanajuego(Configuracion.obtener_configuracion())
        window.Reappear()
