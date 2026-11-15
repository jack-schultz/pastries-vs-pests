import time
import tkinter as tk
import pytest


@pytest.fixture
def canvas():
    root = tk.Tk()
    root.withdraw()
    canvas = tk.Canvas(root, width=900, height=600)
    canvas.pack()
    yield canvas
    root.destroy()


@pytest.fixture
def fast_forward(monkeypatch):
    # Returns a function that jumps the clock so timers have run out.
    def jump(seconds=1000):
        later = time.monotonic() + seconds
        monkeypatch.setattr(time, "monotonic", lambda: later)
    return jump
