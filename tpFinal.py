def ventanajuego():
    import PySimpleGUI as sg
    import random


    def salir(e):
        return e is None


    def cancelar_seleccion(p):
        for clave in p:
            window.Element(clave).Update(button_color=('black', 'white'))
        return []


    def generar_matriz(N):
        '''Genera una matriz de N filas y N columnas'''
        matriz = []
        for i in range(N):
            linea = []
            for j in range(N):
                clave = str(i) + ',' + str(j)
                letra_aleatoria = chr(random.randint(ord('a'), ord('z')))

                linea.append(
                    sg.Submit(  # Propiedades del botón
                        letra_aleatoria,
                        key=clave,
                        disabled=False,

                        # Diseño
                        font='Courier 10',
                        size=(4, 2) if N <= 12 else (2, 1),
                        button_color=('black', 'white')
                    ),
                )
            matriz.append(linea)

        return matriz


    matriz = generar_matriz(10)
    columna_derecha = matriz
    columna_izquierda = [
        [
            sg.Submit(
                'Adjetivos',
                key='adjetivos',
                button_color=('black', 'red')
            ),
            sg.Submit(
                'Sustantivos',
                key='sustantivos',
                button_color=('black', 'silver')
            ),
            sg.Submit(
                'Verbos',
                key='verbos',
                button_color=('black', 'yellow')
            ),
        ],
        [
            sg.Submit('CANCELAR SELECCIÓN', key='cancelar')
        ]
    ]
    layout = [
        [
            sg.Column(columna_derecha),
            sg.Column(columna_izquierda)
        ]
    ]

    window = sg.Window('Sopa de letras').Layout(layout)
    event, values = window.Read()

    presionadas = []
    color = None

    while not salir(event):
        print(event, values)
        if color is None:
            actual = 'adjetivos'
            color = 'red'

        if event == 'cancelar':
            presionadas = cancelar_seleccion(presionadas)

        elif event in ('adjetivos', 'sustantivos', 'verbos'):
            print('Tipo: ', event)
            if not (event == actual):
                if event == 'adjetivos':
                    actual = 'adjetivos'
                    color = 'red'
                elif event == 'sustantivos':
                    color = 'silver'
                    actual = 'sustantivos'
                else:
                    actual = 'verbos'
                    color = 'yellow'

                presionadas = cancelar_seleccion(presionadas)

        else:
            print(presionadas)
            if event in presionadas:
                presionadas.remove(event)
                window.Element(event).Update(button_color=('black', 'white'))
            else:
                presionadas.append(event)
                window.Element(event).Update(button_color=('black', color))

        event, values = window.Read()


if __name__ == '__main__':
    ventanajuego()