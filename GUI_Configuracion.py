import PySimpleGUI as sg
import Configuracion.Configuracion as Configuracion
import Configuracion.Identificador_de_palabra as Identificador


def abrir_configuracion():
    # COLUMNA IZQUIERDA
    def columna_izquierda(opciones):
        lista = []
        for opcion in opciones:
            lista.append([sg.Button(opcion.capitalize().replace("_", " "), size=(22, 1), key=opcion)])

        columna_izquierda = lista + [[
            sg.Button("Guardar", size=(10, 1), key="GRAN_Guardar", ),
            sg.Button("Salir", size=(10, 1), key="salir", )
        ]]

        return columna_izquierda


    # LISTA DE PALABRAS
    def columna_lista_de_palabras(lista_de_palabras):
        columna_lista_de_palabras = [
            [
                sg.Text("Lista de palabras")
            ],
            [
                sg.Table(
                    values=lista_de_palabras,
                    headings=['Palabra', 'Tipo'],
                    key='lista_de_palabras_seleccionada',
                    justification='center',

                )
            ],
            [
                sg.Button('Añadir', key='boton_confirmar'),
                sg.Button('Borrar', button_color=('white', 'red'), key='boton_cancelar'),
            ]
        ]

        return columna_lista_de_palabras

    def actualizar_lista_de_palabras(user):
        print('Actualizar: Lista de palabras')
        print('  > Lista de palabras actual: ')
        for element in user.lista_de_palabras:
            print('    > ', element)
        window.Element('columna_lista_de_palabras').Update(
            columna_lista_de_palabras(user.lista_de_palabras))
        window.Element('lista_de_palabras_seleccionada').Update(user.lista_de_palabras)


    # CANTIDAD DE PALABRAS
    def columna_cantidad_de_palabras(botones_por_defecto, valores):
        cantidad_frame = [
            [
                sg.Text("Sustantivos", size=(10, 1), justification='right'),
                sg.Slider(
                    default_value=valores[0],
                    range=(1, 5), orientation="h",
                    size=(10, 20),
                    key='cantidad_sustantivos'
                )
            ],
            [
                sg.Text("Adjetivos", size=(10, 1), justification='right'),
                sg.Slider(
                    default_value=valores[1],
                    range=(1, 5), orientation="h",
                    size=(10, 20),
                    key='cantidad_adjetivos'
                )
            ],
            [
                sg.Text("Verbos", size=(10, 1), justification='right'),
                sg.Slider(
                    default_value=valores[2],
                    range=(1, 5), orientation="h",
                    size=(10, 20),
                    key='cantidad_verbos'
                )
            ]
        ]

        columna_cantidad_de_palabras = [
            [
                sg.Frame('Cantidad de palabras por tipo', cantidad_frame)
            ],

            botones_por_defecto
        ]

        return columna_cantidad_de_palabras

    def actualizar_cantidad_de_palabras(user):
        window.Element('columna_cantidad_de_palabras').Update(
            columna_cantidad_de_palabras(botones_por_defecto, user.cantidad_de_palabras)
        )
        window.Element('cantidad_sustantivos').Update(value=user.cantidad_de_palabras[0])
        window.Element('cantidad_adjetivos').Update(value=user.cantidad_de_palabras[1])
        window.Element('cantidad_verbos').Update(value=user.cantidad_de_palabras[2])


    # AYUDAS
    def columna_ayudas(botones_por_defecto, estado_ayudas, estado_tipo_ayudas):
        ayudas_frame_habilitar = [
            [
                sg.Radio(
                    "Habilitar",
                    "habilitar_ayudas",
                    default=estado_ayudas,
                    size=(20, 1),
                    key='habilitar_ayudas'
                ),
            ],
            [
                sg.Radio(
                    "Deshabilitar",
                    "habilitar_ayudas",
                    default=not estado_ayudas,
                    key='deshabilitar_ayudas'
                )
            ]
        ]
        ayudas_frame_tipo = [
            [
                sg.Radio(
                    "Lista de palabras",
                    "tipo_de_ayudas",
                    default=estado_tipo_ayudas,
                    size=(20, 1),
                    key='ayuda_palabras'
                ),
            ],
            [
                sg.Radio(
                    "Descripcion",
                    "tipo_de_ayudas",
                    default=not estado_tipo_ayudas,
                    key='ayuda_descripcion'
                )
            ]
        ]
        columna_ayudas = [
            [
                sg.Frame('¿Habilitar ayudas?', ayudas_frame_habilitar)
            ],
            [
                sg.Frame('Seleccione el tipo de ayuda', ayudas_frame_tipo)
            ],
            botones_por_defecto
        ]
        return columna_ayudas

    def actualizar_ayudas(user):
        print(user.ayudas)
        window.Element('habilitar_ayudas').Update(value=True)
        window.Element('deshabilitar_ayudas').Update(value=True)
        window.Element('columna_ayudas').Update(
            columna_ayudas(botones_por_defecto, user.ayudas, user.tipo_ayudas)
        )


    # DISEÑO DEL JUEGO (ayudas, orientación, colores, cantidad de palabras, mayusculas)
    def columna_diseño_del_juego(botones_por_defecto, colores, orientacion, mayusculas, tipografia):
        colores_frame = [
            [
                sg.ColorChooserButton(
                    "Sustantivos", size=(14, 1), key='color_sustantivos', button_color=('white', colores[0])
                ),
            ],
            [
                sg.ColorChooserButton(
                    "Adjetivos", size=(14, 1), key='color_adjetivos', button_color=('white', colores[1])
                ),
            ],
            [
                sg.ColorChooserButton(
                    "Verbos", size=(14, 1), key='color_verbos', button_color=('white', colores[2])
                )
            ],
        ]

        orientacion_frame = [
            [
                sg.Radio("Horizontal", "orientacion", default=orientacion, key='orientacion_horizontal'),
            ],
            [
                sg.Radio("Vertical", "orientacion", default=not orientacion, key='orientacion_vertical')
            ]
        ]

        maymin_frame = [
            [
                sg.Radio("Mayusculas", "maymin", default=mayusculas, key='mayusculas'),
            ],
            [
                sg.Radio("Minusculas", "maymin", default=not mayusculas, key='minusculas')
            ]
        ]

        tipografia_frame = [
            [
                sg.Combo(values=["arial", "helvetica"], key='tipografia')
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

        columna_diseño_del_juego = [
            [
                sg.Column(orientacion_maymin_column),
                sg.Column(color_tipografia_frame)
            ],
            botones_por_defecto
        ]

        return columna_diseño_del_juego


    # OFICINA
    def columna_oficinas(oficinas):
        oficina_frame = [
            [
                sg.Combo(values=oficinas, key='oficina')
            ],
        ]

        columna_oficinas = [
            [
                sg.Frame('Seleccione la oficina', oficina_frame)
            ],
            [
                sg.Button('Agregar', key='boton_confirmar'),
                sg.Button('Borrar', button_color=('white', 'red'), key='boton_cancelar')
            ]
        ]

        return columna_oficinas


    # ACTUALIZAR COLUMNA DERECHA
    def actualizar_columna_derecha(columna_actual, lista_de_opciones):
        for opcion in lista_de_opciones:
            window.Element('columna_' + opcion).Update(visible=False)

        window.Element('columna_' + columna_actual).Update(visible=True)

    # ============================================================================ #
    # "PROGRAMA PRINCIPAL"
    print('Iniciando Configuración')

    # Variables de diseño
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
        'oficinas',
    ]

    # Instanciación de clases
    configuracion = Configuracion.obtener_configuracion()
    default = Configuracion.Configuracion()

    # LAYOUT
    layout = [
        [  # Título
            sg.Text("Sopa de Letras", font="arial 40"),
        ],
        [
            sg.T(''),
        ],
        [
            # COLUMNA IZQUIERDA
            sg.Column(
                columna_izquierda(lista_de_opciones)
            ),

            # COLUMNA DERECHA
            sg.Column(  # Empieza activa por defecto
                columna_lista_de_palabras(
                    configuracion.lista_de_palabras
                ),
                visible=True,
                key='columna_lista_de_palabras'
            ),
            sg.Column(
                columna_cantidad_de_palabras(
                    botones_por_defecto,
                    configuracion.cantidad_de_palabras
                ),
                visible=False,
                key='columna_cantidad_de_palabras'
            ),
            sg.Column(
                columna_ayudas(
                    botones_por_defecto,
                    configuracion.ayudas,
                    configuracion.tipo_ayudas
                ),
                visible=False,
                key='columna_ayudas'
            ),
            sg.Column(
                columna_diseño_del_juego(
                    botones_por_defecto,
                    configuracion.colores,
                    configuracion.orientacion,
                    configuracion.mayusculas,
                    'arial 10'
                ),
                visible=False,
                key='columna_diseño_del_juego'
            ),
            sg.Column(
                columna_oficinas(configuracion.oficinas),
                visible=False,
                key='columna_oficinas'
            ),
        ]
    ]

    # Ejecucion y lectura de ventana de configuracion

    window = sg.Window("Configuración").Layout(layout)

    opcion_actual = lista_de_opciones[0]

    while True:
        event, values = window.Read()
        print(event, values)

        if event is None or event == 'salir':
            window.Close()
            break

        elif event in lista_de_opciones:
            opcion_actual = event
            actualizar_columna_derecha(event, lista_de_opciones)

        elif event == 'boton_confirmar':
            print('Menú actual: ', opcion_actual)
            print('Evento actual:', event)

            if opcion_actual == 'lista_de_palabras':
                print('> lista_de_palabras: Añadir')

                layout_ingresar_palabra = [
                    [sg.Text("Ingrese la palabra a añadir")],
                    [sg.InputText(), sg.Button("Ok")]
                ]

                subwindow = sg.Window("Añadir palabra").Layout(layout_ingresar_palabra)

                boton, palabra = subwindow.Read()
                if not (boton is None or palabra == ''):
                    nueva_palabra = Identificador.identificador(palabra[0])
                    print(nueva_palabra)
                    print(nueva_palabra[1])
                    if nueva_palabra[1] == 'Sustantivo':
                        configuracion.sustantivos[nueva_palabra[0]] = nueva_palabra[2]
                        print(configuracion.sustantivos)

                subwindow.Close()

            if opcion_actual == 'cantidad_de_palabras':
                print('cantidad_de_palabras: Confirmar')

            if opcion_actual == 'ayudas':
                print('ayudas: Confirmar')

            if opcion_actual == 'diseño_del_juego':
                print('diseño_del_juego: Confirmar')

            if opcion_actual == 'oficina':
                print('Oficina: Agregar')

        elif event == 'boton_por_defecto':
            print('Menú actual: ', opcion_actual)
            print('Evento actual:', event)

            if opcion_actual == 'lista_de_palabras':
                print('> lista_de_palabras: Por defecto')
                actualizar_lista_de_palabras(default)

            if opcion_actual == 'cantidad_de_palabras':
                print('> cantidad_de_palabras: Por defecto')
                actualizar_cantidad_de_palabras(default)

            if opcion_actual == 'ayudas':
                print('> ayudas: Por defecto')
                actualizar_ayudas(default)

            if opcion_actual == 'diseño_del_juego':
                print('> diseño_del_juego: Por defecto')

            if opcion_actual == 'oficina':
                print('> oficina: Por defecto')

        elif event == 'boton_cancelar':
            print('Menú actual: ', opcion_actual)
            print('Evento actual:', event)

            if opcion_actual == 'lista_de_palabras':
                print('lista_de_palabras: Borrar')

                lista_palabras_seleccionadas = [configuracion.lista_de_palabras[posicion][0] for posicion in
                                                values['lista_de_palabras_seleccionada']]

                if len(lista_palabras_seleccionadas) > 1:
                    borrar_todos = False
                    for palabra_seleccionada in lista_palabras_seleccionadas:
                        if not borrar_todos:
                            confirmar_borrado = [
                                [
                                    sg.Text(
                                        'La palabra "' + palabra_seleccionada + '" se borrara para siempre, ¿esta seguro?')
                                ],
                                [sg.Checkbox('Realizar esta acción para todos los elementos', key='borrar_todos')],
                                [
                                    sg.Button("Borrar", key="boton_confirmar", button_color=('white', 'red')),
                                    sg.Button("Cancelar", key="boton_cancelar")
                                ],
                            ]

                            subwindow = sg.Window("¿Seguro?").Layout(confirmar_borrado)
                            event, values = subwindow.Read()

                            if event == 'boton_confirmar':
                                configuracion.borrar_palabra(palabra_seleccionada)
                                print('Palabra ' + palabra_seleccionada + ' borrada')
                                actualizar_lista_de_palabras(configuracion)

                                borrar_todos = values['borrar_todos']
                            elif event == 'boton_cancelar':
                                print('Cancelar borrado')
                                borrar_todos = values['borrar_todos']
                            elif event is None:
                                print('Salir')
                                borrar_todos = True
                        else:
                            if event == 'boton_confirmar':
                                configuracion.borrar_palabra(palabra_seleccionada)
                                print('Palabra ' + palabra_seleccionada + ' borrada')
                                actualizar_lista_de_palabras(configuracion)
                            elif event == 'boton_cancelar':
                                print('Palabra' + palabra_seleccionada + ' no ha sido borrada')
                            elif event is None:
                                print('Salir')

                        subwindow.Close()
                elif len(lista_palabras_seleccionadas) == 1:
                    palabra_seleccionada = lista_palabras_seleccionadas[0]

                    confirmar_borrado = [
                        [sg.Text('La palabra "' + palabra_seleccionada + '" se borrara para siempre, ¿esta seguro?')],
                        [sg.Button("Borrar", key="boton_confirmar"), sg.Button("Cancelar", key="boton_cancelar")]
                    ]

                    subwindow = sg.Window("¿Seguro?").Layout(confirmar_borrado)
                    event, values = subwindow.Read()

                    if event == 'boton_confirmar':
                        configuracion.borrar_palabra(palabra_seleccionada)
                        print('Palabra ' + palabra_seleccionada + ' borrada')
                        actualizar_lista_de_palabras(configuracion)

                    subwindow.Close()

                else:
                    sg.PopupOK('No ha seleccionado ninguna palabra')

            if opcion_actual == 'cantidad_de_palabras':
                print('> cantidad_de_palabras: Cancelar')
                actualizar_cantidad_de_palabras(configuracion)

            if opcion_actual == 'ayudas':
                print('> ayudas: Cancelar')
                actualizar_ayudas(configuracion)

            if opcion_actual == 'diseño_del_juego':
                print('> diseño_del_juego: Cancelar')
                # actualizar_diseño_del_juego(configuracion)

            if opcion_actual == 'oficina':
                print('> oficina: Borrar')
                # oficina


if __name__ == '__main__':
    abrir_configuracion()
