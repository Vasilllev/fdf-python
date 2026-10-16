from pathlib import Path

import pytest

from fdf.errors import MapFormatError
from fdf.parser import parse_map_file, parse_map_text
from fdf.projection import Camera


def test_example_map_dimensions_and_center_height() -> None:
    map_data = parse_map_file(Path("maps/elem.fdf"))
    assert (map_data.width, map_data.height, len(map_data)) == (7, 7, 49)
    assert map_data.rows[3][3].z == 4


def test_negative_heights_and_colors() -> None:
    map_data = parse_map_text("-2,0xF 3,0x12AB\n")
    assert [point.z for point in map_data] == [-2, 3]
    assert [point.color for point in map_data] == ["#00000F", "#0012AB"]


@pytest.mark.parametrize("contents", ["", "1 x", "1 2\n3", "1,0x", "1,0x1234567"])
def test_invalid_maps(contents: str) -> None:
    with pytest.raises(MapFormatError):
        parse_map_text(contents)


def test_model_iteration_and_corner_neighbors() -> None:
    map_data = parse_map_text("1 2\n3 4")
    assert [point.z for point in map_data] == [1, 2, 3, 4]
    assert [point.z for point in map_data.neighbors(map_data.rows[0][0])] == [2, 3]


def test_projection_and_camera_fit() -> None:
    camera = Camera()
    assert camera.project(parse_map_text("0").rows[0][0]) == (0.0, 0.0)
    raised = parse_map_text("0\n1")
    camera.fit(raised, 800, 600)
    coords = [camera.project(point) for point in raised]
    assert coords[1][1] < coords[0][1]
    assert (min(x for x, _ in coords) + max(x for x, _ in coords)) / 2 == pytest.approx(400)
    assert (min(y for _, y in coords) + max(y for _, y in coords)) / 2 == pytest.approx(300)
