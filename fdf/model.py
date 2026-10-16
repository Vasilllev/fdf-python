from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int
    color: str | None = None


class FdfMap:
    def __init__(self, rows: list[list[Point]]) -> None:
        self.rows = rows
        self.height = len(rows)
        self.width = len(rows[0]) if rows else 0

    def __len__(self) -> int:
        return self.width * self.height

    def __iter__(self) -> Iterator[Point]:
        for row in self.rows:
            yield from row

    def neighbors(self, point: Point) -> list[Point]:
        result: list[Point] = []
        if point.x + 1 < self.width:
            result.append(self.rows[point.y][point.x + 1])
        if point.y + 1 < self.height:
            result.append(self.rows[point.y + 1][point.x])
        return result
