# AUTORES:
# Bodrone, Bautista
# Galati Martínez, Juan Cruz
# Zambrano Taus, Alejandro
#
# GPL-3.0-or-later

import json

def promedio (n_oficina):

    def determinar_tema(promedio):
        if (promedio < 10.0):
            return ['steelblue', 'lightcyan', 'lightslategray', 'lavender']
        elif (promedio > 10.0) and (promedio < 20.0):
            return ['palegoldenrod', 'tomato', 'sandybrown', 'seashell']
        else:
            return ['tomato', 'darkred', 'firebrick', 'gold']

    arch = open("dato-oficinas.json", "r")
    oficinas = json.load(arch)

    promedio = 0
    oficina = oficinas[n_oficina]
    temperatura = list(map(lambda x: x["temp"], oficina))
    for n in range(len(temperatura)):
        promedio += oficinas[n_oficina][n]["temp"]
    promedio = promedio/len(temperatura)
    return (determinar_tema(promedio))


if __name__ == '__main__':
    promedio()
