# AUTORES:
# Bodrone, Bautista
# Galati Martínez, Juan Cruz
# Zambrano Taus, Alejandro

import json
import PySimpleGUI as sg
import Configuracion.Configuracion as Configuracion
import Configuracion.Identificador_de_palabra as Identificador

def abrir_configuracion():
    '''Función principal, abre y ejecuta todas las funciones para la GUI de la ventana de configuración.'''
    def columna_izquierda(opciones):
        '''Genera la columna izquierda. Recibe una lista de opciones, a las que da formato como botón.'''
        lista = []
        for opcion in opciones:
            lista.append([sg.Button(opcion.capitalize().replace("_", " "), size=(22, 1), key=opcion)])

        columna_izquierda = lista + [[
            sg.Button("Guardar", size=(10, 1), key="Guardar", bind_return_key=True),
            sg.Button("Salir", size=(10, 1), key="Salir", )
        ]]

        return columna_izquierda


    def columna_derecha(opcion, configuracion):
        '''Genera la columna derecha según la opción actual seleccionada y la configuración del usuario para esa opción.'''
        def lista_de_palabras(valores):
            '''En la columna derecha, permite la visualización, adición y borrado de
            de la Lista de palabras'''
            if len(valores) == 0:
                encabezado = ['Error', 'Solución']
                valores = [['No hay ninguna palabra guardada', 'Agregue palabras para poder jugar']]
            else:
                encabezado = ['Palabra', 'Tipo']

            layout = [
                [
                    sg.Table(
                        values=valores,
                        headings=encabezado,
                        key='lista_de_palabras_seleccionada',
                        justification='center',

                    )
                ],
                [
                    sg.Button('Añadir', key='boton_confirmar'),
                    sg.Button('Borrar', button_color=('white', 'red'), key='boton_cancelar'),
                ]
            ]

            return layout


        def cantidad_de_palabras(botones_por_defecto, valores, cantidad_sustantivos, cantidad_adjetivos, cantidad_verbos):
            '''En la columna derecha, permite la visualización y modificación de
            la cantidad de palabras de la Lista de palabras a usar en el juego'''
            cantidad_frame = [
                [
                    sg.Text("Sustantivos", size=(10, 1), justification='right'),
                    sg.Slider(
                        default_value=valores[0],
                        range=(0, cantidad_sustantivos if cantidad_sustantivos <= 5 else 5), orientation="h",
                        size=(10, 20),
                        key='cantidad_sustantivos'
                    )
                ],
                [
                    sg.Text("Adjetivos", size=(10, 1), justification='right'),
                    sg.Slider(
                        default_value=valores[1],
                        range=(0, cantidad_adjetivos if cantidad_adjetivos <= 5 else 5), orientation="h",
                        size=(10, 20),
                        key='cantidad_adjetivos'
                    )
                ],
                [
                    sg.Text("Verbos", size=(10, 1), justification='right'),
                    sg.Slider(
                        default_value=valores[2],
                        range=(0, cantidad_verbos if cantidad_verbos <= 5 else 5), orientation="h",
                        size=(10, 20),
                        key='cantidad_verbos'
                    )
                ]
            ]

            cantidad_de_palabras = [
                [
                    sg.Frame('Cantidad de palabras por tipo', cantidad_frame)
                ],

                botones_por_defecto
            ]

            return cantidad_de_palabras

        def ayudas(botones_por_defecto, estado_ayudas, estado_tipo_ayudas):
            '''En la columna derecha, permite la visualización y modificación del
            tipo de ayuda que recibirá el alumno en la ejecución del juego'''
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

        def diseño_del_juego(botones_por_defecto, colores, orientacion, mayusculas, tipografia):
            '''En la columna derecha, permite la visualización, y modificación de
            los colores de cada tipo de palabra, la orientación de las palabras,
            si estarán en mayúsculas o minúsculas, y la tipografía del reporte'''
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

            diseño_del_juego = [
                [
                    sg.Column(orientacion_maymin_column),
                    sg.Column(color_tipografia_frame)
                ],
                botones_por_defecto
            ]

            return diseño_del_juego

        def oficinas(oficina_actual):
            '''En la columna derecha, permite la visualización y selección de
            la oficina desde la que obtener los datos ambientales'''
            arch = open("dato-oficinas.json", "r")
            oficinas = json.load(arch)

            oficina_frame = [
                [
                    sg.Combo(values=[*oficinas], default_value=oficina_actual, key='oficina')
                ],
            ]

            columna_oficinas = [
                [
                    sg.Frame('Seleccione la oficina', oficina_frame)
                ],
                [
                    sg.Button('Confirmar', key='boton_confirmar'),
                    sg.Button('Cancelar', button_color=('white', 'red'), key='boton_cancelar')
                ]
            ]

            return columna_oficinas

        # COLUMNA DERECHA
        retorno = []

        botones_por_defecto = [
            sg.Button('Confirmar', key='boton_confirmar'),
            sg.Button('Por defecto', key='boton_por_defecto'),
            sg.Button('Cancelar', button_color=('white', 'red'), key='boton_cancelar')
        ]

        if opcion == 'lista_de_palabras':
            retorno = lista_de_palabras(
                configuracion.lista_de_palabras
            )
        elif opcion == 'cantidad_de_palabras':
            retorno = cantidad_de_palabras(
                botones_por_defecto,
                configuracion.cantidad_de_palabras,
                len(configuracion.sustantivos),
                len(configuracion.adjetivos),
                len(configuracion.verbos)
            )
        elif opcion == 'ayudas':
            retorno = ayudas(
                botones_por_defecto,
                configuracion.ayudas,
                configuracion.tipo_ayudas
            )
        elif opcion == 'diseño_del_juego':
            retorno = diseño_del_juego(
                botones_por_defecto,
                configuracion.colores,
                configuracion.orientacion,
                configuracion.mayusculas,
                'Arial 10'
            )
        elif opcion == 'oficinas':
            retorno = oficinas(configuracion.oficina_actual)

        return retorno

    def PopUp_confirmar(titulo,string):
        '''Mensaje que permite al usuario confirmar una acción o cancelarla.
        El mensaje y título del Popup es personalizable'''
        layout = [
            [
                sg.T(string)
            ],
            [
                sg.Button('Confirmar', key='boton_confirmar'),
                sg.Button('Cancelar', key='boton_cancelar'),
            ]
        ]

        window = sg.Window(titulo).Layout(layout)
        confirmar = window.Read()
        window.Close()
        return confirmar

    def PopUp_guardar_y_salir(configuracion):
        '''Mensaje que consulta al usuario si desea salir sin guardar o guardar antes de salir.
        Retorna si se guardaron o no los cambios'''
        layout = [
            [
                sg.T('Hay cambios que no ha guardado, ¿Desea guardar los cambios antes de salir?')
            ],
            [
                sg.Button('Guardar y salir', key='boton_confirmar'),
                sg.Button('Salir', key='boton_cancelar'),
            ]
        ]

        window = sg.Window('Cambios sin guardar').Layout(layout)
        event, values = window.Read()
        window.Close()

        guardado = False
        
        if event == 'boton_confirmar':
            guardado = Configuracion.guardar_configuracion(user_config)
            if guardado:
                sg.PopupOK('Los cambios se han guardado con éxito.')
            else:
                sg.PopupOK('Un error ocurrió mientras intentábamos guardar la configuración. No se guardaron los cambios')

        return guardado

    def lista_de_palabras_agregar_palabra(user_config):
        layout_ingresar_palabra = [
            [sg.Text("Ingrese la palabra a añadir")],
            [sg.InputText(), sg.Button("Ok")]
        ]

        subwindow = sg.Window("Añadir palabra").Layout(layout_ingresar_palabra)

        boton, palabra = subwindow.Read()
        if not (boton is None or palabra == ''):
            nueva_palabra = Identificador.identificador(palabra[0])
            print(nueva_palabra)
            if not '' in nueva_palabra:
                user_config.agregar_palabra(nueva_palabra[0], nueva_palabra[1], nueva_palabra[2])
            else:
                sg.PopupOK('No se ha ingresado ninguna palabra o descripción')
            
        subwindow.Close()
        
    def lista_de_palabras_borrar_palabras(user_config, values):
        '''Permite borrar una o más palabras de la Lista de palabras'''
        lista_palabras_seleccionadas = [user_config.lista_de_palabras[posicion][0] for posicion in
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
                        user_config.borrar_palabra(palabra_seleccionada)
                        print('Palabra ' + palabra_seleccionada + ' borrada')

                        borrar_todos = values['borrar_todos']
                    elif event == 'boton_cancelar':
                        print('Cancelar borrado')
                        borrar_todos = values['borrar_todos']
                    elif event is None:
                        print('Salir')
                        borrar_todos = True
                else:
                    if event == 'boton_confirmar':
                        user_config.borrar_palabra(palabra_seleccionada)
                        print('Palabra ' + palabra_seleccionada + ' borrada')
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
                user_config.borrar_palabra(palabra_seleccionada)
                print('Palabra ' + palabra_seleccionada + ' borrada')

            subwindow.Close()

        else:
            sg.PopupOK('No ha seleccionado ninguna palabra')


    def layout_principal(lista_de_opciones, opcion_actual, configuracion):
        '''Genera la Interfaz Gráfica de Usuario, llama a la generación de la columna izquierda y derecha,
        mostrando la columna derecha correspondiente a la opción seleccinada.
        Opción seleccionada por defecto: Lista de palabras'''       
        layout = [
            [  # Título
                sg.Text("Sopa de Letras", font="arial 40"),
            ],
            [
                sg.T(''),
            ],
            [
                sg.Column(columna_izquierda(lista_de_opciones)),
                sg.Column(columna_derecha(opcion_actual, configuracion))
            ]
        ]

        return layout

    # EJECUCIÓN DE LA INTERFAZ GRÁFICA DE USUARIO DE LA VENTANA DE CONFIGURACIÓN
    lista_de_opciones = [
        'lista_de_palabras',
        'cantidad_de_palabras',
        'ayudas',
        'diseño_del_juego',
        'oficinas',
    ]

    user_config = Configuracion.obtener_configuracion()
    default_config = Configuracion.Configuracion()

    opcion_actual = lista_de_opciones[0]
    guardado = True
    
    while True:
        # Como no se puede actualizar ciertos elementos, forzamos a una actualización en cada bucle manualmente.
        window = sg.Window('Titulo').Layout(layout_principal(lista_de_opciones, opcion_actual, user_config))
        event, values = window.Read()

        # Imprime los datos de referencia en consola. Facilita depuración.
        print('\n# ' + '=' * 36 + ' #\n')
        print('Información de ventana:')
        print(' > Menú actual: ', opcion_actual)
        print(' > Evento actual:', event)

        # Salir de la configuración
        if event is None or event == 'Salir':
            if not guardado:
                guardado = PopUp_guardar_y_salir(user_config)
            window.Close()
            break

        # Seleccionar opción
        elif event in lista_de_opciones:
            opcion_actual = event

        # Para Lista de palabras, añadir palabra.
        # Para las otras opciones, confirmar cambios.
        if event == 'boton_confirmar':
            print(' > Valores:', values)
            guardado = False

            if opcion_actual == 'lista_de_palabras':
                print('> lista_de_palabras: Añadir')
                lista_de_palabras_agregar_palabra(user_config)

            if opcion_actual == 'cantidad_de_palabras':
                user_config.cantidad_de_palabras = [values['cantidad_sustantivos'], values['cantidad_adjetivos'], values['cantidad_verbos']]

            if opcion_actual == 'ayudas':
                user_config.ayudas = values['habilitar_ayudas']
                user_config.tipo_ayudas = values['ayuda_palabras']

            if opcion_actual == 'diseño_del_juego':
                user_config.orientacion = values['orientacion_horizontal']
                user_config.mayusculas = values['mayusculas']
                #Colores             
                if not values['color_sustantivos'] == '':
                    user_config.colores[0] = values['color_sustantivos']
                if not values['color_adjetivos'] == '':
                    user_config.colores[1] = values['color_adjetivos']
                if not values['color_verbos'] == '':
                    user_config.colores[2] = values['color_verbos']
                    
            if opcion_actual == "oficinas":
                user_config.oficina_actual = values["oficina"]
                sg.PopupOK('Para ver los cambios debe reiniciar la aplicación')

        # Reestablecer a los valores por defecto.
        if event == 'boton_por_defecto':
            print(' > Valores:', values)

            if PopUp_confirmar('Valores por defecto', 'Continuar restablecerá todas las opciones de ' +  opcion_actual.capitalize().replace("_", " ") + ' a sus valores por defecto.\n¿Seguro que desea continuar?'):

                if opcion_actual == 'cantidad_de_palabras':
                    user_config.cantidad_de_palabras = default_config.cantidad_de_palabras

                if opcion_actual == 'ayudas':
                    user_config.ayudas = default_config.ayudas
                    user_config.tipo_ayudas = default_config.tipo_ayudas

                if opcion_actual == 'diseño_del_juego':
                    user_config.colores[0] = default_config.colores[0]
                    user_config.colores[1] = default_config.colores[1]
                    user_config.colores[2] = default_config.colores[2]
                    user_config.orientacion = default_config.orientacion
                    user_config.mayusculas = default_config.mayusculas

                sg.PopupOK('Valores por defecto reestablecidos.')

        # Para todas las opciones excepto Lista de palabras, no hace nada. Lista de palabras: Borrar palabra.
        if event == 'boton_cancelar':
            print(' > Valores:', values)
            print('No hacer nada es igual a no guardar los cambios, so...')

            if opcion_actual == 'lista_de_palabras':
                guardado = False
                lista_de_palabras_borrar_palabras(user_config, values)

        if event == 'Guardar':
            guardado = Configuracion.guardar_configuracion(user_config)

            if guardado:
                sg.PopupOK('Los cambios se han guardado con éxito.')
            else:
                sg.PopupOK('Un error ocurrió mientras intentábamos guardar la configuración. No se guardaron los cambios')

        window.Close()

if __name__ == '__main__':
    abrir_configuracion()
