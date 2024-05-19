import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bookbinder.booklet_reader import BookletReader
from PyPDF2 import PdfReader, PdfWriter, PageObject, Transformation



# input_reader = PdfReader("testing/dummy.pdf")
input_reader = PdfReader("input/CallofCthulhu.pdf")
signature_reader = PdfReader("store/signature.pdf")
booklet_reader = BookletReader(input_reader, signature_reader)
print("Reader length", len(input_reader.pages))
print("Booklet length", booklet_reader.length)

# for n in range(booklet_reader.length):
#     print(f"Page {n}:", booklet_reader.page(n))


print(booklet_reader.booklet_layout)

writer = PdfWriter()
for ix, n in enumerate(range(0, booklet_reader.length, 2)):
    # print(f"Page {n}:", booklet_reader.sorted_page(n))
    # print(f"Page {n + 1}:", booklet_reader.sorted_page(n + 1))

    print(f"Coupple {n}|{n + 1}:", booklet_reader.sorted_page(n, debug=True), "|", booklet_reader.sorted_page(n + 1, debug= True))
    left_page = booklet_reader.sorted_page(n)
    right_page = booklet_reader.sorted_page(n+1)

    big_page = PageObject.create_blank_page(height=left_page.mediabox.height, width=left_page.mediabox.width*2)
    big_page.merge_page(right_page)
    big_page.add_transformation(Transformation().translate(tx=left_page.mediabox.width))
    big_page.merge_page(left_page)

    writer.add_page(big_page.rotate(90 if ix % 2 else -90))


with open("testing/dummy_output.pdf", "wb") as fp:
    writer.write(fp)