import re
from pathlib import Path

from fdf.errors import MapFormatError
from fdf.model import FdfMap, Point

_COLOR_PATTERN = re.compile(r"0x[0-9a-fA-F]{1,6}\Z")


def parse_map_text(text: str) -> FdfMap:
    lines = text.splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        raise MapFormatError("Пустая карта")

    rows: list[list[Point]] = []
    expected_width: int | None = None
    for row_index, line in enumerate(lines, start=1):
        if not line.strip():
            raise MapFormatError(f"Строка {row_index}: пустая строка внутри карты")
        tokens = line.split()
        if expected_width is None:
            expected_width = len(tokens)
        elif len(tokens) != expected_width:
            raise MapFormatError(f"Строка {row_index}, колонка {len(tokens) + 1}: разная ширина строк")

        row: list[Point] = []
        for column, token in enumerate(tokens, start=1):
            pieces = token.split(",")
            if len(pieces) > 2 or not pieces[0]:
                raise MapFormatError(f"Строка {row_index}, колонка {column}: неверное значение")
            try:
                z = int(pieces[0])
            except ValueError as error:
                raise MapFormatError(f"Строка {row_index}, колонка {column}: высота должна быть целым числом") from error

            color: str | None = None
            if len(pieces) == 2:
                if not _COLOR_PATTERN.fullmatch(pieces[1]):
                    raise MapFormatError(f"Строка {row_index}, колонка {column}: неверный цвет")
                color = "#" + pieces[1][2:].upper().zfill(6)
            row.append(Point(len(row), row_index - 1, z, color))
        rows.append(row)
    return FdfMap(rows)


def parse_map_file(path: str | Path) -> FdfMap:
    return parse_map_text(Path(path).read_text(encoding="utf-8-sig"))

