# AUTORES:
# Bodrone, Bautista
# Galati Martínez, Juan Cruz
# Zambrano Taus, Alejandro

import PySimpleGUI as sg
import GUI_Configuracion as gui_configuracion
import Configuracion.Configuracion as Configuracion
import Juego as juego
import Ambiente.Promedio_temperatura as Promedio

'''Menú principal e inicio del programa. Desde acá se llama a todos los demás módulos'''


def abrirMain():
    def tema(bg_primario, text_primario, bg_secundario = None, text_secundario = None):
        '''Modifica los colores de Interfaz Gráfica de Usuario en todo el programa'''
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

    # DEFINIR TEMA
    datos_configu = Configuracion.obtener_configuracion()
    temaactual = Promedio.promedio(datos_configu.oficina_actual)
    tema(temaactual[0], temaactual[1], temaactual[2], temaactual[3])

    # DEFINIR INTERFAZ GRÁFICA
    layout = [
        [
            sg.Text("SOPA DE LETRAS", font=(str(datos_configu.tipografia) + ' 58'),
                    justification="center", key="titulo")  # hay espacio por no centrarce
        ],
        [
            sg.Image(filename="Grid.png", size=(800, 400))
         ],
        [
            sg.Button("JUGAR", font=('arial', '20', 'bold'), size=(15, 1), key="jugar"),

            sg.Button("CONFIGURACION", font=('arial', '20', 'bold'), size=(15, 1), key="config"),

            sg.Button("SALIR", font=('arial', '20', 'bold'), size=(15, 1), key="salir")
        ]
    ]

    window = sg.Window(#Propiedades
                        "Título",
                        resizable=False,
                        size=(800, 600)
                    ).Layout(layout)

    # BUCLE DE EJECUCIÓN DEL MENÚ PRINCIPAL
    while True:
        event, values = window.Read()

        if event is None or event == 'salir':
            break

        if event == "config":
            window.Close()
            gui_configuracion.abrir_configuracion()
            break

        if event == "jugar":
            window.Disappear()
            juego.ventanajuego(datos_configu)
            window.Reappear()


if __name__ == '__main__':
    abrirMain()
