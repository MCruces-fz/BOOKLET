"""
   M A I N   F I L E
"""

from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import PageObject
from typing import Tuple
import numpy as np
from os.path import join as join_path

from utils.const import OUTDIR, STORE
from utils.footils import inch2mm, mm2inch, basename


class Booklet:
    def __init__(self, input_path, sheets_booklet: int = 4):

        self._input_pdf = PdfFileReader(input_path)
        self.pdf = PdfFileWriter()
        self.pdf.appendPagesFromReader(self._input_pdf)

        signature_path = join_path(STORE, "signature.pdf")
        self.signature = PdfFileReader(signature_path)

        self._sheets_booklet = sheets_booklet  # Sheets per booklet
        self._add_blank = None  # Number of pages to add at the end

    @property
    def sheets_booklet(self) -> int:
        """
        Number of sheets per booklet.

        :return: The number of desired sheets per booklet.
        """
        return self._sheets_booklet

    @sheets_booklet.setter
    def sheets_booklet(self, sheets_booklet):
        """
        The user can choose the number of sheets per booklet.

        :param sheets_booklet:  Number of folded sheets to make each booklet.
        """
        self._sheets_booklet = sheets_booklet

    @property
    def add_blank(self) -> int:
        """
        Property for get the number of pages to add at the end
            of the file. It is needed to match with the number
            of sheets used in each booklet.

        :return: Number of blank pages
        """
        faces_sheet = self._sheets_booklet * 4
        remaining = self._input_pdf.getNumPages() % faces_sheet
        self._add_blank = faces_sheet - remaining
        return self._add_blank

    @staticmethod
    def page_shape(page: PageObject) -> Tuple[float, float]:
        """
        Shape of the pages in millimeters.

        :param page: Page object to check dimensions.
        :return: width and height in millimeters.
        """
        page_shape = page.mediaBox
        pg_width = inch2mm(page_shape.getWidth())
        pg_height = inch2mm(page_shape.getHeight())
        return pg_width, pg_height

    def add_pages(self, pdf: PdfFileWriter, add_blank: int, signature: bool = True) -> PdfFileWriter:
        """
        Add necessary pages to the end of the file.

        :param pdf: Object to add pages at the end.
        :param add_blank: Number of blank pages to fill.
        :param signature: Set if fill with signature, or failing that,
            fill with blank pages.
        """
        for p in range(add_blank):
            if p < self.signature.getNumPages() and signature:
                pdf.addPage(self.signature.getPage(p))
            else:
                pdf.addBlankPage()
        return pdf

    def new_layout(self, pdf: PdfFileWriter) -> PdfFileWriter:
        """
        Takes the PDF object with the expected number of pages and
            applies the new layout. I mean, the correct order to
            be able to print  and fold the booklets correctly.

        :param pdf: PDF object to apply the new layout.
        :return: PDF object with the new layout.
        """

        faces_sheet = self.sheets_booklet * 4
        n_booklets = pdf.getNumPages() // faces_sheet

        # New Layout
        new_layout = np.zeros(pdf.getNumPages())
        for b in range(n_booklets):
            for n in range(0, 4 * self.sheets_booklet, 2):
                booklet_number = b * faces_sheet
                first_couple = 1 + n / 2 + booklet_number
                second_couple = faces_sheet - n / 2 + booklet_number
                if n % 4 == 2:
                    new_layout[booklet_number + n + 1] = first_couple
                    new_layout[booklet_number + n] = second_couple
                else:
                    new_layout[booklet_number + n] = first_couple
                    new_layout[booklet_number + n + 1] = second_couple
        new_layout = new_layout.astype(np.int)

        pg_width, pg_height = self.page_shape(pdf.getPage(0))
        sorted_pdf = PdfFileWriter()
        for p in new_layout:
            page = pdf.getPage(p - 1)
            if (pg_width, pg_height) != (148, 210):  # to dinA5
                w, h = mm2inch(148), mm2inch(210)
                page.scaleTo(w, h)
            # page.rotateCounterClockwise(90)
            sorted_pdf.addPage(page)

        return sorted_pdf

    def merge_pages(self, upper: PageObject, lower: PageObject) -> PageObject:
        """
        Given two dinA5 pages, it merges them into an dinA4 page.
        This was a chamba, and now it is only a chambinha.

        :param upper: Page to locate in the upper half of the dinA4 sheet.
        :param lower: Page to locate in the lower half of the dinA4 sheet.
        :return: The dinA4 page with upper and lower pages merged.
        """

        # w, h = self.page_shape(upper)  # dinA5
        nu_w, nu_h = mm2inch(210), mm2inch(297)  # dinA4

        merged_page = PageObject.createBlankPage(width=nu_w, height=nu_h)

        tx_up, ty_up = self.real_translation(x=nu_w/2, y=nu_h/4)
        merged_page.mergeRotatedTranslatedPage(upper, rotation=90, tx=tx_up, ty=ty_up)

        tx_dw, ty_dw = self.real_translation(x=nu_w/2, y=0)
        merged_page.mergeRotatedTranslatedPage(lower, rotation=90, tx=tx_dw, ty=ty_dw)
        return merged_page

    @staticmethod
    def real_translation(x, y):
        """
        Real translation parameters.
        I don't understand how the PyPDF2 translation and rotation works, so
        that I prefer to translate this coordinates to something I understand.

        :param x: Real x direction (horizontal).
        :param y: Real y direction (vertical).
        :return: translation coordinates for PyPDF2 method.
        """
        tx = x - y
        ty = x + y
        return tx, ty

    def two_by_two(self, pdf: PdfFileWriter) -> PdfFileWriter:
        """
        Merges all pages by couples.

        :param pdf: Input pdf with a pari number of pages, but preferably with
            a number of pages such that pdf.GetNumPages() % sheets_booklet = 0,
            because otherwise in the future it will break.
        :return: Paired PDF instance of PdfFileWriter.
        """
        paired_pdf = PdfFileWriter()
        for i in range(0, pdf.getNumPages(), 2):
            page_i = pdf.getPage(i)
            page_j = pdf.getPage(i + 1)
            merged = self.merge_pages(page_i, page_j)
            paired_pdf.addPage(merged)
        return paired_pdf

    @staticmethod
    def orientate_pages(pdf: PdfFileWriter) -> PdfFileWriter:
        """
        Rotate necessary pages to print in a natural way with any printer.

        :param pdf: Input PDf instance of PdfFileWriter.
        :return: PDF instance of PdfFileWriter with oriented pages.
        """
        rotate = -1
        for p in range(pdf.getNumPages()):
            pdf.getPage(p).rotateClockwise(np.degrees((1 + rotate) * np.pi / 2))
            rotate *= -1
        return pdf

    def create(self) -> PdfFileWriter:
        """
        Create the PDf instance of PdfFileWriter class with all changes done.

        :return: PDF instance of PdfFileWriter.
        """
        pdf = self.add_pages(self.pdf, self.add_blank)
        pdf = self.new_layout(pdf)
        pdf = self.two_by_two(pdf)
        pdf = self.orientate_pages(pdf)
        return pdf

    @classmethod
    def create_and_save(cls, input_file_path: str, output_dir_path: str = OUTDIR):
        """
        Create and save the file.

        :param input_file_path: Full path to the file to convert.
        :param output_dir_path: Full path to the output directory (OUTDIR by default).
        """
        bk = cls(input_file_path)
        pdf = cls.add_pages(bk, bk.pdf, bk.add_blank)
        pdf = cls.new_layout(bk, pdf)
        pdf = cls.two_by_two(bk, pdf)
        pdf = cls.orientate_pages(pdf)

        with open(join_path(output_dir_path, f"{basename(input_file_path)}_booklet.pdf"), 'wb') as fo:
            pdf.write(fo)
