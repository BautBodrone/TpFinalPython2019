# AUTORES:
# Bodrone, Bautista
# Galati Martínez, Juan Cruz
# Zambrano Taus, Alejandro

import PySimpleGUI as sg
import random
import numpy as np


def ventanajuego(config):  # en main juego.ventanajuego(configuracion.Configuracion.obtener_configuracion())

    def cancelar_seleccion(p, correcto=False):
        for clave in p:
            if not correcto:
                window.Element(clave).Update(button_color=('black', 'white'))
            else:
                window.Element(clave).Update(disabled=True)
        return []

    def confirmar_seleccion(p, actual, lista, cantidad_de_palabras):
        '''Confirma si las casillas seleccionadas corresponden a una palabra en la lista de palabras'''         
        # Lista es una lista de listas; cada lista de lista contiene:
        # [Lista de claves, tipo] de una palabra.
        # p es una lista de claves, actual es el tipo seleccionado.

        # Por lo tanto, si se cumple la siguiente condición,
        # podemos afirmar sin dudas que la palabra es correcta

        if [p, actual] in lista:
            correcto = True

            lista.remove([p, actual])

            if actual == 'sustantivos':
                cantidad_de_palabras[0] -= 1
            elif actual == 'adjetivos':
                cantidad_de_palabras[1] -= 1
            else:
                cantidad_de_palabras[2] -= 1
        else:
            correcto = False

        return cantidad_de_palabras, correcto

    def max_palabra(lis_palabra):
        '''Define la cantidad de casillas de la Matriz.
        Como mínimo será de la cantidad de palabras a colocar'''
        max = 0
        for palabra in lis_palabra:
            if len(palabra[0]) > max:
                max = len(palabra[0])
                
        if max < len(lis_palabra):
            max = len(lis_palabra)

        return max + random.randint(1, 2) # Para que la palabra más larga no quede pegada a los bordes

    def shuffle_pal(lista, palabras, cantidad, tipo):
        temporal = list(palabras.keys())
        random.shuffle(temporal)
        for i in range(cantidad):
            try:
                lista.append([temporal[i], palabras[temporal[i]], tipo])
            except IndexError:
                pass

    def generar_lis_palabras(config):
        """ Genera lista de con palabras aleatorias dependiendo del limite dado por el usuario"""
        lista = []
        cant_sustantivos, cant_adjetivos, cant_verbos = [int(i) for i in config.cantidad_de_palabras]
        
        shuffle_pal(lista, config.sustantivos, cant_sustantivos, "sustantivos")
        shuffle_pal(lista, config.adjetivos, cant_adjetivos, "adjetivos")
        shuffle_pal(lista, config.verbos, cant_verbos, "verbos")
        
        random.shuffle(lista)
        return lista

    def generar_matriz(N, lis_palabra):
        '''Genera una Matriz Cuadrada de orden N'''

        lista = list(map(lambda x: [x[0], x[2]], lis_palabra)) # hace una lista solo con las palabras y su tipo
        posicionesY = sorted(random.sample(range(0, N), k=len(lista)))

        # Diccionario que guarda la posición de las palabras. Clave: Línea, Valor: (Inicio, palabra)
        posiciones = {}
        while lista:
            # Mientras haya palabras en la lista

            #Seleccionar palabra y quitarla de la lista
            palabra = lista[random.randrange(0, len(lista))]
            lista.remove(palabra)
            tipo = palabra[1]
            palabra = palabra[0]

            # Definir coordenadas para todas las palabras
            posicionY = posicionesY.pop()
            posicionX = random.randrange(0, (N - len(palabra))) # (X, Y)

            posiciones[posicionY] = [posicionX, palabra, tipo]

        # Crear la matriz
        matriz = []
        lista_claves_palabra = []

        for y in range(N):
            linea = []

            if y in posiciones.keys(): # La línea contiene una palabra
                inicio = posiciones[y][0]
                palabra = posiciones[y][1]
                tipo = posiciones[y][2]
                claves_palabra = []
                posicion_letra = 0
            else:  # La línea no contiene una palabra
                # Defino el inicio fuera de la matriz, y así llenará todas las casillas con letras al azar
                inicio = N
                palabra = ''
                
            for x in range(N):
                if (x < inicio) or (x >= inicio + len(palabra)):
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
                else: # Colocar letra de la palabra
                    letra = palabra[posicion_letra]
                    posicion_letra += 1
                    clave = str(y) + ',' + str(x)
                    claves_palabra.append(clave)

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
            if palabra != '':
                lista_claves_palabra.append([claves_palabra, tipo])
        
        if not config.orientacion:  # Orientación Vertical
            matriz = np.transpose(matriz)

        return lista_claves_palabra, matriz

    def ayuda_frame(configu, lis_a):
        opciones =[
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
        ]

        confirmar_cancelar = [
            sg.Submit("PINTÉ UNA PALABRA", key="confirmar"),
            sg.Submit('LIMPIAR LETRAS', key='cancelar')
        ]

        sin_ayuda = [
            [
                sg.Text(
                    "Sustantivos a encontrar: " + str(cantidad_de_palabras[0]),
                    justification='right',
                    key="cant_sus"
                )
            ],
            [
                sg.Text(
                    "Adjetivos a encontar: " + str(cantidad_de_palabras[1]),
                    justification='right',
                    key="cant_adj"
                )
            ],
            [
                sg.Text(
                    "Verbos a encontrar: " + str(cantidad_de_palabras[2]),
                    justification='right',
                    key="cant_verb"
                )
            ],
            opciones,
            confirmar_cancelar,
        ]

        pal_frame = [
            [
                sg.Listbox(
                    values=list(map(lambda x:x[0], lis_a)),
                    size=(30, 6)
                )
            ],
            opciones,
            confirmar_cancelar,
        ]

        descri_frame=[
            [
                sg.Listbox(
                    values=list(map(lambda x:x[1], lis_a)),
                    size=(30, 6)
                )
            ],
            opciones,
            confirmar_cancelar,
        ]

        if configu.ayudas is False:
            return sin_ayuda
        else:
            if configu.tipo_ayudas:
                return pal_frame
            else:
                return descri_frame

    #Comprueba si hay suficientes palabras para la ejecución
    if (config.cantidad_de_palabras != [0.0, 0.0, 0.0]) and (len(config.lista_de_palabras) != 0):

        # VARIABLES IMPORTANTES

        # Matriz
        lis_palabras = generar_lis_palabras(config)
        N = max_palabra(lis_palabras)

        # Ayudas
        lis_ayuda = list(map(lambda x: [x[0], x[1]], lis_palabras))

        # Palabras 
        lista_claves_palabra, matriz = generar_matriz(N, lis_palabras)
        cantidad_de_palabras = [int(n) for n in config.cantidad_de_palabras.copy()]

        columna_izquierda = matriz
        columna_derecha = ayuda_frame(config, lis_ayuda)
        
        layout = [
            [
                sg.Column(columna_izquierda),
                sg.Column(columna_derecha)
            ],
        ]

        window = sg.Window('Sopa de letras').Layout(layout)

        # Valores iniciales para la primer ejecución
        presionadas = []
        actual = 'sustantivos'
        color = config.colores[0]

        # BUCLE DE LECTURA DE LA INTERFAZ GRÁFICA DEL JUEGO
        while True:
            event, values = window.Read()

            if event is None:
                window.Close()
                break

            elif event == 'cancelar':
                presionadas = cancelar_seleccion(presionadas)

            elif event == "confirmar":
                cantidad_de_palabras, confirmar = confirmar_seleccion(presionadas, actual, lista_claves_palabra, cantidad_de_palabras)
                presionadas = cancelar_seleccion(presionadas, confirmar)

                if not config.ayudas:
                    if actual == 'sustantivos':
                        window.Element('cant_sus').Update("Sustantivos a encontrar: " + str(cantidad_de_palabras[0]))
                    if actual == 'adjetivos':
                        window.Element('cant_adj').Update("Adjetivos a encontrar: " + str(cantidad_de_palabras[1]))
                    if actual == 'verbos':
                        window.Element('cant_verb').Update("Verbos a encontrar: " + str(cantidad_de_palabras[2]))

                # GANASTE
                # Si no quedan elementos en lista_claves_palabra es que encontraste todas

                if not lista_claves_palabra:
                    sg.PopupOK("!!!!GANASTE!!!!")
                    window.Close()
                    break

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
                    window.Element(event).Update(button_color=('black', color))

    elif len(config.lista_de_palabras) == 0:
        sg.PopupOK("Es necesario por lo menos una palabra para jugar")
    else:
        sg.PopupOK("Incremente la cantidad de palabras")

if __name__ == '__main__':
    import Configuracion.Configuracion as configuracion
    ventanajuego(configuracion.obtener_configuracion())
