from dataclasses import dataclass, field
from enum import Enum
from typing import List

@dataclass(frozen=True)
class Dimensions:
    width: int
    height: int


class Papierformat(Enum):
    """Dimensions in pixels"""
    A4 = Dimensions(595, 842)
    A5 = Dimensions(420, 595)


@dataclass
class LayoutConfig:
    """Configuration for output booklet layout"""
    sheets_per_booklet: int
    output_paper_size: Dimensions = Papierformat.A4
    include_signature: bool = True

    @property
    def faces_per_booklet(self) -> int:
        faces_per_sheet: int = 4
        return faces_per_sheet * self.sheets_per_booklet


@dataclass
class Page:
    """An original page"""
    page_number: int
    paper_size: Dimensions
    title: str | None = None


@dataclass
class Layout:
    pages: List[Page]
    audit_config: LayoutConfig
    # mapping: dict[int, int] = {}


@dataclass
class BookletPage:
    page_number: int | None = None
    source_page_number: int | None = None

@dataclass
class BookletFace:
    left: BookletPage = field(default_factory=lambda: BookletPage())
    right: BookletPage = field(default_factory=lambda: BookletPage())


@dataclass
class BookletSheet:
    odd: BookletFace = field(default_factory=lambda: BookletFace())
    even: BookletFace = field(default_factory=lambda: BookletFace())
    paper_size: Dimensions = Papierformat.A4


@dataclass
class Booklet:
    number_of_sheets: int
    sheets: List[BookletSheet] | None = None

    def __post_init__(self):
        if self.sheets is None:
            self.sheets = [BookletSheet() for s in range(self.number_of_sheets)] 


if __name__ == "__main__":
    lc = LayoutConfig(sheets_per_booklet=4)
    print(lc.output_paper_size is Papierformat.A4)
    print(lc.faces_per_booklet)