import PySimpleGUI as sg
import GUI_Configuracion as gui_configuracion
import JuegoTest as juego
import Configuracion.Configuracion as Configuracion

def tema(bg_primario, text_primario, bg_secundario = None, text_secundario = None):
    if bg_secundario is None:
        bg_secundario = bg_primario
    if text_secundario is None:
        text_secundario = text_primario
        
    tema = sg.SetOptions(
        icon=None,
        button_color=(bg_secundario,'green'),
        progress_meter_color=None,
        text_color=text_primario,
        background_color=bg_primario,
        element_background_color=bg_primario,
        text_element_background_color=bg_primario,
        input_elements_background_color=bg_secundario,
        element_text_color=text_primario,
        input_text_color=text_primario,
        scrollbar_color=bg_secundario,
    )
    return tema

tema('red','green','blue', 'lightgreen')

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
