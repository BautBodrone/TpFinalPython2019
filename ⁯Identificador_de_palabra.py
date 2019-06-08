from pattern.web import Wiktionary
from pattern.es import parse
import PySimpleGUI as sg


def identificador (palabra): ##palabra = gato para testeo

    """"Retorno una lista con la palabra y que tipo es para mandarla a la tabla """

    palabra = palabra.lower()##solo encuntra palabras en minuscula
    engine = Wiktionary(license=None, throttle=5.0, language="es")
    match = False
    wik = False
    patt = False

    try:
        art = engine.search(palabra)
        section = art.sections
    except AttributeError:
        section = "error"

    if section != "error":
        lis = section[3]
        if ("Sustantivo" in lis.title) or ("Adjetivo" in lis.title) or ("Verbo" in lis.title):
            tag = lis.title
            lis = [[palabra, tag]]
            wik = True
            print(lis)
    try:
        patt_es = parse(str(palabra), tokenize=False, tags=True, chunks=False)
        patt = True
    except AttributeError: ##puse esto para poner algo ya que no se que error puede tirar
        patt_es = "error"

    if patt_es != "error":
        if wik==True:
            definicion = sg.PopupGetText("Palabra No Encontrada en wiki", "Ingrese definicion") ## para guardar en archivo local
            if ("NN" in patt_es):
                lis = [[palabra, "Sustantivo"]]
            elif ("VB" in patt_es):
                lis = [[palabra, "Verbo"]]
            elif ("JJ" in patt_es):
                lis = [[palabra, "Adjetivo"]]
        elif (("NN" in patt_es) and ("Sustantivo" in tag)) or (("VB" in patt_es) and ("verbo" in tag)) or (("JJ" in patt_es) and ("Adjetivo" in tag)):
            match = True

    return lis

identificador("Gato")
