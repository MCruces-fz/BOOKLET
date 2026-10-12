from core.models import FACES_PER_SHEET
from core.models import LayoutConfig, Layout, Page, Booklet #, BookletSheet, BookletFace, BookletPage
from typing import List


class Book:

    __booklets: List[Booklet] | None = None

    def __init__(self, config: LayoutConfig, source_length: int):
        self.config = config
        self.source_lenght = source_length

    @property
    def booklets(self) -> List[Booklet]:
        if self.__booklets is None:
            self.__booklets = [
                Booklet(index, number_of_sheets=self.config.sheets_per_booklet) 
                for index in range(self.booklets_quantity)
            ]
        return self.__booklets

    @property
    def booklets_quantity(self) -> int:
        """
        The quantity of booklets is calculated taking into account:
        - source document pages
        - signature pages (optional)
        
        then, final number of pages depends on how many booklets we will need.
        """
        full_length = self.source_lenght

        # TODO Signature logic should live outside Book
        signature_length = 2 
        if self.config.include_signature:
            full_length += signature_length

        # NOTE: equivalent to math.ceil(full_length / config.faces_per_booklet)
        return (full_length - 1) // self.config.faces_per_booklet + 1


class Engine:

    def booklets_quantity(config, pages):
        """
        The quantity of booklets is calculated taking into account:
        - source document pages
        - signature pages (optional)
        
        then, final number of pages depends on how many booklets we will need.
        """
        full_length = len(pages)

        signature_length = 2
        if config.include_signature:
            full_length += signature_length

        # NOTE: equivalent to math.ceil(full_length / config.faces_per_booklet)
        return (full_length - 1) // config.faces_per_booklet + 1

    @classmethod
    def compute_layout(self, config: LayoutConfig, pages: List[Page]) -> Layout:
        
        # TODO: Aquí lo ideal sería recorrer el objeto `Book` por el orden correcto
        # e ir añadiendo en cada `BookletPage` los `page_nubmer` y `source_page_number` correspondientes.
        # Si se recorren las páginas por el orden correcto, ya tenemos el layout final. 

        book = Book(config, len(pages))

        mapping: dict[int, int] = {}

        for booklet_number in range(book.booklets_quantity):
            first_page_booklet = booklet_number * config.faces_per_booklet
            for couple_index in range(0, config.faces_per_booklet, 2):
                first_couple = 1 + couple_index//2 + first_page_booklet
                second_couple = config.faces_per_booklet - couple_index//2 + first_page_booklet

                if couple_index % FACES_PER_SHEET == 2:
                    mapping.update({first_page_booklet + couple_index : first_couple - 1})
                    mapping.update({first_page_booklet + couple_index + 1 : second_couple - 1})
                else:
                    mapping.update({first_page_booklet + couple_index + 1 : first_couple - 1})
                    mapping.update({first_page_booklet + couple_index : second_couple - 1})
        
        mapping = dict(sorted(mapping.items()))
         
        return Layout(pages, config, book, mapping)

