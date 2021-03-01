#!/usr/bin/env python
# coding: utf-8

from tkinter import Tk, IntVar, BooleanVar, StringVar
from tkinter import PhotoImage, Spinbox, Checkbutton, Entry, messagebox, Label
# from tkinter import TOP, RIGHT, BOTTOM, LEFT, BOTH
# from tkinter import NORMAL, DISABLED
from tkinter import ttk, filedialog
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
from packages.utils import set_length, sort, twoByTwo, link_merged, orientate_page
from packages import inputDir, outputDir


# =============================================================================
# APLICACIÓN PRINCIPAL
# =============================================================================

class Application:
    def __init__(self):
        self.root = Tk()
        self.root.title("MCruces - Booklets App")
        self.root.configure(background='#f0f0f0')

        #        style = ttk.Style(self.root)
        #        style.theme_use('classic')
        #        style.configure('Dlr.TFrame', background='blue')

        # Carga imagen Fibonacci
        imgFibonacci = PhotoImage(file='Fibonacci.png')
        imgFibonacci = imgFibonacci.subsample(2, 2)
        self.imageFib = ttk.Label(self.root, image=imgFibonacci, anchor="center")

        self.titleLabel = Label(self.root, text='Booklet Machine', font='Helvetica 20 bold')

        # INPUT
        # Label 'Directory of..."
        self.inputDirLabel = ttk.Label(self.root, text='Input:')
        # Path to Directory
        self.inputDirStr = StringVar(value=inputDir)
        self.inputDirEntry = Entry(self.root, width=30, textvariable=self.inputDirStr, justify='right')

        def browseInputDir():
            filename = filedialog.askdirectory()
            self.inputDirStr.set(filename)

        # Button Browse 1
        self.browseInputDirButton = ttk.Button(self.root, text="Browse", command=browseInputDir)

        # OUTPUT
        # Label 'Directory of..."
        self.outputDirLabel = ttk.Label(self.root, text='Output:')
        # Path to Directory
        self.outputDirStr = StringVar(value=outputDir)
        self.outputDirEntry = Entry(self.root, width=30, textvariable=self.outputDirStr, justify='right')

        def browseOutputDir():
            filename = filedialog.askdirectory()
            self.outputDirStr.set(filename)

        # Button Browse 2
        self.browseOutputDirButton = ttk.Button(self.root, text="Browse", command=browseOutputDir)

        # f Number
        # Number of sheets per booklet
        self.fNumberLabel = ttk.Label(self.root, text='Sheets per booklet:')
        # Path to Directory
        self.fNumberInt = IntVar(value=5)
        self.fNumberEntry = Spinbox(self.root, from_=1, to=500, wrap=True, width=5, textvariable=self.fNumberInt)

        # Button RUN
        self.runButton = ttk.Button(self.root, text="RUN", command=self.createBooklet)

        # Grids
        self.imageFib.grid(row=0, columnspan=4, sticky='news', padx=10, pady=10)

        self.titleLabel.grid(row=1, column=0, columnspan=4, sticky='we', padx=5, pady=5)

        self.inputDirLabel.grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.inputDirEntry.grid(row=2, column=1, columnspan=2, sticky='we', padx=0, pady=5)
        self.browseInputDirButton.grid(row=2, column=3, sticky='we', padx=5, pady=5)

        self.outputDirLabel.grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.outputDirEntry.grid(row=3, column=1, columnspan=2, sticky='we', padx=0, pady=5)
        self.browseOutputDirButton.grid(row=3, column=3, sticky='we', padx=5, pady=5)

        self.fNumberLabel.grid(row=4, column=0, columnspan=2, sticky='e', padx=5, pady=5)
        self.fNumberEntry.grid(row=4, column=2, sticky='w', padx=5, pady=5)

        self.runButton.grid(row=5, column=0, columnspan=4, sticky='we', padx=5, pady=5)

        #        self.root.attributes("-transparentcolor", "#f0f0f0")

        self.root.mainloop()

    def createBooklet(self):
        # ========================= DEFINE VARIABLES ========================= #

        fileName = sorted(os.listdir(self.inputDirStr.get()))[-1]
        filePath = joinPath(self.inputDirStr.get(), fileName)
        inFile = open(filePath, 'rb')
        inPdf = pyp.PdfFileReader(inFile)
        outPdf = pyp.PdfFileWriter()

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
        ExtraPagesPdf, f, addblank = set_length(inPdf, N, f=self.fNumberInt.get())

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
        orientate_page(almostFinalPdf, _fN, self.outputDirStr.get())

        print(f'Now you can use {fileName[:-4]}_Booklet.pdf as you want!')
        inFile.close()
        # signFile.close()


app = Application()
