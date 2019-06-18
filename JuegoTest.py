import PySimpleGUI as sg
import random
import Configuracion.Configuracion as Configuracion
import numpy as np


def ventanajuego(config):  # en main juego.ventanajuego(configuracion.Configuracion.obtener_configuracion())
    def salir(e):
        return e is None

    def cancelar_seleccion(p):
        for clave in p:
            window.Element(clave).Update(button_color=('black', 'white'))
        return []

    def confirmar_seleccion(p, actual):
        for i in range (len(lis_palabras)):
            if (set(p) == set(lis_palabras[i][0]))and(actual == lis_palabras[i][2]):
                sg.Popup("noiz")

    def max_palabra(lis_palabra):
        max = 0
        print('lista_palabras', lis_palabra)
        for i in lis_palabra:
            if len(i[0])>max:
                max = len(i[0])
        if max<len(lis_palabra):
            max= len(lis_palabra)
        return max

    def shuffle_pal(lista, palabras, cantidad, tipo):
        temporal = list(palabras.keys())
        random.shuffle(temporal)
        for i in range(cantidad):
            try:
                lista.append([temporal[i], palabras[temporal[i]], tipo])
            except IndexError:
                pass

    def generar_lis_palabras(config):
        lista = []
        cant_sustantivos, cant_adjetivos, cant_verbos = config.cantidad_de_palabras
        
        shuffle_pal(lista, config.sustantivos, cant_sustantivos, "sustantivos")
        shuffle_pal(lista, config.adjetivos, cant_adjetivos, "adjetivos")
        shuffle_pal(lista, config.verbos, cant_verbos, "verbos")
        
        random.shuffle(lista)
        return lista

    def generar_matriz(N, lis_palabras):
        '''Genera una matriz de N filas y N columnas'''
        solo_palabras = list(map(lambda x: x[0], lis_palabras))  # hace una lista solo con las palabras
        matriz = []
        N = N + random.randint(1, 2)  # para que la palabra mas grande no quede siempre pegada a los bordes
        lis_pos = 0
        orientacion = config.orientacion
        go = range(0, N)
        go = sorted(random.sample(go, k=len(solo_palabras)))
        for y in range(N):
            linea = []
            entro = False
            try:
                if (go[0] == y) and (lis_pos < len(solo_palabras)):
                    len_pal = len(solo_palabras[lis_pos])
                    start = random.randrange(0, (N-len_pal))
                    pos_agregado = 0
                    entro = True
                    claves = []
                    del go[0]
            except IndexError:
                pass
            for x in range(N):
                if entro is True:
                    if(x >= start)and(x < (start+len_pal)):
                        claves.append(str(y) + ',' + str(x))
                        letra = solo_palabras[lis_pos][pos_agregado]
                        pos_agregado = pos_agregado + 1
                    else:
                        letra = chr(random.randint(ord('a'), ord('z')))
                else:
                    letra = chr(random.randint(ord('a'), ord('z')))
                clave = str(y) + ',' + str(x)
                linea.append(
                    sg.Submit(  # Propiedades del botón
                        letra,
                        key=clave,
                        disabled=False,

                        # Diseño
                        font='Courier 10',
                        size=(4, 2) if N <= 12 else (2, 1),
                        button_color=('black', 'white'),
                        pad=(0, 0)
                    ),
                )
            matriz.append(linea)
            if entro is True:
                lis_palabras[lis_pos][0] = claves  # utilizado para buscar si las palabras coiciden con lo clickeado
                lis_pos = lis_pos + 1
        if orientacion:  # horizontal
            return matriz
        else:  # vertical
            return np.transpose(matriz)

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
            sg.Submit("Confirmar", key="confirmar"), sg.Submit('CANCELAR SELECCIÓN', key='cancelar')
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
        # print(lis_palabras[0])
        print(event, values)
        if color is None:
            actual = 'adjetivos'
            color = config.colores[1]

        if event == 'cancelar':
            presionadas = cancelar_seleccion(presionadas)

        elif event == "confirmar":
            confirmar_seleccion(presionadas, actual)

        elif event in ('adjetivos', 'sustantivos', 'verbos'):
            print('Tipo: ', event)
            if not (event == actual):
                if event == 'adjetivos':
                    actual = 'adjetivos'
                    color = config.colores[1]
                elif event == 'sustantivos':
                    color = config.colores[0]
                    actual = 'sustantivos'
                else:
                    actual = 'verbos'
                    color = config.colores[2]

                presionadas = cancelar_seleccion(presionadas)

        else:
            if event in presionadas:
                presionadas.remove(event)
                window.Element(event).Update(button_color=('black', 'white'))
            else:
                presionadas.append(event)
                print(presionadas)
                window.Element(event).Update(button_color=('black', color))

        event, values = window.Read()


if __name__ == '__main__':
    ventanajuego(Configuracion.obtener_configuracion())
