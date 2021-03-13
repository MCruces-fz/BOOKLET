from os.path import join as join_path

from bookbinder.machine import Booklet
from utils.const import OUTDIR, INPDIR

input_pdf_path = join_path(INPDIR, "CallofCthulhu.pdf")
Booklet.create_and_save(input_pdf_path, OUTDIR)

# booklet = Booklet(input_pdf_path)
# output = booklet.create()
# with open(join_path(OUTDIR, f'output_booklet.pdf'), 'wb') as fo:
#     output.write(fo)
