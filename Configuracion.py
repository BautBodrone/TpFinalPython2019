def ventanaconfig():
    import PySimpleGUI as sg
    sg.ChangeLookAndFeel('Kayak')
    data = ["Palabra"]
    lista_columna_derecha = [[sg.Text("Listado De Datos")],
                             [sg.Table(values=[['a','b','c']],headings=['Palabra', 'Tipo', 'Longitud'], enable_events=True, key='_LIST_')],
                             [sg.Button("Añadir", key="añadir"), sg.Button("Borrar", key="borrar"),
                             sg.Button("Guardar", key="guardar_pal")]]

    columna_izquierda = [[sg.Text("Configuracion")],
                         [sg.Button("Agregar User", key="agregar_user", size=(30, 1))],
                         [sg.Button("Config. Colores", key="config_colores", size=(30, 1))],
                         [sg.Button("Ayudas", key="ayudas", size=(30, 1))],
                         [sg.Button("Orientacion, Cantidad, MAY/min", key="????", size=(30, 1))],
                         [sg.Button("Tipografia", key="tipografia", size=(30,1))],
                         [sg.Button("Oficina", key="oficina", size=(30, 1))],
                         [sg.Button("Prest", key="prest", size=(8, 1)),
                          sg.Button("Guardar", key="Guardar", size=(8, 1)),
                          sg.Button("Salir", key="salir", size=(8, 1))]]

    layout = [[sg.Column(columna_izquierda), sg.Column(lista_columna_derecha)]]

    #Layout user
    users_layout = [
                    [sg.Combo(values=["asd","asd"])],
                    [sg.OK()]
    ]

    #Layout config colores
    colores_layout = [
                    [sg.ColorChooserButton("Sustantivos"), sg.ColorChooserButton("Adjetivos"), sg.ColorChooserButton("Verbos")],
                    [sg.OK()]
    ]

    #Layout de ayudas, selector radial
    ayudas_layout = [
                    [sg.Radio("Habilitar","rad1",default = True), sg.Radio("Deshabilitar","rad1")],
                    [sg.OK()]]

    #Layout orientacion, cantidad y MAYmin por separado
    orientacion_layout = [
                        [sg.Radio("Horizontal","orientacion",default=True), sg.Radio("Vertical","orientacion")]
    ]
    cantidad_layout = [
                    [sg.Text("Sustantivos"), sg.Slider(range=(1,5),orientation="h")],
                    [sg.Text("Adjetivos"), sg.Slider(range=(1,5),orientation="h")],
                    [sg.Text("Verbos"), sg.Slider(range=(1,5),orientation="h")],
    ]
    maymin_layout = [
                    [sg.Radio("Mayusculas","maymin",default=True), sg.Radio("Minusculas","maymin")]
    ]
    #Layout final oricanmm
    oricanmm_layout = [
                        [sg.Frame("Orientacion", orientacion_layout)],
                        [sg.Frame("Cantidad", cantidad_layout)],
                        [sg.Frame("Mayusculas/Minusculas", maymin_layout)],
                        [sg.OK()]
    ]

    #Layout oficina
    oficina_layout = [
                    [sg.Combo(values=["asd","asd"])],
                    [sg.OK()]
    ]

    #Layout selector de tipografia
    tipografia_layout = [
                    [sg.Combo(values=["arial","helvetica"])],
                    [sg.OK()]
    ]

    #Ejecucion y lectura de ventana de Configuracion, y subventanas
    window = sg.Window("UI").Layout(layout)
    while True:
        event, values = window.Read()
        if event is None:
            print(event,values)
            break
        if event == "ayudas":
            subwindow = sg.Window("").Layout(ayudas_layout)
            event, values = subwindow.Read()
            if event is "OK":
                subwindow.Close()
            print(event, values)
        if event == "????":
            subwindow = sg.Window("").Layout(oricanmm_layout)
            event, values = subwindow.Read()
            if event is "OK":
                subwindow.Close()
            print(event, values)
        if event == "agregar_user":
            subwindow = sg.Window("").Layout(users_layout)
            event, values = subwindow.Read()
            if event is "OK":
                subwindow.Close()
            print(event, values)
        if event == "config_colores":
            subwindow = sg.Window("").Layout(colores_layout)
            event, values = subwindow.Read()
            if event is "OK":
                subwindow.Close()
            print(event, values)
        if event == "oficina":
            subwindow = sg.Window("").Layout(oficina_layout)
            event, values = subwindow.Read()
            if event is "OK":
                subwindow.Close()
            print(event, values)
        if event == "tipografia":
            subwindow = sg.Window("").Layout(tipografia_layout)
            event, values = subwindow.Read()
            if event is "OK":
                subwindow.Close()
            print(event, values)
        if event == 'salir':
            print(event, values)
            break

if __name__ == '__main__':
    ventanaconfig()
