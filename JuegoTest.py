from random import shuffle
import Configuracion.Configuracion as Configuracion

def ventanajuego(config): ## en main juego.ventanajuego(configuracion.Configuracion.obtener_configuracion())
    import PySimpleGUI as sg
    import random

    def salir(e):
        return e is None

    def cancelar_seleccion(p):
        for clave in p:
            window.Element(clave).Update(button_color=('black', 'white'))
        return []

    def max_palabra(lis_palabra):
        #palabras = list(map(lambda x: x[0], lis_palabra))
        max = 0
        print(lis_palabra)
        for i in lis_palabra:
            if len(i[0])>max:
                max = len(i[0])
        return max

    def shuffle_pal (lis, tempo, tipo):
        shuffle(tempo)
        for x in tempo.keys():
            try:
                lis.append([x, tempo[x]])
            except IndexError:
                pass

    def generar_lis_palabras(config):
        lis = []
        cant_pal = config.cantidad_de_palabras
        sus = int(cant_pal[0])
        adj = int(cant_pal[1])
        verb = int(cant_pal[2])
        shuffle_pal(lis, config.sustantivos, sus)
        shuffle_pal(lis, config.adjetivos, adj)
        shuffle_pal(lis, config.verbos, verb)
        shuffle(lis)
        return lis

    def generar_matriz(N, lis_palabras):
        '''Genera una matriz de N filas y N columnas'''
        solo_palabras = list(map(lambda x: x[0], lis_palabras))
        matriz = []
        N = N + random.randint(1, 2) #para que la palabra mas grande no quede siempre pegada a los bordes
        lis_pos = -1
        ori = config.orientacion
        if ori is True: ##horizontal
            for x in range(N):
                linea = []
                go = random.choice([True, False])
                if go is True:
                    len_pal = len(solo_palabras[lis_pos])
                    start = random.randrange(0, (N-len_pal))
                    pos_agregado = 0
                    lis_pos = + 1
                for y in range(N):
                    if go is True:
                        if(x >= start)and(x < (start+len_pal)):
                            letra = solo_palabras[pos_agregado]
                            pos_agregado = + 1
                        else:
                            letra = chr(random.randint(ord('a'), ord('z')))
                    else:
                        letra = chr(random.randint(ord('a'), ord('z')))
                    clave = str(x) + ',' + str(y)
                    linea.append(
                        sg.Submit(  # Propiedades del botón
                            letra,
                            key=clave,
                            disabled=False,

                            # Diseño
                            font='Courier 10',
                            size=(4, 2) if N <= 12 else (2, 1),
                            button_color=('black', 'white')
                        ),
                    )
                matriz.append(linea)
        else:##no probado
            for y in range(N):
                linea = []
                go = random.choice([True, False])
                if go is True:
                    len_pal = len(lis_palabras[lis_pos])
                    start = random.randrange(0, (N - len_pal))
                    pos_agregado = 0
                    lis_pos = + 1
                for x in range(N):
                    if go is True:
                        if (y >= start) and (y < (start + len_pal)):
                            letra = lis_palabras[pos_agregado]
                            pos_agregado = + 1
                        else:
                            letra = chr(random.randint(ord('a'), ord('z')))
                    else:
                        letra = chr(random.randint(ord('a'), ord('z')))
                    clave = str(x) + ',' + str(y)
                    linea.append(
                        sg.Submit(  # Propiedades del botón
                            letra,
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

    config = Configuracion.obtener_configuracion()
    print(config.get_colores())
    lis_palabras = generar_lis_palabras(config)
    num = max_palabra(lis_palabras)
    matriz = generar_matriz(num, lis_palabras)
    columna_derecha = matriz
    columna_izquierda = [
        [
            sg.Submit(
                'Sustantivos',
                key='sustantivos',
                button_color=('black', config.colores[0])
            ),
            sg.Submit(
                'Adjetivos',
                key='adjetivos',
                button_color=('black', config.colores[1])
            ),
            sg.Submit(
                'Verbos',
                key='verbos',
                button_color=('black', config.colores[2])
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
