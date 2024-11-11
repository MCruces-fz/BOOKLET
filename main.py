from bookbinder.machine import BookletReader, BookletWriter
from PyPDF2 import PdfReader
from os.path import join as join_path
from utils.const import OUTDIR, INPDIR, STORAGE, TESTDIR


# input_reader = PdfReader(join_path(TESTDIR, "dummy.pdf"))
input_reader = PdfReader(join_path(INPDIR, "La_Historia_de_mi_Vida.pdf"))
signature_reader = PdfReader(join_path(STORAGE,"signature.pdf"))
booklet_reader = BookletReader(input_reader, signature_reader)
booklet_writer = BookletWriter(booklet_reader)
booklet_writer.save_location = join_path(OUTDIR, "La_Historia_de_mi_Vida_booklet.pdf")
booklet_writer.save()
