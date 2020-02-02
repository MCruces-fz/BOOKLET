# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 22:22:22 2020

@author: Miguel
"""

import PyPDF2 as pyp # Documentation at:
# https://pythonhosted.org/PyPDF2/
from PyPDF2.pdf import PageObject # Documentation at:
# https://pythonhosted.org/PyPDF2/PageObject.html
import numpy as np
import os
#from os import listdir
from os.path import join as joinPath

import sys

# Directorio raíz del proyecto
ROOT_DIR = os.path.abspath("../")

# Importa Mask RCNN
if ROOT_DIR not in sys.path:
    # para encontrar la versión local de la biblioteca
    sys.path.append(ROOT_DIR)

from packages import inputDir, outputDir, filesDir

fileName = sorted(os.listdir(inputDir))[-1]
filePath = joinPath(inputDir, fileName)
inFile = open(filePath, 'rb')
inPdf = pyp.PdfFileReader(inFile)
outPdf = pyp.PdfFileWriter()

signPath = joinPath(filesDir, "signature.pdf")
signFile = open(signPath, 'rb')
signature = pyp.PdfFileReader(signFile)
signPage = signature.getPage(0)
signPyPDF2 = signature.getPage(1)

#================ FUNCTIONS ===============#

# it adds a number of addblank pages to the end of the file
def add_pages(inPdf, addblank):
    # create the output file
    outPdf.appendPagesFromReader(inPdf)
    for i in range(addblank):
        if i==0:
            outPdf.addPage(signPage)
            continue
        if i==1:
            outPdf.addPage(signPyPDF2)
            continue
#    # save the changes in extra_pages
#     savePath = joinPath(outputDir, 'extra_pages.pdf')
#     with open(savePath, 'wb') as outfile:
#         outPdf.write(outfile)
        # add one page in each loop, in addblank loops
        outPdf.addBlankPage()
    return outPdf

# it adds the necessary pages to the end of the file, with add_pages
def set_length(inPdf, N, f=False):
    #=========== SHEETS PER BOOKLET ===========#
    if N == 1:
        print(f'This pdf has N = {N} page.')
    else:
        print(f'This pdf has N = {N} pages.')
    if f == False:
        f = 4
    #========== SET ADDBLANK NUMBER ==========#
    remaining = N%(4*f)
    if remaining != 0:
        addblank = 4*f - remaining
    else:
        addblank = 0
    if addblank > 1 and addblank < 4*f:
        print(f'So, with {f} sheets per booklet, we need to add {addblank} blank pages at the end of the pdf.')
    if addblank == 1:
        print('So, with {f} sheets per booklet, we need to add {addblank} blank page at the end of the pdf.')
    if addblank == 0:
        print('So that is exactly that we need.')
        addblank = 4*f
    #========== ADD PAGES AT THE END ==========#
    extra_pages = add_pages(inPdf,addblank)
    return extra_pages, f, addblank # remember to close 'outfile' file

# ExtraPagesPdf, f, addblank = set_length(inPdf, N, f=5)


# it sorts the file
def sort(inPdf, N, f, addblank, W):
    #============= ORDER OF PAGES =============#
    # Number of booklets (Nbk)
    Nbk = (N+ addblank)//(4*f)
    if (N+ addblank)%(4*f) != 0:
        print('Something is wrong with addblank value.')
    # Pages in original order (i.e.: [1, 2, 3, 4, 5, ...])
#    PDF = np.ones(N + addblank) + np.array(range(N + addblank))
    # it will be the correct order
    pdf = np.zeros(N + addblank)
    # loop which enters in each booklet
    for b in range(Nbk):# Booklets loop
        for n in range(0, 4*f, 2):# Couples of pages insde any booklet loop
            bk = b*4*f# Booklet counter
            if n%4 == 2:
                pdf[bk+n+1] = 1+ n/2 + b*4*f# First value of the couple
                pdf[bk+n] = 4*f -n/2 + b*4*f# Second value of the couple
            else:
                pdf[bk+n] = 1+ n/2 + b*4*f# First value of the couple
                pdf[bk+n+1] = 4*f -n/2 + b*4*f# Second value of the couple
    # Pages in correct order (i.e.: [1, 16, 15, 2, 3, ...])
    pdf = pdf.astype(int)
    #===== NEW BOOKLET WITH CORRECT ORDER =====#
    # create the output file
    outPdf = pyp.PdfFileWriter()
    for i in pdf:
        page = inPdf.getPage(i-1)
        # It scales the lateral, so half page is 1/sqrt(2) -> A5
        if W >= 20:
            page.scaleBy(2**(-1/2))
        page.rotateCounterClockwise(90)
        outPdf.addPage(page)
    return outPdf, pdf

# SortedPdf, correct_order = sort(ExtraPagesPdf, N, f, addblank, PageWidth)


# it merges two pages
def merge_pages(file, upper, lower):
    outPdf = pyp.PdfFileWriter()
    
    sup_page = file.getPage(upper)
    inf_page = file.getPage(lower)
    
    sup_width = file.getPage(0).mediaBox.getWidth()# Width of A4 page
    sup_height = file.getPage(0).mediaBox.getHeight()# Height of A4 page
    
    #Esto es una chamba pero funiona. Establezco un tamaño muy pequeño, y luego que se ajuste solo:
    translated_page = PageObject.createBlankPage(None, sup_width-600, sup_height-400)
    translated_page.mergeRotatedTranslatedPage(sup_page, 90, -200, 200, expand=1)
    translated_page.mergeRotatedTranslatedPage(inf_page, 90, 0, 0, expand=1)
    
    outPdf.addPage(translated_page)
    return outPdf



# pega los archivos de dos en dos y guarda cada página en './output/pages'
def twoByTwo(SortedPdf, correct_order):
    pagesMerged = []
    for i in range(0, len(correct_order), 2):
        outPdf = pyp.PdfFileWriter()
        page_merged = merge_pages(SortedPdf, i, i+1)
        page = page_merged.getPage(0)
        outPdf.addPage(page)
        pagesMerged.append(outPdf)
    return pagesMerged



def link_merged(twoBy2):
    outPdf = pyp.PdfFileWriter()
    for page in twoBy2:
        page = page.getPage(0)
        outPdf.addPage(page)
    return outPdf


# dejar una, rotar una
def orientate_page(SortedPdf, _N):
    outPdf = pyp.PdfFileWriter()
    rotate = -1
    for i in range(0, _N, 1):
        if rotate == 1:
            page = SortedPdf.getPage(i)
            page.rotateCounterClockwise(180)
        else:
            page = SortedPdf.getPage(i)
        outPdf.addPage(page)
        rotate *= -1
    with open(joinPath(outputDir, f'{fileName[:-4]}_Booklet.pdf'), 'wb') as fo:
        outPdf.write(fo)

#signFile.close()

#if __name__ == '__main__':
#     # ========================= DEFINE VARIABLES ========================= #
#    
#    N = inPdf.getNumPages() # obtienes el número de páginas del archivo de entrada
#    Page0 = inPdf.getPage(0) # Page0 es la primera página (class PageObect)
#    #Page1 = inPdf.getPage(1) # Page1 es la segunda página (class PageObect)
#    PageShape = Page0.mediaBox # dimensiones de página en pts
#    # (1pt = 1/72 inch = 2,54/72 cm)
#    PageWidth = float(PageShape[2])*(2.54/72) # anchura de página en cm
#    PageHeight = float(PageShape[3])*(2.54/72) # altura de página en cm
#    dinA = [PageHeight, PageWidth]
#    
#    # ========================= RUN the PROGRAM ========================= #
#
#    # Añade páginas blancas al final del archivo original (poner una firma en la última página)
#    ExtraPagesPdf, f, addblank = set_length(inPdf, N, f=4)
#    
#    # la variable _N es el nuevo número de páginas
#    _N = ExtraPagesPdf.getNumPages()
#    print(f'Now, {fileName} has {_N} pages')
#    
#    # Ordena las páginas y devuelve el orden
#    SortedPdf, correct_order = sort(ExtraPagesPdf, N, f, addblank, PageWidth)
#    print('Pages ordered!')
#    
#    # Empaca de dos en dos
#    twoBy2 = twoByTwo(SortedPdf, correct_order)
#    print('Merged two by two.')
#    
#    # Las mete en el mismo pdf
#    almostFinalPdf = link_merged(twoBy2)
#    print('Now, stored\'em all in the same pdf')
#    
#    # número de páginas empacadas en el nuevo pdf
#    _fN = almostFinalPdf.getNumPages()
#    print(f'With {_fN} pages')
#    
#    # Orienta las páginas para imprimir por el borde largo sin rayarse
#    orientate_page(almostFinalPdf, _fN)
#    
#    print('Now you can use FinalPdf.pdf as you want!')
#    inFile.close()
#    print('Remember to remove all files when you have finished and closed this program.')