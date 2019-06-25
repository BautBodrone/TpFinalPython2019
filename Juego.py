# AUTORES:
# Bodrone, Bautista
# Galati Martínez, Juan Cruz
# Zambrano Taus, Alejandro

import PySimpleGUI as sg
import random
import numpy as np


def ventanajuego(config):  # en main juego.ventanajuego(configuracion.Configuracion.obtener_configuracion())
    '''Función que ejecuta el juego.
    Recibe la configuración del usuario desde el Main.

    Contiene todas las funciones para generar la GUI y ejecutar el juego de principio a fin.'''

    # CASILLAS SELECCIONADAS 
    def confirmar_seleccion(p, actual, lista, cantidad_de_palabras):
        '''Confirma si las casillas seleccionadas corresponden a
        una palabra en la lista de palabras.
        Retorna la cantidad de palabras por tipo restantes por encontrar y si la palabra seleccionada es correcta o no.'''         
        # Lista es una lista de listas.
        # Cada lista de lista contiene: [Lista de claves, tipo] de una palabra.
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

    def cancelar_seleccion(p, correcto=False):
        '''Vacía la lista de casillas presionadas si no hay ninguna palabra confirmada como correcta.
        Si hay una palabra confirmada, actualiza sus botones para que se bloqueen.'''
        for clave in p:
            if not correcto:
                window.Element(clave).Update(button_color=('black', 'white'))
            else:
                window.Element(clave).Update(disabled=True)
        return []

    def generar_lista_de_palabras(config):
        '''Genera lista de con palabras aleatorias dependiendo del limite dado por el usuario'''
        def shuffle_pal(lista, palabras, cantidad, tipo):
            '''Toma la lista de palabras completa y la desordena,
            guardando solo la cantidad de palabras por tipo seleccionadas por el usuario'''

            temporal = list(palabras.keys())
            random.shuffle(temporal)
            for i in range(cantidad):
                try:
                    lista.append([temporal[i], palabras[temporal[i]], tipo])
                except IndexError:
                    pass

        # Generar lista de palabras        
        lista = []
        cant_sustantivos, cant_adjetivos, cant_verbos = [int(i) for i in config.cantidad_de_palabras]
        
        shuffle_pal(lista, config.sustantivos, cant_sustantivos, "sustantivos")
        shuffle_pal(lista, config.adjetivos, cant_adjetivos, "adjetivos")
        shuffle_pal(lista, config.verbos, cant_verbos, "verbos")
        
        random.shuffle(lista)
        return lista

    def generar_matriz(lista_de_palabras, mayusculas):
        '''Genera una Matriz Cuadrada de orden N.
        N se define en base a la longitud de las palabras
        
        Las palabras se colocan al azar en distintas filas, iniciando en un punto al azar de la columna.

        Retorna una lista de listas y la matríz,
        Cada lista contiene las coordenadas y tipo de palabra de las palabras colocadas en la matríz
        La matríz es rellenada con letras al azar, excepto en las coordenadas correspondientes a las palabras,
        donde se colocan, obviamente, las letras correspondientes a cada palabra'''

        def max_palabra(lista_de_palabras):
            '''Define la cantidad de casillas de la Matriz.
            Como mínimo será de la cantidad de palabras a colocar'''
            max = 0
            for palabra in lista_de_palabras:
                if len(palabra[0]) > max:
                    max = len(palabra[0])
                    
            if max < len(lista_de_palabras):
                max = len(lista_de_palabras)

            # Para que la palabra más larga no quede pegada a los bordes,
            # se agregan 1 o 2 casillas extra
            return max + random.randint(1, 2) 

        N = max_palabra(lista_de_palabras)

        lista = list(map(lambda x: [x[0], x[2]], lista_de_palabras)) # hace una lista solo con las palabras y su tipo
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

        # CREAR LA MATRÍZ
        matriz = []
        lista_claves_palabra = []

        for y in range(N):
            # Por cada fila en la matríz
            fila = []

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
                # Por cada columna en la fila
                if (x < inicio) or (x >= inicio + len(palabra)): # Colocar letra al azar antes y después de la palabra
                    letra = chr(random.randint(ord('a'), ord('z')))
                    clave = str(y) + ',' + str(x)
                else: # Colocar letra de la palabra
                    letra = palabra[posicion_letra]
                    posicion_letra += 1
                    clave = str(y) + ',' + str(x)
                    claves_palabra.append(clave)

                if mayusculas:
                    letra = letra.upper()
                else:
                    letra = letra.lower()

                # Crear casilla (botón)                
                fila.append(
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

            # Guardar fila
            matriz.append(fila)

            if palabra != '': # Si hay una palabra en la fila, guarda sus claves y tipo
                lista_claves_palabra.append([claves_palabra, tipo])
        
        if not config.orientacion:  # Orientación Vertical
            matriz = np.transpose(matriz)

        return matriz, lista_claves_palabra

    def ayuda_frame(ayudas, tipo_ayudas, lista_de_ayudas):
        '''Estructura de la columna derecha.
        Si se configuraron ayudas, muestra el tipo de ayuda seleccionada;
        sino, la cantidad de palabras restantes por encontrar.'''
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
                    values=list(map(lambda x:x[0], lista_de_ayudas)),
                    size=(30, 6)
                )
            ],
            opciones,
            confirmar_cancelar,
        ]

        descri_frame=[
            [
                sg.Listbox(
                    values=list(map(lambda x:x[1], lista_de_ayudas)),
                    size=(30, 6)
                )
            ],
            opciones,
            confirmar_cancelar,
        ]

        if ayudas is False:
            return sin_ayuda
        else:
            if tipo_ayudas:
                return pal_frame
            else:
                return descri_frame


    # INICIO DE LA EJECUCIÓN
    #Comprueba si hay suficientes palabras para la ejecución
    if (config.cantidad_de_palabras != [0.0, 0.0, 0.0]) and (len(config.lista_de_palabras) != 0):

        # VARIABLES
        lista_de_palabras = generar_lista_de_palabras(config)
        lista_de_ayudas = list(map(lambda x: [x[0], x[1]], lista_de_palabras))
        matriz, lista_claves_palabra = generar_matriz(lista_de_palabras, config.mayusculas)
        cantidad_de_palabras = [int(n) for n in config.cantidad_de_palabras.copy()]

        # Definición de la GUI
        layout = [
            [
                sg.Column(matriz),
                sg.Column(ayuda_frame(config.ayudas, config.tipo_ayudas, lista_de_ayudas))
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
                    # Actualizar palabras restantes en la sección de ayudas, si no hay ayudas
                    if actual == 'sustantivos':
                        window.Element('cant_sus').Update("Sustantivos a encontrar: " + str(cantidad_de_palabras[0]))
                    if actual == 'adjetivos':
                        window.Element('cant_adj').Update("Adjetivos a encontrar: " + str(cantidad_de_palabras[1]))
                    if actual == 'verbos':
                        window.Element('cant_verb').Update("Verbos a encontrar: " + str(cantidad_de_palabras[2]))

                # GANASTE
                # Si no quedan elementos en lista_claves_palabra es que encontraste todas
                if not lista_claves_palabra:
                    sg.PopupOK("!!!!GANASTE!!!!", font=('comic sans', 30, 'bold'))
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

    elif len(config.lista_de_palabras) == 0: # No hay palabras en la lista de palabras
        sg.PopupOK("Es necesario por lo menos una palabra para jugar")
    else: # La configuración de cantidad_de_palabras tiene todos los valores en 0
        sg.PopupOK("Incremente la cantidad de palabras desde la Configuración")

if __name__ == '__main__':
    import Configuracion.Configuracion as configuracion
    ventanajuego(configuracion.obtener_configuracion())
