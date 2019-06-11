class Usuario:

    def __init__(self, nombre = "default", contrasena = "default"):
        '''El inicializador de la clase Usuario recibe un nombre y una contrasena, a la vez que automaticamente genera un diccionario vacio para cada tipo de palabra, y una configuracion default'''
        self.nombre = nombre
        self.contrasena = contrasena
        self.sustantivos = {}
        self.adjetivos = {}
        self.verbos = {}
        self.config = {"nombre": nombre,
                       "contrasena": contrasena,
                       "config_colores": (),
                       "ayudas": False,
                       "orientacion": False,
                       "cantpalabras": (),
                       "maymin": False,
                       "tipografia": "arial 10"
                       }

    def setnombre(self, nombre):
        self.nombre = nombre

    def getnombre(self):
        return self.nombre

    def setcontrasena(self, contrasena):
        self.contrasena = contrasena

    def getcontrasena(self):
        return self.contrasena

    def checkearcontrasena(self, ingresada):
        '''Checkea si la contrasena ingresada coincide con la del usuario ingresado.'''
        if lower.ingresada == lower.contrasena:
            return True
        else:
            return False

    def sumarsustantivo(self, palabra, descripcion):
        self.sustantivos[palabra] = descripcion

    def getsustantivos(self):
        return self.sustantivos

    def sumaradjetivo(self, palabra, descripcion):
        self.adjetivos[palabra] = descripcion

    def getadjetivos(self):
        return self.adjetivos

    def sumarverbo(self, palabra, descripcion):
        self.verbos[palabra] = descripcion

    def getverbos(self):
        return self.verbos

    def eliminarpalabra(self, palabra):
        '''Checkea si la palabra existe en alguno de los diccionarios, y procede a eliminarla'''
        if palabra in self.sustantivos.keys():
            del self.sustantivos[palabra]
        elif palabra in self.adjetivos.keys():
            del self.adjetivos[palabra]
        elif palabra in self.verbos.keys():
            del self.verbos[palabra]

    def setconfig(self, **configuracion):
        '''Recibe un diccionario con las modificaciones a la configuracion, en caso de que un valor sea distinto de None, lo modifica'''
        for clave, valor in configuracion.items():
            if valor is not None:
                self.config[clave] = valor

    def getconfig(self):
        return self.config
