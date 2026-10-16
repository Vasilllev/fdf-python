import sys
from collections.abc import Sequence

from fdf.errors import FdfError
from fdf.interface import show_map
from fdf.parser import parse_map_file


def main(arguments: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if arguments is None else arguments)
    if len(args) != 1:
        print("Использование: python main.py maps/elem.fdf", file=sys.stderr)
        return 2
    try:
        map_data = parse_map_file(args[0])
    except FileNotFoundError:
        print(f"Файл не найден: {args[0]}", file=sys.stderr)
        return 1
    except FdfError as error:
        print(f"Ошибка карты: {error}", file=sys.stderr)
        return 1

    try:
        show_map(map_data)
    except RuntimeError as error:
        print(f"Не удалось открыть окно: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
