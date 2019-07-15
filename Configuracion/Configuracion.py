# AUTORES:
# Bodrone, Bautista
# Galati Martínez, Juan Cruz
# Zambrano Taus, Alejandro

import json
from os import sep #Mantiene el acceso a archivos generico entre sistemas operativos

class ConfigEncoder(json.JSONEncoder):
    '''Adapta los datos de la clase Configuracion para poder enviarlos a un archivo con formato .json'''
    def default(self, obj):
        return obj.__dict__
    

class Configuracion:
    '''Clase que guarda la información de configuración del usuario'''
    def __init__(
            self,
            sustantivos = {
                "casa": "descripcion",
                "perro": "descripcion",
                "comida": "descripcion",
                "teclado": "descripcion",
                "cuaderno": "descripcion"
            },
            adjetivos = {
                "alto": "descripcion",
                "lindo": "descripcion",
                "chino": "descripcion",
                "rapido": "descripcion",
            },
            verbos = {
                "correr": "descripcion",
                "saltar": "descripcion",
                "nadar": "descripcion"
            },
            cantidad_de_palabras = (3,3,3),
            ayudas = True,
            tipo_ayudas = True,
            mayusculas = True,
            orientacion = True,
            colores = ['#FF0000','#00FF00','#0000FF'],
            oficina_actual = 'oficina1',
            oficinas = ["oficina1", "oficina2"],
            tipografias = ["Verdana", "Helvetica", "Comic", "Times", "Fixedsys "],
            tipografia = "arial"
        ):
        self.sustantivos = sustantivos
        self.adjetivos = adjetivos
        self.verbos = verbos
        self._lista_de_palabras = self._generar_lista_de_palabras(self.sustantivos, self.adjetivos, self.verbos)
        self.cantidad_de_palabras = cantidad_de_palabras
        self.ayudas = ayudas
        self.tipo_ayudas = tipo_ayudas
        self.mayusculas = mayusculas
        self.orientacion = orientacion
        self.oficina_actual = oficina_actual
        self.oficinas = oficinas
        self.colores = colores
        self.tipografias = tipografias
        self.tipografia = tipografia

    @property
    def lista_de_palabras(self):
        '''Retorna la lista de palabras'''
        return self._generar_lista_de_palabras(self.sustantivos, self.adjetivos, self.verbos)

    def _generar_lista_de_palabras(self, sustantivos, adjetivos, verbos):
        '''Recibe los diccionarios de palabras por tipo, y los agrupa en una única lista de listas,
        en las que se guarda la palabra y su tipo'''
        def generar_lista_de(dic, tipo):
            '''Genera una lista de listas de uno de los diccionarios,
            en cada lista se guarda la palabra y su tipo'''
            return list(map(lambda palabra: [palabra, tipo], dic.keys()))

        lista_de_palabras  = generar_lista_de(sustantivos, "Sustantivo")
        lista_de_palabras += generar_lista_de(adjetivos, "Adjetivo")
        lista_de_palabras += generar_lista_de(verbos, "Verbo")

        return lista_de_palabras

    def agregar_palabra(self, palabra, tipo, descripcion):
        '''Recibe una palabra y su tipo y la añade al atributo correspondiente a su tipo'''
        if tipo == 'Sustantivo':
            self.sustantivos[palabra] = descripcion
        elif tipo == 'Adjetivo':
            self.adjetivos[palabra] = descripcion
        elif tipo == 'Verbo':
            self.verbos[palabra] = descripcion            

    def borrar_palabra(self, palabra):
        '''Busca la palabra en los 3 atributos que guardan palabras, si la encuentran, la borran.'''
        if palabra in self.sustantivos.keys():
            del self.sustantivos[palabra]
        elif palabra in self.adjetivos.keys():
            del self.adjetivos[palabra]
        elif palabra in self.verbos.keys():
            del self.verbos[palabra]

    def to_dict(self):
        '''Convierte la clase en diccionario'''
        return self.__dict__

    def get_colores(self):
        '''Es un getter de colores... que creo que no se usa'''
        return self.colores


