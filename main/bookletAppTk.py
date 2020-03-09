#!/usr/bin/env python
# coding: utf-8

from tkinter import Tk, IntVar, BooleanVar, StringVar
from tkinter import PhotoImage, Spinbox, Checkbutton, Entry, messagebox, Label
from tkinter import TOP, RIGHT, BOTTOM, LEFT, X, N, BOTH
from tkinter import NORMAL, DISABLED
from tkinter import ttk, filedialog
import PyPDF2 as pyp # Documentation at:
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
from packages import inputDir, outputDir


fileName = sorted(os.listdir(inputDir))[-1]
filePath = joinPath(inputDir, fileName)
inFile = open(filePath, 'rb')
inPdf = pyp.PdfFileReader(inFile)
outPdf = pyp.PdfFileWriter()

# =============================================================================
# APLICACIÓN PRINCIPAL
# =============================================================================

class Application():
    def __init__(self):
        self.root = Tk()
        self.root.title("MCruces - Booklets App")
        
        # Carga imagen Fibonacci
        imgFibonacci = PhotoImage(file='Fibonacci.png')
        imgFibonacci = imgFibonacci.subsample(2, 2)
        self.imageFib = ttk.Label(self.root, image=imgFibonacci, anchor="center")
        
        # INPUT
        # Label 'Directory of..."
        self.inputDirLabel = ttk.Label(self.root,text='Input:')
        # Path to Directory
        self.inputDirStr = StringVar(value=inputDir)
        self.inputDirEntry = Entry(self.root, textvariable=self.inputDirStr)
        
        def browseInputDir():
            filename = filedialog.askdirectory()
            self.inputDirStr.set(filename)
        
        # Button Browse
        self.browseInputDirButton = ttk.Button(self.root, text="Browse", command=browseInputDir)
        
        # OUTPUT
        # Label 'Directory of..."
        self.outputDirLabel = ttk.Label(self.root,text='Output:')
        # Path to Directory
        self.outputDirStr = StringVar(value=outputDir)
        self.outputDirEntry = Entry(self.root, textvariable=self.outputDirStr)
        
        def browseOutputDir():
            filename = filedialog.askdirectory()
            self.outputDirStr.set(filename)
        
        # Button Browse
        self.browseOutputDirButton = ttk.Button(self.root, text="Browse", command=browseOutputDir)
        
        
        # Grids
        self.imageFib.grid(row=0, columnspan=4, sticky='w'+'n'+'e'+'s', padx=10, pady=10)
        
        self.inputDirLabel.grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.inputDirEntry.grid(row=1, column=1, columnspan=2, sticky='w'+'e', padx=0, pady=5)
        self.browseInputDirButton.grid(row=1, column=3, padx=5, pady=5)
        
        self.outputDirLabel.grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.outputDirEntry.grid(row=2, column=1, columnspan=2, sticky='w'+'e', padx=0, pady=5)
        self.browseOutputDirButton.grid(row=2, column=3, padx=5, pady=5)
        
#        self.root.attributes("-transparentcolor", "#f0f0f0")
        
        self.root.mainloop()


app = Application()