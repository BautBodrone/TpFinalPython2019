import PySimpleGUI as sg
import GUI_Configuracion as gui_configuracion
import Juego as juego
import Configuracion.Configuracion as Configuracion
import Promedio_temperatura as Promedio


def tema(bg_primario, text_primario, bg_secundario = None, text_secundario = None):
    if bg_secundario is None:
        bg_secundario = bg_primario
    if text_secundario is None:
        text_secundario = text_primario
        
    tema = sg.SetOptions(
        icon=None,
        button_color=(text_secundario,bg_secundario),
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


temaactual = Promedio.promedio(Configuracion.obtener_configuracion().oficinas)
tema(temaactual[0], temaactual[1], temaactual[2], temaactual[3])

layout = [
    [
        sg.Text("SOPA DE LETRAS", font=('comic sans ms', '58', 'bold'))
    ],
    [
        sg.T('')
    ],
    [
        sg.Button("JUGAR", font=('arial', '20', 'bold'), key="jugar"),
    ],
    [
        sg.Button("CONFIGURACION", font=('arial', '20', 'bold'), key="config"),
    ],
    [
        sg.Button("SALIR", font=('arial', '20', 'bold'), key="salir")
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
