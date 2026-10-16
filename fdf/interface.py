import tkinter as tk
from tkinter import TclError

from fdf.model import FdfMap
from fdf.projection import Camera


def show_map(map_data: FdfMap) -> None:
    try:
        root = tk.Tk()
        root.title("FDF — каркасная модель")
        canvas = tk.Canvas(root, background="black", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        camera = Camera()

        def draw(_event: tk.Event[tk.Misc] | None = None) -> None:
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            camera.fit(map_data, width, height)
            canvas.delete("all")
            for point in map_data:
                start = camera.project(point)
                for neighbor in map_data.neighbors(point):
                    end = camera.project(neighbor)
                    canvas.create_line(*start, *end, fill=point.color or neighbor.color or "white")

        canvas.bind("<Configure>", draw)
        root.bind("<Escape>", lambda _event: root.destroy())
        root.mainloop()
    except TclError as error:
        raise RuntimeError("Не удалось открыть графическое окно") from error
