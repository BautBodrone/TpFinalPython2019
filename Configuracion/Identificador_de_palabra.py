from pattern.web import Wiktionary
from pattern.text.es import parse
import PySimpleGUI as sg
from datetime import datetime


def identificador (palabra):

    """"Retorno una lista con la palabra y que tipo es para mandarla a la tabla """

    palabra = palabra.lower()##solo encuntra palabras en minuscula
    engine = Wiktionary(license=None, throttle=5.0, language="es")
    match = False
    wik = False
    patt = False
    lis = []

    try:
        art = engine.search(palabra)
        section = art.sections
    except AttributeError:
        section = "error"

    if section != "error":
        lis = section[3]
        descr = section[3].string
        descr = ((((descr.split("2"))[0].split("1"))[1]).split("*")[0]).split("\n")[0]
        if ("Sustantivo" in lis.title) or ("Adjetivo" in lis.title) or ("Verbo" in lis.title):
            tag = lis.title.split(" ")[0]
            lis = [[palabra, tag, descr]]
            wik = True

    try:
        patt_es = parse(palabra, tokenize=False, tags=True, chunks=False).split("/")[1]
        patt = True
    except AttributeError:
        patt_es = "error"

    if patt_es != "error":
        print(patt_es)
        if wik is False:
            definicion = sg.PopupGetText("Palabra No Encontrada en wiki", "Ingrese definicion") ## para guardar en archivo local
            if "NN" in patt_es:
                lis = [[palabra, "Sustantivo", definicion]]
            elif "VB" in patt_es:
                lis = [[palabra, "Verbo", definicion]]
            elif "JJ" in patt_es:
                lis = [[palabra, "Adjetivo", definicion]]
        if wik is True:
            if(("NN" in patt_es) and ("Sustantivo" in tag)) or (("VB" in patt_es) and ("Verbo" in tag)) or\
                    (("JJ" in patt_es) and ("Adjetivo" in tag)):
                match = True
        patt = True

    if (wik is False) or (patt is False) or (match is False):
        file = open("reporte.txt", "a+")
        fechahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        reporte = ""
        if (wik is False) and (patt is True):
             reporte = "La palabra "+palabra+" no fue encontrada en wiki. "+fechahora
        elif (wik is True) and (patt is False):
            reporte = "La palabra "+palabra+" no fue encontrada en pattern.es. "+fechahora
        elif (wik is False) and (patt is False):
            reporte = "La palabra "+palabra+" no fue encontrada en ninguno de los dos sitios. "+fechahora
        elif (match is True):
            reporte = "La clasificacion de la palabra "+palabra+" no conicide. "+fechahora
        file.write(reporte)
        file.write("\n")
        file.close()

    return lis

if __name__ == '__main__':
    identificador("")
