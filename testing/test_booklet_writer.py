import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bookbinder.machine import BookletReader, BookletWriter
from PyPDF2 import PdfReader, PdfWriter, PageObject, Transformation


# input_reader = PdfReader("testing/dummy.pdf")
input_reader = PdfReader("input/CallofCthulhu.pdf")
signature_reader = PdfReader("store/signature.pdf")
booklet_reader = BookletReader(input_reader, signature_reader)
booklet_writer = BookletWriter(booklet_reader)
booklet_writer.save_location = "testing/dummy_output.pdf" 
booklet_writer.save()