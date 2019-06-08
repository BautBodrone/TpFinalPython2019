class Usuario:

    def __init__(self, nombre = "default", contrasena = "default"):
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
        if palabra in self.sustantivos.keys():
            del self.sustantivos[palabra]
        elif palabra in self.adjetivos.keys():
            del self.adjetivos[palabra]
        elif palabra in self.verbos.keys():
            del self.verbos[palabra]

    def setconfig(self, **configuracion):
        for clave, valor in configuracion.items():
            if valor is not None:
                self.config[clave] = valor

    def getconfig(self):
        return self.config

usuario1 = Usuario()