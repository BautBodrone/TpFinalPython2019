import json

class Configuracion:
    def __init__(
            self,
            sustantivos = {
                'casa':'desc'
            },
            adjetivos = {
                'alto':'desc'
            },
            verbos = {
                'correr':'desc'
            },
            cantidad_de_palabras = (1.0,1.0,1.0),
            ayudas = True,
            tipo_ayuda = True,
            mayusculas = True,
            colores = ('#FF0000', '#00FF00', '#0000FF'),
            oficina = None
        ):
        self.sustantivos = sustantivos
        self.adjetivos = adjetivos
        self.verbos = verbos
        self._lista_de_palabras = self._generar_lista_de_palabras(self.sustantivos, self.adjetivos, self.verbos)
        self.cantidad_de_palabras = cantidad_de_palabras
        self.ayudas = ayudas
        self.tipo_ayuda = tipo_ayuda
        self.mayusculas = mayusculas
        self.colores = colores
        self.oficina = oficina

    @property
    def lista_de_palabras(self):
        return self._generar_lista_de_palabras(self.sustantivos, self.adjetivos, self.verbos)

    def _generar_lista_de_palabras(self, sustantivos, adjetivos, verbos):
        def generar_lista_de(dic, tipo):
            return list(map(lambda palabra: [palabra, tipo, len(palabra)], dic.keys()))

        lista_de_palabras = generar_lista_de(sustantivos, "Sustantivo")
        lista_de_palabras += generar_lista_de(adjetivos, "Adjetivo")
        lista_de_palabras += generar_lista_de(verbos, "Verbo")

        return lista_de_palabras

    def agregar_sustantivo(self, palabra, descripcion):
        self.sustantivos[palabra] = descripcion

    def agregar_adjetivo(self, palabra, descripcion):
        self.adjetivos[palabra] = descripcion

    def agregar_verbo(self, palabra, descripcion):
        self.verbos[palabra] = descripcion


    def borrar_palabra(self, palabra):
        if palabra in self.sustantivos.keys():
            del self.sustantivos[palabra]
        elif palabra in self.adjetivos.keys():
            del self.adjetivos[palabra]
        elif palabra in self.verbos.keys():
            del self.verbos[palabra]

def obtener_configuracion():
    try:
        archivo_configuracion = open('/configuracion/usuario.txt', 'r')
    except:
        configuracion = Configuracion()
    else:
        print('')

    return configuracion
