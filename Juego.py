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

    Contiene todas las funciones para generar la GUI y ejecutar el juego de principio a fin.
    '''


    def generar_lista_de_palabras(config, cantidad_de_palabras):
        '''Genera lista de con palabras aleatorias dependiendo del limite dado por el usuario

        Retorna una lista con las palabras a usar en el juego, su descripción y tipo
        '''

        def shuffle_pal(lista_de_palabas, palabras, cantidad_de_palabras, tipo):
            '''Toma la lista de palabras de un tipo de palabras y la desordena,
            guardando solo la cantidad de palabras por tipo seleccionadas por el usuario
            '''
            temporal = list(palabras.keys())
            random.shuffle(temporal)
            for i in range(cantidad_de_palabras):
                try:
                    lista_de_palabas.append([temporal[i], palabras[temporal[i]], tipo])
                except IndexError:
                    pass
                
        lista = []

        shuffle_pal(lista, config.sustantivos, cantidad_de_palabras[0], "sustantivos")
        shuffle_pal(lista, config.adjetivos, cantidad_de_palabras[1], "adjetivos")
        shuffle_pal(lista, config.verbos, cantidad_de_palabras[2], "verbos")

        random.shuffle(lista)
        return lista
        

    def max_palabra(lista_de_palabas):
        '''Define la cantidad de casillas de la Matriz.
        Como mínimo será de la cantidad de palabras a colocar
        '''
        
        max = 0
        for i in lista_de_palabas:
            if len(i[0]) > max:
                max = len(i[0])
        if max < len(lista_de_palabas):
            max = len(lista_de_palabas)
        return max
    
    def generar_matriz(lista_de_palabras, config):
        '''Genera una Matriz Cuadrada de orden N.
        N se define en base a la longitud de las palabras (en la función max_palabra())
        
        Las palabras se colocan al azar en distintas filas, iniciando en un punto al azar de la columna.

        Modifica
        Lista de palabras. Originalmente, la lista de palabras contiene [palabra, descripción, tipo],
        al salir de esta función, contiene [claves_palabra, palabra, descripción, tipo], donde
        claves_palabra es una lista de las coordenadas de las letras de la palabra.

        Retorna,
        La matriz, la grilla de juego.
        La matriz es una lista de listas, rellenada con letras al azar,
        excepto en las coordenadas correspondientes a las palabras,
        donde se colocan, obviamente, las letras correspondientes a cada palabra
        '''

        # Variables principales
        N = max_palabra(lista_de_palabas) + random.randint(1, 2)  # para que la palabra mas grande no quede siempre pegada a los bordes      
        filas_con_palabras = sorted(random.sample(range(0, N), k=len(lista_de_palabras)))
        matriz = []

        # Inicializar variables
        indice_palabra_actual = 0
        for y in range(N):
            # Por cada fila en la matriz
            fila = []
            
            if y in filas_con_palabras: #Si hay una palabra en la fila
                # Obtener palabra
                datos_palabra = lista_de_palabras[indice_palabra_actual]
                palabra = datos_palabra[0]

                inicio = random.randrange(0, N-len(datos_palabra[0]))
                claves_palabra = []
                letra_actual = 0
            else: # Si no hay una palabra en la fila
                inicio = N
                palabra = ''

            for x in range(N):
                # Por cada columna en la fila
                clave = str(y) + ',' + str(x)

                if (x <= inicio) or (x > inicio + len(palabra)): # Coloco letra al azar
                    letra = letra = chr(random.randint(ord('a'), ord('z')))
                    
                else: # Coloco letra correspondiente a la palabra
                    letra = palabra[letra_actual]
                    letra_actual += 1
                    claves_palabra.append(clave)                    
                
                if config.mayusculas:
                    letra = letra.upper()

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

            if palabra != '':
                lista_de_palabras[indice_palabra_actual] = [
                    # el conenido de datos_palabra es [palabra, descripcion, tipo]
                    claves_palabra, datos_palabra[0], datos_palabra[1], datos_palabra[2]
                ]
                indice_palabra_actual += 1

        if config.orientacion is False:  # vertical
            matriz = np.transpose(matriz)

        return matriz

    def columna_derecha(config, cantidad_de_palabras, lista_de_ayudas):
        '''Estructura de la columna derecha.
        Si se configuraron ayudas, muestra el tipo de ayuda seleccionada;
        sino, la cantidad de palabras restantes por encontrar.'''

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
        ]


        ayuda_palabras = [
            [
                sg.Table(
                    values=list(map(lambda x: [x[0].capitalize()], lista_de_ayudas)),
                    headings=['Palabras a encontrar'.upper()],
                    vertical_scroll_only = False,
                    justification='center',
                    key='ayuda_palabras',
                    size=(60,6)
                )
            ],
        ]

        ayuda_descripcion = [
            [
                sg.Table(
                    values=list(map(lambda x: [x[1].capitalize()], lista_de_ayudas)),
                    headings=['Palabras a encontrar'.upper()],
                    vertical_scroll_only = False,
                    justification='left',
                    key='ayuda_descripcion',
                    size=(60,6)
                )
            ],
        ]

        if config.ayudas is False:
            ayuda_frame = sg.Frame('Palabras restantes',sin_ayuda)
        else:
            if config.tipo_ayudas:
                ayuda_frame = sg.Column(ayuda_palabras)
            else:
                ayuda_frame = sg.Column(ayuda_descripcion)

        columna_derecha = [
            [
                ayuda_frame
            ],
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
                sg.Submit("Seleccionar Palabra", key="confirmar"),
                sg.Submit('Cancelar Palabra', key='cancelar')
            ],
        ]

        return columna_derecha

    def confirmar_seleccion(p, actual, lista_de_palabas, cantidad_de_palabras, config, correcto=False):
        '''Confirma si las casillas seleccionadas corresponden a una palabra en la lista de palabras.

        Retorna si la palabra seleccionada es correcta o no.
        '''     
        for i in range(len(lista_de_palabas)):
            correcto = (set(p) == set(lista_de_palabas[i][0])) and (actual == lista_de_palabas[i][3])
            print(correcto)
            if correcto:
                break

        if correcto:          
            if lista_de_palabas[i][3] == "sustantivos":
                cantidad_de_palabras[0] -= 1
            elif lista_de_palabas[i][3] == "adjetivos":
                cantidad_de_palabras[1] -= 1
            else:
                cantidad_de_palabras[2] -= 1

            lista_de_palabas.remove(lista_de_palabas[i]) # Borrar palabra de la lista
                    
        return correcto

    def cancelar_seleccion(p, correcto=False):
        '''Vacía la lista de casillas presionadas si no hay ninguna palabra confirmada como correcta.

        Si hay una palabra confirmada, actualiza sus botones para que se bloqueen.

        Retorna una lista vacía.
        '''
        for clave in p:
            if not correcto:
                window.Element(clave).Update(button_color=('black', 'white'))
            else:
                window.Element(clave).Update(disabled=True)
        return []

    # INICIO DE LA EJECUCIÓN
    # Comprueba si hay suficientes palabras para la ejecución
    if (config.cantidad_de_palabras != [0.0, 0.0, 0.0]) and (len(config.lista_de_palabras) != 0):

        # VARIABLES
        cantidad_de_palabras = [int(cant) for cant in config.cantidad_de_palabras.copy()]
        lista_de_palabas = generar_lista_de_palabras(config, cantidad_de_palabras)
        lista_de_ayudas = list(map(lambda x: [x[0], x[1]], lista_de_palabas))
        random.shuffle(lista_de_ayudas)

        # DEFINICIÓN DE LA INTERFAZ GRÁFICA

        # generar_matriz modifica lista_de_palabras
        matriz = generar_matriz(lista_de_palabas, config)
        
        layout = [
            [
                sg.Column(matriz),
                sg.Column(columna_derecha(config, cantidad_de_palabras, lista_de_ayudas))
            ]
        ]

        window = sg.Window('Sopa de letras').Layout(layout)
        event, values = window.Read()

        # Valores iniciales para la primer ejecución
        presionadas = []
        actual = 'sustantivos'
        color = config.colores[0]

        if set(config.cantidad_de_palabras) == [0, 0, 0]:
            sg.PopupOK("Incremente el numero de palabras")

        # BUCLE DE LECTURA DE LA INTERFAZ GRÁFICA DEL JUEGO
        while True:
            if event is None:
                window.Close()
                break

            elif event == "confirmar":
                confirmar = confirmar_seleccion(presionadas, actual, lista_de_palabas, cantidad_de_palabras, config)
                presionadas = cancelar_seleccion(presionadas, confirmar)

                if confirmar is False:
                    sg.PopupAutoClose("Intente de nuevo", auto_close_duration=1)
                else:

                    # Actualizar ayudas
                    if config.ayudas is False:
                        window.Element("cant_sus").Update(value="Sustantivos a encontrar: " + str(cantidad_de_palabras[0]))
                        window.Element("cant_adj").Update(value="Adjetivos a encontrar: " + str(cantidad_de_palabras[1]))
                        window.Element("cant_verb").Update(value="Verbos a encontrar: " + str(cantidad_de_palabras[2]))
                    else:
                        lista_de_ayudas = list(map(lambda x: [x[1], x[2]], lista_de_palabas))
                        
                        if config.tipo_ayudas:
                            window.Element('ayuda_palabras').Update(values=list(map(lambda x: [x[0].capitalize()], lista_de_ayudas)))
                        else:
                            window.Element('ayuda_descripcion').Update(values=list(map(lambda x: [x[1].capitalize()], lista_de_ayudas)))

                    # GANASTE
                    # Si no quedan elementos en lista_de_palabras es que encontraste todas
                    if not lista_de_palabas:
                        sg.PopupOK("!!!!GANASTE!!!!")
                        window.Close()
                        break

            elif event == 'cancelar':
                presionadas = cancelar_seleccion(presionadas)

            elif event in ('adjetivos', 'sustantivos', 'verbos'):
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

            event, values = window.Read()

    elif len(config.lista_de_palabras) == 0:
        sg.PopupOK("Es necesario por lo menos una palabra para jugar")
    else:
        sg.PopupOK("Incremente la cantidad de palabras")


if __name__ == '__main__':
    import Configuracion.Configuracion as configuracion
    
    ventanajuego(configuracion.obtener_configuracion())
