"""
   M A I N   F I L E
"""

from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import PageObject
from typing import Union
from decimal import Decimal
import numpy as np
from os.path import join as join_path

from utils.const import OUTDIR

input_pdf_path = "input/CallofCthulhu.pdf"


class Booklet:
    def __init__(self, input_path, sheets_booklet: int = 4):

        input_pdf = PdfFileReader(input_path)
        self.pdf = PdfFileWriter()
        self.pdf.appendPagesFromReader(input_pdf)

        signature_path = "store/signature.pdf"
        self.signature = PdfFileReader(signature_path)

        self.sheets_booklet = sheets_booklet  # Sheets per booklet
        self.faces_sheet = self.sheets_booklet * 4
        remaining = self.pdf.getNumPages() % self.faces_sheet
        self.add_blank = self.faces_sheet - remaining

    @staticmethod
    def inch2mm(value: Union[int, float, Decimal]) -> float:
        """
        Conversion of inches to millimeters.
    
        :param value: Value in inches to convert to millimeters.
        :return: Value in millimeters.
        """
        return float(value) * 25.4 / 72

    def page_shape(self):
        """
        Shape of the pages in millimeters.
        """
        page_shape = self.pdf.getPage(0).mediaBox
        pg_width = self.inch2mm(page_shape.lowerRight[0] - page_shape.lowerLeft[0])
        pg_height = self.inch2mm(page_shape.upperLeft[1] - page_shape.lowerLeft[1])
        # print(f"PDF with {self.pdf.getNumPages()} pages and dimensions {pg_width:.0f}x{pg_height:.0f} mm")
        return pg_width, pg_height

    def add_pages(self):
        """
        Add necessary pages
        """
        for p in range(self.add_blank):
            if p < self.signature.getNumPages():
                self.pdf.addPage(self.signature.getPage(p))
            else:
                self.pdf.addBlankPage()

    def new_layout(self):
        n_booklets = self.pdf.getNumPages() // self.faces_sheet

        new_layout = np.zeros(self.pdf.getNumPages())

        # New Layout
        for b in range(n_booklets):
            for n in range(0, 4 * self.sheets_booklet, 2):
                booklet_number = b * self.faces_sheet
                first_couple = 1 + n / 2 + booklet_number
                second_couple = self.faces_sheet - n / 2 + booklet_number
                if n % 4 == 2:
                    new_layout[booklet_number + n + 1] = first_couple
                    new_layout[booklet_number + n] = second_couple
                else:
                    new_layout[booklet_number + n] = first_couple
                    new_layout[booklet_number + n + 1] = second_couple
        new_layout = new_layout.astype(np.int)

        pg_width, pg_height = self.page_shape()
        sorted_pdf = PdfFileWriter()
        for p in new_layout:
            page = self.pdf.getPage(p - 1)
            if pg_width >= 200:
                page.scaleBy(2 ** (-1 / 2))
            page.rotateCounterClockwise(90)
            sorted_pdf.addPage(page)

        self.pdf = sorted_pdf

    def two_by_two(self):
        paired_pdf = PdfFileWriter()
        for i in range(0, self.pdf.getNumPages(), 2):
            merged = self.merge_pages(i, i + 1)
            paired_pdf.addPage(merged)

    def merge_pages(self, current: int, next_: int) -> PageObject:
        pass

    def create(self):
        self.add_pages()
        self.new_layout()
        return self.pdf


if __name__ == '__main__':
    booklet = Booklet(input_pdf_path)
    output = booklet.create()
    with open(join_path(OUTDIR, f'output_booklet.pdf'), 'wb') as fo:
        output.write(fo)
