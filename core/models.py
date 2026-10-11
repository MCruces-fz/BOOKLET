from dataclasses import dataclass
from enum import Enum

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
    faces_per_sheet: int = 4

    @property
    def faces_per_booklet(self) -> int:
        return self.faces_per_sheet * self.sheets_per_booklet


if __name__ == "__main__":
    lc = LayoutConfig(sheets_per_booklet=4)
    print(lc.output_paper_size is Papierformat.A4)
    print(lc.faces_per_booklet)