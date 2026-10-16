import math
from dataclasses import dataclass

from fdf.model import FdfMap, Point


@dataclass
class Camera:
    scale: float = 1.0
    offset_x: float = 0.0
    offset_y: float = 0.0
    z_scale: float = 1.0

    def project(self, point: Point) -> tuple[float, float]:
        angle = math.radians(30)
        projected_x = (point.x - point.y) * math.cos(angle)
        projected_y = (point.x + point.y) * math.sin(angle) - point.z * self.z_scale
        return (projected_x * self.scale + self.offset_x,
                projected_y * self.scale + self.offset_y)

    def fit(self, map_data: FdfMap, width: int, height: int) -> None:
        points = list(map_data)
        if not points:
            return
        angle = math.radians(30)
        projected = [((point.x - point.y) * math.cos(angle),
                      (point.x + point.y) * math.sin(angle) - point.z * self.z_scale)
                     for point in points]
        min_x = min(point[0] for point in projected)
        max_x = max(point[0] for point in projected)
        min_y = min(point[1] for point in projected)
        max_y = max(point[1] for point in projected)
        projected_width = max_x - min_x
        projected_height = max_y - min_y
        ratios: list[float] = []
        if projected_width > 0:
            ratios.append(width / projected_width)
        if projected_height > 0:
            ratios.append(height / projected_height)
        self.scale = min(ratios) * 0.9 if ratios else 1.0
        self.offset_x = width / 2 - (min_x + max_x) * self.scale / 2
        self.offset_y = height / 2 - (min_y + max_y) * self.scale / 2