def obtener_configuracion():
    '''Función que busca y abre el archivo de configuración.
    Si no lo encuentra o no lo puede abrir, genera uno nuevo con valores por defecto'''
    def generar_configuracion():
        '''Genera un nuevo archivo de configuración con valores por defecto'''
        print('Generar configuración por defecto')
        configuracion = Configuracion()
        
        print('Configuración por defecto creada')
        print('Abrir/crear archivo config.json')
        archivo_configuracion = open('configuracion' + sep + 'config.json', 'w+')
        
        print('Archivo abierto/creado con éxito')
        print('Serializando configuración y guardarla en config.json')
        json.dump(configuracion, archivo_configuracion, cls=ConfigEncoder, indent=4)
        
        print('Configuración serializada y guardada en config.json con éxito')

        return configuracion
        
    try:
        print('\n# ' + '='*30 + ' #\n')
        print('Buscando archivo config.json')
        archivo_configuracion = open('configuracion' + sep + 'config.json', 'r')
        
        print('Archivo config.json abierto con éxito')
    except:
        print('No se pudo abrir config.json')
        print('Generar configuración por defecto')
        configuracion = generar_configuracion()
        
        print('Configuración por defecto creada y cargada con éxito')

    else:
        try:
            print('Intentando cargar configuración desde config.json')
            c = json.load(archivo_configuracion)
            
            print('Archivo config.json cargado con éxito')
            configuracion = Configuracion(
                sustantivos=c['sustantivos'],
                adjetivos=c['adjetivos'],
                verbos=c['verbos'],
                cantidad_de_palabras=c['cantidad_de_palabras'],
                ayudas=c['ayudas'],
                tipo_ayudas=c['tipo_ayudas'],
                mayusculas=c['mayusculas'],
                orientacion=c["orientacion"],
                colores=c['colores'],
                oficinas = c['oficinas'],
                oficina_actual = c['oficina_actual'],
                tipografia = c["tipografia"]
            )
            
            print('Objeto Configuración creado con éxito')

        except:
            print('Un error ocurrió al cargar config.json')
            print('Generar configuración por defecto')
            configuracion = generar_configuracion()
            print('Configuración por defecto cargada con éxito')

    # Imprime la configuración actual, para facilitar la depuración.
    print('\n' + '='*30 + '\n')
    print('Configuración actual: ')
    configuracion_actual = configuracion.__dict__
    for key, value in configuracion_actual.items():
        if type(value) is dict:
            print('  > ' + str(key) + ': ')
            for k, v in value.items():
                print('    > ' + str(k) + ': ' + str(v))
        elif type(value) is list:
            print('  > ' + str(key) + ': ')
            for element in value:
                print('    > ' + str(element))

        else:
            print('  > ' + str(key) + ': '  + str(value))
    print('\n' + '=' * 30 + '\n')

    return configuracion

def guardar_configuracion(configuracion):
    '''Busca el archivo de configuración y guarda los cambios realizados desde GUI_Configuracion.py.
    Si lo encuentra, lo sobreescribe; sino, lo crea'''
    
    exito = False
    try:
        print('\n# ' + '='*30 + ' #\n')
        print('Abrir/crear archivo config.json')
        archivo_configuracion = open('configuracion' + sep + 'config.json', 'w+')
        
        print('Archivo abierto/creado con éxito')
        print('Serializar configuración y guardarla en config.json')
        json.dump(configuracion, archivo_configuracion, cls=ConfigEncoder, indent=4)
        
        print('Configuración serializada y guardada en config.json con éxito')
    except:
        print('Ocurrió un error')
        exito = False
        print('\n# ' + '='*30 + ' #\n')
    else:
        exito = True
        print('\n# ' + '='*30 + ' #\n')

    return exito
        
