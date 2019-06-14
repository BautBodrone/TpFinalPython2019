import PySimpleGUI as sg
import Configuracion.Configuracion as Configuracion
import Configuracion.Identificador_de_palabra as Identificador

def abrir_configuracion():
    #COLUMNA IZQUIERDA
    def columna_izquierda(opciones):
        lista = []
        for opcion in opciones:
            lista.append([sg.Button(opcion.capitalize().replace("_"," "), size=(22, 1), key=opcion)])

        columna_izquierda = lista + [[
            sg.Button("Guardar", size=(10, 1), key="GRAN_Guardar",),
            sg.Button("Salir", size=(10, 1), key="salir",)
        ]] 

        return columna_izquierda

    #LISTA DE PALABRAS
    def columna_derecha_lista_de_palabras(lista_de_palabras):
        columna_derecha_lista_de_palabras = [
            [
                sg.Text("Lista de palabras")
            ],
            [
                sg.Table(
                    values=lista_de_palabras,
                    headings=['Palabra', 'Tipo'],
                    enable_events=True,
                    key='lista_de_palabras_seleccionada',
                    justification='center',

                )
            ],
            [
                sg.Button('Añadir', key='boton_confirmar'),
                sg.Button('Borrar', button_color=('white', 'red'), key='boton_cancelar'),
            ]
        ]

        return columna_derecha_lista_de_palabras

    #CANTIDAD DE PALABRAS
    def columna_derecha_cantidad_de_palabras(botones_por_defecto):
        cantidad_frame = [
            [
                sg.Text("Sustantivos", size=(10,1), justification='right'),
                sg.Slider(range=(1,5),orientation="h", size=(10,20), key='cantidad_sustantivos')
            ],
            [
                sg.Text("Adjetivos", size=(10,1), justification='right'),
                sg.Slider(range=(1,5),orientation="h", size=(10,20), key='cantidad_adjetivos')
            ],
            [
                sg.Text("Verbos", size=(10,1), justification='right'),
                sg.Slider(range=(1,5),orientation="h", size=(10,20),key='cantidad_verbos')
            ]
        ]
    
        columna_derecha_cantidad_de_palabras = [
            [
                sg.Frame('Cantidad de palabras por tipo', cantidad_frame)
            ],

            botones_por_defecto
        ]

        return columna_derecha_cantidad_de_palabras
    
    #AYUDAS
    def columna_derecha_ayudas(botones_por_defecto):
        ayudas_frame_habilitar = [
            [
                sg.Radio("Habilitar", "habilitar_ayudas",default = True, size=(20,1), key='habilitar_ayudas'),
            ],
            [
                sg.Radio("Deshabilitar", "habilitar_ayudas",)
            ]
        ] 
        ayudas_frame_tipo = [
            [
                sg.Radio("Lista de palabras", "tipo_de_ayudas", default = True, size=(20,1), key='ayuda_palabras'),
            ],
            [
                sg.Radio("Descripcion", "tipo_de_ayudas")
            ]
        ]
        columna_derecha_ayudas = [
            [
                sg.Frame('¿Habilitar ayudas?', ayudas_frame_habilitar)
            ],
            [
                sg.Frame('Seleccione el tipo de ayuda',ayudas_frame_tipo)
            ],
            botones_por_defecto
        ]
        return columna_derecha_ayudas
    
    #DISEÑO DEL JUEGO (ayudas, orientación, colores, cantidad de palabras, mayusculas)
    def columna_derecha_diseño_del_juego(botones_por_defecto):
        colores_frame = [
            [
                sg.ColorChooserButton("Sustantivos", size=(14,1), key='color_sustantivos'),
            ],
            [
                sg.ColorChooserButton("Adjetivos", size=(14,1), key='color_adjetivos'),
            ],
            [
                sg.ColorChooserButton("Verbos", size=(14,1), key='color_verbos')
            ],
        ]
        
        orientacion_frame = [
            [
                sg.Radio("Horizontal","orientacion",default=True, key='orientacion_horizontal'),
            ],
            [
                sg.Radio("Vertical","orientacion")
            ]
        ]

        maymin_frame = [
            [
                sg.Radio("Mayusculas","maymin",default=True, key='mayusculas'),
            ],
            [
                sg.Radio("Minusculas","maymin")
            ]
        ]

        tipografia_frame = [
            [
                sg.Combo(values=["arial","helvetica"], key='tipografia')
            ]
        ]

        orientacion_maymin_column = [
            [
                sg.Frame("Seleccionar orientación", orientacion_frame),
            ],
            [
                sg.Frame("Mayusculas/Minusculas", maymin_frame)
            ],
        ]

        color_tipografia_frame = [
            [
                sg.Frame('Seleccionar tipografia', tipografia_frame)
            ],
            [
                sg.Frame("Seleccionar colores", colores_frame),
            ],
        ]

        columna_derecha_diseño_del_juego = [
            [
                sg.Column(orientacion_maymin_column),
                sg.Column(color_tipografia_frame)
            ],
            botones_por_defecto
        ]

        return columna_derecha_diseño_del_juego

    #OFICINA
    def columna_derecha_oficina(oficinas):
        oficina_frame = [
            [
                sg.Combo(values=oficinas, key='oficina')
            ],
        ]

        columna_derecha_oficina = [
            [
                sg.Frame('Seleccione la oficina', oficina_frame)
            ],
            [
                sg.Button('Agregar', key='boton_confirmar'),
                sg.Button('Borrar', button_color=('white', 'red'), key='boton_cancelar')
            ]
        ]

        return columna_derecha_oficina

    #ACTUALIZAR COLUMNA DERECHA
    def actualizar_columna_derecha(columna_actual, lista_de_opciones):
        for opcion in lista_de_opciones:
            window.Element('columna_derecha_'+opcion).Update(visible=False)

        window.Element('columna_derecha_'+columna_actual).Update(visible=True)
    

    #"PROGRAMA PRINCIPAL"

    #Variables de diseño
    botones_por_defecto = [
        sg.Button('Confirmar', key='boton_confirmar'),
        sg.Button('Por defecto', key='boton_por_defecto'),
        sg.Button('Cancelar', button_color=('white', 'red'), key='boton_cancelar')
    ]

    lista_de_opciones = [
        'lista_de_palabras',
        'cantidad_de_palabras',
        'ayudas',
        'diseño_del_juego',
        'oficina',
    ]

    #Variables importantes
    configuracion = Configuracion.obtener_configuracion()

    #EJEMPLO AGREGAR PALABRA
    print(configuracion.lista_de_palabras)

    #Variables auxiliares
    oficinas = ["Oficina 1","Oficina 2"]

    #LAYOUT
    layout = [
        [   #Título
            sg.Text("Sopa de Letras", font="arial 40"),
        ],
        [
            sg.T(''),
        ],
        [
            #COLUMNA IZQUIERDA
            sg.Column(
                columna_izquierda(lista_de_opciones)
            ),

            #COLUMNA DERECHA
            sg.Column(#Empieza activa por defecto
                columna_derecha_lista_de_palabras(configuracion.lista_de_palabras),
                visible=True,
                key='columna_derecha_lista_de_palabras'
            ),
            sg.Column(
                columna_derecha_cantidad_de_palabras(botones_por_defecto),
                visible=False,
                key='columna_derecha_cantidad_de_palabras'
            ),
            sg.Column(
                columna_derecha_ayudas(botones_por_defecto),
                visible=False,
                key='columna_derecha_ayudas'
            ),
            sg.Column(
                columna_derecha_diseño_del_juego(botones_por_defecto),
                visible=False,
                key='columna_derecha_diseño_del_juego'
            ),
            sg.Column(
                columna_derecha_oficina(oficinas),
                visible=False,
                key='columna_derecha_oficina'
            ),
        ]
    ]

    #LAYOUT VENTANA LECTURA PALABRA
    ventana_lectura = [
        [sg.Text("Ingrese la palabra a añadir")],
        [sg.InputText(), sg.Button("Ok")]
    ]

    #LAYOUT SEGURO BORRAR
    ventana_seguro = [
        [sg.Text("Esta a punto de eliminar una palabra ¿Esta seguro?")],
        [sg.Button("Borrar", key="boton_confirmar"), sg.Button("Cancelar", key="boton_cancelar")]
    ]

    #Ejecucion y lectura de ventana de configuracion
    
    window = sg.Window("Configuración").Layout(layout)

    opcion_actual=lista_de_opciones[0]
    
    while True:
        event, values = window.Read()
        
        if event is None or event == 'salir':
            window.Close()
            break

        if event in lista_de_opciones:
            opcion_actual = event
            actualizar_columna_derecha(event, lista_de_opciones)


        if event == 'boton_confirmar':
            print('Menú actual: ', opcion_actual)
            print('Evento actual:', event)

            if opcion_actual == 'lista_de_palabras':
                print('> lista_de_palabras: Añadir')
                ventana_lectura = [
                    [sg.Text("Ingrese la palabra a añadir")],
                    [sg.InputText(), sg.Button("Ok")]
                ]
                subwindow = sg.Window("Añadir palabra").Layout(ventana_lectura)
                boton, palabra = subwindow.Read()
                Identificador.identificador(palabra[0])
                subwindow.Close()
                #agregar_palabra()

            if opcion_actual == 'cantidad_de_palabras':
                print('> cantidad_de_palabras: Confirmar')
                #cantidad_de_palabras()

            if opcion_actual == 'ayudas':
                print('> ayudas: Confirmar')
                #ayudas()

            if opcion_actual == 'diseño_del_juego':
                print('> diseño_del_juego: Confirmar')
                #diseño_del_juego()

            if opcion_actual == 'oficina':
                print('> oficina: Agregar')
                #oficina


        if event == 'boton_por_defecto':
            print(opcion_actual)
            print(event)

            if opcion_actual == 'lista_de_palabras':
                print('> lista_de_palabras: Por defecto')
                #agregar_palabra()

            if opcion_actual == 'cantidad_de_palabras':
                print('> cantidad_de_palabras: Por defecto')
                #cantidad_de_palabras()

            if opcion_actual == 'ayudas':
                print('> ayudas: Por defecto')
                #ayudas()

            if opcion_actual == 'diseño_del_juego':
                print('> diseño_del_juego: Por defecto')
                #diseño_del_juego()

            if opcion_actual == 'oficina':
                print('> oficina: Por defecto')
                #oficina

            
        if event == 'boton_cancelar':
            print(opcion_actual)
            print(event)

            if opcion_actual == 'lista_de_palabras':
                print('> lista_de_palabras: Borrar')
                palabra_seleccionada = values['lista_de_palabras_seleccionada']
                print('>> lista_de_palabras - palabra seleccionada: ', palabra_seleccionada[0])
                subwindow = sg.Window("¿Seguro?").Layout(ventana_seguro)
                boton, seleccion = subwindow.Read()
                if boton == 'boton_confirmar':
                    print("Se borro la palabra: ")
                    #borrar la palabra de la lista

                subwindow.Close()


            if opcion_actual == 'cantidad_de_palabras':
                print('> cantidad_de_palabras: Cancelar')
                #cantidad_de_palabras()

            if opcion_actual == 'ayudas':
                print('> ayudas: Cancelar')
                #ayudas()

            if opcion_actual == 'diseño_del_juego':
                print('> diseño_del_juego: Cancelar')
                #diseño_del_juego()

            if opcion_actual == 'oficina':
                print('> oficina: Borrar')
                #oficina
        

if __name__ == '__main__':
    abrir_configuracion()
