import PySimpleGUI as sg
import random
import Configuracion.Configuracion as Configuracion

def ventanajuego(config): ## en main juego.ventanajuego(configuracion.Configuracion.obtener_configuracion())
    def salir(e):
        return e is None

    def cancelar_seleccion(p):
        for clave in p:
            window.Element(clave).Update(button_color=('black', 'white'))
        return []

    def max_palabra(lis_palabra):
        max = 0
        print('lista_palabras', lis_palabra)
        for i in lis_palabra:
            if len(i[0])>max:
                max = len(i[0])
        return max

    def shuffle_pal(lista, palabras, cantidad):
        temporal = list(palabras.keys())
        random.shuffle(temporal)
        print(temporal)
        for i in range(cantidad):
            try:
                lista.append([temporal[i], palabras[temporal[i]]])
            except IndexError:
                pass

    def generar_lis_palabras(config):
        lista = []
        cant_sustantivos, cant_adjetivos, cant_verbos = config.cantidad_de_palabras
        
        shuffle_pal(lista, config.sustantivos, cant_sustantivos)
        shuffle_pal(lista, config.adjetivos, cant_adjetivos)
        shuffle_pal(lista, config.verbos, cant_verbos)
        
        random.shuffle(lista)
        return lista

    def generar_matriz(N, lis_palabras):
        '''Genera una matriz de N filas y N columnas'''
        solo_palabras = list(map(lambda x: x[0], lis_palabras))##hace una lista solo con las palabras
        matriz = []
        N = N + random.randint(1, 2) #para que la palabra mas grande no quede siempre pegada a los bordes
        lis_pos = 0
        orientacion = config.orientacion
        if orientacion: ##horizontal
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
                        del go[0]
                except IndexError:
                    pass
                for x in range(N):
                    if entro is True:
                        if(x >= start)and(x < (start+len_pal)):
                            letra = solo_palabras[lis_pos][pos_agregado]
                            pos_agregado = pos_agregado + 1
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
                            button_color=('black', 'white'),
                            pad=(0, 0)
                        ),
                    )
                matriz.append(linea)
                if entro is True:
                    lis_pos = lis_pos + 1
        else:##no probado
            for y in range(N):
                linea = []
                go = random.choice([True, False])
                if go:
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
            color = config.colores[1]

        if event == 'cancelar':
            presionadas = cancelar_seleccion(presionadas)

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
            print(presionadas)
            if event in presionadas:
                presionadas.remove(event)
                window.Element(event).Update(button_color=('black', 'white'))
            else:
                presionadas.append(event)
                window.Element(event).Update(button_color=('black', color))

        event, values = window.Read()


if __name__ == '__main__':
    ventanajuego(Configuracion.obtener_configuracion())
