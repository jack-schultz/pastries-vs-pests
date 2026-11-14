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
