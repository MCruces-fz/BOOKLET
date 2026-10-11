# from bookbinder.machine import BookletReader, BookletWriter
# from PyPDF2 import PdfReader
# from os.path import join as join_path
# from utils.const import OUTDIR, INPDIR, STORAGE, TESTDIR


# # input_reader = PdfReader(join_path(TESTDIR, "dummy.pdf"))
# input_reader = PdfReader(join_path(INPDIR, "La_Historia_de_mi_Vida.pdf"))
# signature_reader = PdfReader(join_path(STORAGE,"signature.pdf"))
# booklet_reader = BookletReader(input_reader, signature_reader)
# booklet_writer = BookletWriter(booklet_reader)
# booklet_writer.save_location = join_path(OUTDIR, "La_Historia_de_mi_Vida_booklet.pdf")
# booklet_writer.save()



from core.layout_engine import Engine, Book
from core.models import LayoutConfig, Page, Papierformat

layout_config = LayoutConfig(sheets_per_booklet=4)
pages = [
    Page(1, Papierformat.A5, title="Authors"), 
    Page(2, Papierformat.A5, title="Index"),
    Page(3, Papierformat.A5),
    Page(4, Papierformat.A5, title="END")
    ]

eng = Engine.compute_layout(layout_config, pages)

book = Book(config=layout_config, source_length=15)
# print(len(book.booklets))
print(book.booklets_quantity)

for bkl in book.booklets:
    print(bkl)
