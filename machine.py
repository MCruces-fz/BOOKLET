"""
   M A I N   F I L E
"""

from PyPDF2 import PdfFileReader

input_pdf_path = "input/CallofCthulhu.pdf"

inp_pdf = PdfFileReader(input_pdf_path)
