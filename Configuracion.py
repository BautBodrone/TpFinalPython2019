import PySimpleGUI as sg    

def abrir_configuracion():
    botones_por_defecto = [
        sg.Button('Confirmar'),
        sg.Button('Por defecto'),
        sg.Button('Cancelar', button_color=('white', 'red'))
    ]
    columna_izquierda = [
        [
            sg.Button("Usuarios", size=(22, 1), key="usuarios",)
        ],
        [
            sg.Button("Lista de palabras", size=(22, 1), key="lista_de_palabras",)
        ],
        [
            sg.Button('Cantidad de palabras', size=(22,1), key='cantidad')
        ],
        [
            sg.Button("Ayudas", size=(22, 1), key="ayudas",)
        ],
        [
            sg.Button("Diseño del juego", size=(22, 1), key="diseño",)
        ],
        [
            sg.Button("Oficina", size=(22, 1), key="oficina",)],
        [
            sg.Button("Guardar", size=(10, 1), key="GRAN_Guardar",),
            sg.Button("Salir", size=(10, 1), key="salir",)
        ]
    ]

    #LISTA DE PALABRAS: Columna derecha
    columna_derecha_palabras = [
        [
            sg.Text("Lista de palabras")
        ],
        [
            sg.Table(
                values=[['Casa','Sustantivo','{}'.format(len("Casa"))]],
                headings=['Palabra', 'Tipo', 'Longitud'],
                enable_events=True,
                key='tabla_de_palabras',
                justification='center',
                
            )
        ],
        [
            sg.Button("Añadir", key="añadir"),
            sg.Button("Borrar", key="borrar"),
            sg.Button("Guardar", key="guardar_palabra")
        ]
    ]

    columna_derecha_usuarios = [
        [
            sg.Combo(values=[None])
        ],
        [
            sg.OK()
        ]
    ]

    #CANTIDAD DE PALABRAS: Columna derecha
    cantidad_frame = [
        [
            sg.Text("Sustantivos", size=(10,1), justification='right'),
            sg.Slider(range=(1,5),orientation="h", size=(10,20))
        ],
        [
            sg.Text("Adjetivos", size=(10,1), justification='right'),
            sg.Slider(range=(1,5),orientation="h", size=(10,20))
        ],
        [
            sg.Text("Verbos", size=(10,1), justification='right'),
            sg.Slider(range=(1,5),orientation="h", size=(10,20))
        ]
    ]
    columna_derecha_cantidad = [
        [
            sg.Frame('Cantidad de palabras por tipo', cantidad_frame)
        ],

        botones_por_defecto
    ]

    #AYUDAS: Columna derecha
    ayudas_frame_habilitar = [
        [
            sg.Radio("Habilitar","rad1",default = True, size=(20,1)),
        ],
        [
            sg.Radio("Deshabilitar","rad1")
        ]
    ] 

    ayudas_frame_tipo = [
        [
            sg.Radio("Lista de palabras", "rad2", default = True, size=(20,1)),
        ],
        [
            sg.Radio("Descripcion", "rad2")
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

    #DISEÑO DEL JUEGO: Columna derecha (ayudas, orientación, colores, cantidad de palabras, mayusculas)
    colores_frame = [
        [
            sg.ColorChooserButton("Sustantivos", size=(14,1)),
        ],
        [
            sg.ColorChooserButton("Adjetivos", size=(14,1)),
        ],
        [
            sg.ColorChooserButton("Verbos", size=(14,1))
        ],
    ]
    
    orientacion_frame = [
        [
            sg.Radio("Horizontal","orientacion",default=True),
        ],
        [
            sg.Radio("Vertical","orientacion")
        ]
    ]

    maymin_frame = [
        [
            sg.Radio("Mayusculas","maymin",default=True),
        ],
        [
            sg.Radio("Minusculas","maymin")
        ]
    ]

    tipografia_frame = [
        [
            sg.Combo(values=["arial","helvetica"])
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


    #DISEÑO: Columna derecha
    columna_derecha_diseño = [
        [
            sg.Column(orientacion_maymin_column),
            sg.Column(color_tipografia_frame)
        ],
        botones_por_defecto
    ]

    #OFICINA: Columna derecha
    oficinas = ["Oficina 1","Oficina 2"]
    oficina_frame = [
        [
            sg.Combo(values=oficinas)
        ],
        [
            sg.Button('Seleccionar'),
            sg.Button('Agregar'),
            sg.Button('Borrar')
        ]
    ]

    columna_derecha_oficina = [
        [
            sg.Frame('Seleccione la oficina', oficina_frame)
        ]
    ]

    
    
    #LAYOUT CONFIGURACIÓN
    layout = [
        [
            sg.Text("Sopa de Letras", font="arial 40")
        ],
        [
            sg.T('')
        ],
        [
            sg.Column(columna_izquierda),
            
            sg.Column(columna_derecha_usuarios, visible=False, key='columna_derecha_usuarios'),
            sg.Column(columna_derecha_palabras, visible=True, key='columna_derecha_palabras'),
            sg.Column(columna_derecha_cantidad, visible=False, key='columna_derecha_cantidad'),
            sg.Column(columna_derecha_ayudas, visible=False, key='columna_derecha_ayudas'),
            sg.Column(columna_derecha_diseño, visible=False, key='columna_derecha_diseño'),
            sg.Column(columna_derecha_oficina, visible=False, key='columna_derecha_oficina')
        ]
    ]

    def actualizar_columna_derecha(columna_actual):
        window.Element('columna_derecha_usuarios').Update(visible=False),
        window.Element('columna_derecha_palabras').Update(visible=False),
        window.Element('columna_derecha_cantidad').Update(visible=False),
        window.Element('columna_derecha_ayudas').Update(visible=False),
        window.Element('columna_derecha_diseño').Update(visible=False),
        window.Element('columna_derecha_oficina').Update(visible=False)

        window.Element('columna_derecha_'+columna_actual).Update(visible=True)

    #Ejecucion y lectura de ventana de configuracion
    
    window = sg.Window("UI").Layout(layout)
    
    while True:
        event, values = window.Read()
        print(event,values)
        
        if event is None or event == 'salir':
            window.Close()
            break

        if event == "lista_de_palabras":
            actualizar_columna_derecha('palabras')

        if event == "cantidad":
            actualizar_columna_derecha('cantidad')

        if event == "ayudas":
            actualizar_columna_derecha('ayudas')

        if event == "usuarios":
            actualizar_columna_derecha('usuarios')
            
        if event == "diseño":
            actualizar_columna_derecha('diseño')
            
        if event == "oficina":
            actualizar_columna_derecha('oficina')

if __name__ == '__main__':
    abrir_configuracion()
