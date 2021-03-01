#!/usr/bin/env python
# coding: utf-8

import PyPDF2 as pyp  # Documentation at:
# https://pythonhosted.org/PyPDF2/
import os
import sys
from os.path import join as joinPath

# Directorio raíz del proyecto
ROOT_DIR = os.path.abspath("../")

# Importa Mask RCNN
if ROOT_DIR not in sys.path:
    # para encontrar la versión local de la biblioteca
    sys.path.append(ROOT_DIR)

# Aqui se importan mis paquetes
from packages.module import set_length, sort, twoByTwo, link_merged, orientate_page
from packages import inputDir

fileName = sorted(os.listdir(inputDir))[-1]
filePath = joinPath(inputDir, fileName)
inFile = open(filePath, 'rb')
inPdf = pyp.PdfFileReader(inFile)
outPdf = pyp.PdfFileWriter()

# ========================= DEFINE VARIABLES ========================= #

N = inPdf.getNumPages()  # obtienes el número de páginas del archivo de entrada
Page0 = inPdf.getPage(0)  # Page0 es la primera página (class PageObect)
# Page1 = inPdf.getPage(1) # Page1 es la segunda página (class PageObect)
PageShape = Page0.mediaBox  # dimensiones de página en pts
# (1pt = 1/72 inch = 2,54/72 cm)
PageWidth = float(PageShape[2]) * (2.54 / 72)  # anchura de página en cm
PageHeight = float(PageShape[3]) * (2.54 / 72)  # altura de página en cm
dinA = [PageHeight, PageWidth]

# ========================= RUN the PROGRAM ========================= #

# Añade páginas blancas al final del archivo original (poner una firma en la última página)
ExtraPagesPdf, f, addblank = set_length(inPdf, N, f=5)

# la variable _N es el nuevo número de páginas
_N = ExtraPagesPdf.getNumPages()
print(f'Now, {fileName} has {_N} pages')

# Ordena las páginas y devuelve el orden
SortedPdf, correct_order = sort(ExtraPagesPdf, N, f, addblank, PageWidth)
print('Pages ordered!')

# Empaca de dos en dos
twoBy2 = twoByTwo(SortedPdf, correct_order)
print('Merged two by two.')

# Las mete en el mismo pdf
almostFinalPdf = link_merged(twoBy2)
print('Now, stored\'em all in the same pdf')

# número de páginas empacadas en el nuevo pdf
_fN = almostFinalPdf.getNumPages()
print(f'With {_fN} pages')

# Orienta las páginas para imprimir por el borde largo sin rayarse
orientate_page(almostFinalPdf, _fN)

print(f'Now you can use {fileName[:-4]}_Booklet.pdf as you want!')
inFile.close()
# signFile.close()


'''
TO DO:
    Que la carpeta output se genere si no existe
    Ya la hostia:
        Programar una ventanita con botones y todo el rollo
        Hacer esto en JavaScript para que salga una ventanita html.
'''
